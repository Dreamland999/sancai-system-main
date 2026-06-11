from __future__ import annotations

import hashlib
import random
import re
import sys
from pathlib import Path
from typing import Any, Iterable

import numpy as np
import pandas as pd

try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    from torch.utils.data import DataLoader, TensorDataset

    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    torch = None  # type: ignore[assignment]
    nn = None  # type: ignore[assignment]
    F = None  # type: ignore[assignment]
    DataLoader = None  # type: ignore[assignment]
    TensorDataset = None  # type: ignore[assignment]


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT.parent / "data"
REPORTS_DIR = ROOT.parent / "reports"
RANDOM_SEED = 42
CSV_ENCODINGS = ("utf-8-sig", "utf-8", "gbk")

INPUT_FILES = {
    "标签字典表": DATA_DIR / "标签字典表_最终检查版.csv",
    "饮品成分表": DATA_DIR / "饮品成分表_最终检查版.csv",
    "饮品方案表": DATA_DIR / "饮品方案表_最终检查版.csv",
    "用户输入表": DATA_DIR / "用户输入表_最终检查版.csv",
}

OUTPUT_RECOMMENDATION_CSV = REPORTS_DIR / "推荐记录表_双塔_MLP排序版.csv"
OUTPUT_RECOMMENDATION_XLSX = REPORTS_DIR / "推荐记录表_双塔_MLP排序版.xlsx"
OUTPUT_TRAINING_CSV = REPORTS_DIR / "双塔训练样本.csv"
OUTPUT_RANKER_TRAINING_CSV = REPORTS_DIR / "MLP排序训练样本.csv"
OUTPUT_REPORT_TXT = REPORTS_DIR / "双塔_MLP排序评估报告.txt"
OUTPUT_MODEL_PT = ROOT / "twin_tower_model.pt"
OUTPUT_RANKER_MODEL_PT = ROOT / "mlp_ranker_model.pt"
OUTPUT_VOCAB_JSON = ROOT / "twin_tower_vocab.json"

USER_TAG_FIELDS = [
    "时间段",
    "地点/场景",
    "身体状态标签",
    "心情状态标签",
    "体验需求标签",
    "口味偏好",
    "冷热偏好",
    "饮食限制",
    "地区标签",
    "兴趣标签",
    "系统解析标签",
]

RECIPE_TAG_FIELDS = [
    "成分组合",
    "成分角色",
    "用量等级",
    "适配身体状态",
    "适配心情状态",
    "感官标签",
    "体验标签",
    "健康约束",
    "甜度建议",
    "冷热建议",
    "推荐解释",
    "视觉标签",
    "可否机器制作",
]

INGREDIENT_TAG_FIELDS = [
    "成分类别",
    "成分角色",
    "是否含咖啡因",
    "是否含乳",
    "感官标签",
    "状态/体验标签",
    "健康约束",
    "视觉标签",
]

REQUIRED_OUTPUT_COLUMNS = [
    "recommendation_id",
    "session_id",
    "user_id",
    "recipe_id",
    "饮品名称",
    "推荐排名",
    "双塔相似度",
    "规则综合分",
    "状态匹配分",
    "风味偏好分",
    "场景适配分",
    "健康约束分",
    "视觉适配分",
    "制作可行性分",
    "新颖度分",
    "baseline_rank_score",
    "mlp_rank_score",
    "最终排序分",
    "候选来源",
    "是否通过规则过滤",
    "过滤原因",
    "推荐理由",
    "推荐标签依据",
]

LIST_SPLIT_RE = re.compile(r"[、，,/；;｜|\s\r\n]+")
NIGHT_KEYWORDS = {"夜间", "晚上", "晚间", "睡前", "深夜", "夜宵"}
MILK_LIMIT_KEYWORDS = {"乳糖不耐", "无乳", "无奶", "乳制品过敏", "牛奶过敏", "不含乳"}
CAFFEINE_LIMIT_KEYWORDS = {"咖啡因敏感", "低咖啡因", "少咖啡因", "无咖啡因", "低因"}
LOW_SUGAR_KEYWORDS = {"控糖", "低糖", "少糖", "无糖", "低甜"}
GASTRIC_SENSITIVE_KEYWORDS = {"胃敏感", "胃不适", "胃弱", "胃炎", "空腹不适", "肠胃敏感"}

MILK_RECIPE_KEYWORDS = {"牛奶", "鲜奶", "奶油", "淡奶油", "奶盖", "酸奶", "芝士", "炼乳", "奶泡"}
CAFFEINE_RECIPE_KEYWORDS = {"美式", "咖啡", "浓缩", "冷萃", "espresso", "意式浓缩", "手冲", "拿铁", "摩卡"}
STRONG_STIMULUS_KEYWORDS = {"强刺激", "浓缩", "美式", "高因", "高咖啡因", "辛辣", "气泡", "冰爽"}
HIGH_SWEET_KEYWORDS = {"高甜", "全糖", "多糖", "厚甜", "甜口", "甜感强"}
ACID_GAS_KEYWORDS = {"强酸", "高酸", "气泡", "碳酸", "苏打", "鲜酸", "强气泡"}


def seed_everything(seed: int = RANDOM_SEED) -> None:
    random.seed(seed)
    np.random.seed(seed)
    if TORCH_AVAILABLE:
        torch.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)


def clean_text(value: object) -> str:
    if value is None:
        return ""
    text = str(value).replace("\u3000", " ").strip()
    if text.lower() == "nan":
        return ""
    return text


def dataframe_score(df: pd.DataFrame) -> int:
    columns_text = "|".join([clean_text(column) for column in df.columns])
    sample_text = "|".join([clean_text(value) for value in df.head(3).astype(str).fillna("").values.flatten().tolist()])
    text = columns_text + "|" + sample_text
    score = 0
    for token in ["标签", "成分", "饮品", "用户", "session", "recipe", "ingredient", "时间", "状态", "口味", "冷热", "推荐"]:
        if token in text:
            score += 1
    chinese_count = sum(1 for ch in text if "\u4e00" <= ch <= "\u9fff")
    score += min(chinese_count // 10, 10)
    return score


def read_csv_auto(path: Path) -> pd.DataFrame:
    best_df: pd.DataFrame | None = None
    best_score = -1
    last_error: Exception | None = None
    for encoding in CSV_ENCODINGS:
        try:
            df = pd.read_csv(path, dtype=str, keep_default_na=False, encoding=encoding, engine="python")
            score = dataframe_score(df)
            if score > best_score:
                best_score = score
                best_df = df
        except Exception as exc:
            last_error = exc
    if best_df is not None:
        return best_df
    raise last_error  # type: ignore[misc]


def drop_empty_rows_cols(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df.copy()
    df = df.copy().fillna("")
    for column in df.columns:
        df[column] = df[column].map(clean_text)
    non_empty_columns = [column for column in df.columns if not df[column].eq("").all()]
    df = df[non_empty_columns].copy()
    if df.empty:
        return df.reset_index(drop=True)
    non_empty_rows = ~df.eq("").all(axis=1)
    return df.loc[non_empty_rows].reset_index(drop=True)


def split_tags(value: object) -> list[str]:
    text = clean_text(value)
    if not text:
        return []
    tokens: list[str] = []
    for token in LIST_SPLIT_RE.split(text):
        token = clean_text(token).strip("。．.,")
        if token:
            tokens.append(token)
    return dedupe_preserve_order(tokens)


def dedupe_preserve_order(items: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        value = clean_text(item)
        if value and value not in seen:
            seen.add(value)
            result.append(value)
    return result


def normalize_join(values: Iterable[str]) -> str:
    return "、".join([clean_text(value) for value in values if clean_text(value)])


def overlap_score(left: Iterable[str], right: Iterable[str]) -> float:
    left_set = set([clean_text(item) for item in left if clean_text(item)])
    right_set = set([clean_text(item) for item in right if clean_text(item)])
    if not left_set or not right_set:
        return 0.0
    return len(left_set & right_set) / max(len(left_set), len(right_set), 1)


def contains_any(text: str, keywords: Iterable[str]) -> bool:
    value = clean_text(text)
    return any(keyword and keyword in value for keyword in keywords)


def stable_random_float(*parts: str, seed: int = RANDOM_SEED) -> float:
    digest = hashlib.sha256(("|".join([str(seed), *parts])).encode("utf-8")).hexdigest()
    return int(digest[:16], 16) / float(16 ** 16 - 1)


def to_numeric_score(value: object, default: float = 0.0) -> float:
    text = clean_text(value)
    if not text:
        return default
    mapping = {
        "是": 1.0,
        "可": 1.0,
        "需预制": 0.7,
        "需要预制": 0.7,
        "预制": 0.7,
        "暂不适合": 0.3,
        "否": 0.3,
        "低": 0.3,
        "中": 0.6,
        "高": 1.0,
    }
    if text in mapping:
        return mapping[text]
    if "预制" in text:
        return 0.7
    if "不适合" in text:
        return 0.3
    return default


def normalize_columns(df: pd.DataFrame, aliases: dict[str, list[str]]) -> pd.DataFrame:
    rename_map: dict[str, str] = {}
    normalized_actual = {
        re.sub(r"[\s\-_/、，,;；|｜]+", "", clean_text(column)): column for column in df.columns
    }
    for canonical, candidates in aliases.items():
        found = None
        for candidate in [canonical, *candidates]:
            if candidate in df.columns:
                found = candidate
                break
            candidate_key = re.sub(r"[\s\-_/、，,;；|｜]+", "", clean_text(candidate))
            if candidate_key in normalized_actual:
                found = normalized_actual[candidate_key]
                break
        if found and found != canonical:
            rename_map[found] = canonical
    if rename_map:
        df = df.rename(columns=rename_map)
    return df


def discover_missing_fields(df: pd.DataFrame, required_fields: list[str]) -> list[str]:
    return [field for field in required_fields if field not in df.columns]


def build_user_tags(user_row: pd.Series) -> tuple[list[str], dict[str, list[str]]]:
    field_tags: dict[str, list[str]] = {}
    merged: list[str] = []
    for field in USER_TAG_FIELDS:
        tags = split_tags(user_row.get(field, ""))
        field_tags[field] = tags
        merged.extend(tags)
    return dedupe_preserve_order(merged), field_tags


def parse_composition_tokens(text: object) -> list[str]:
    tokens: list[str] = []
    for token in split_tags(text):
        token = re.sub(r"\s+", "", token)
        if token:
            tokens.append(token)
    return dedupe_preserve_order(tokens)


def build_ingredient_lookup(ingredient_df: pd.DataFrame) -> dict[str, dict[str, Any]]:
    lookup: dict[str, dict[str, Any]] = {}
    if "成分名称" not in ingredient_df.columns:
        return lookup
    for _, row in ingredient_df.iterrows():
        name = clean_text(row.get("成分名称", ""))
        if name:
            lookup[name] = {column: row.get(column, "") for column in ingredient_df.columns}
    return lookup


def match_ingredients_from_composition(composition_text: object, ingredient_lookup: dict[str, dict[str, Any]]) -> tuple[list[str], list[dict[str, Any]], list[str]]:
    composition_tokens = parse_composition_tokens(composition_text)
    ingredient_names = list(ingredient_lookup.keys())
    matched_names: list[str] = []
    matched_rows: list[dict[str, Any]] = []
    missing_tokens: list[str] = []
    for token in composition_tokens:
        exact_matches = [name for name in ingredient_names if token == name or token in name or name in token]
        if exact_matches:
            for name in exact_matches:
                if name not in matched_names:
                    matched_names.append(name)
                    matched_rows.append(ingredient_lookup[name])
        else:
            missing_tokens.append(token)
    return matched_names, matched_rows, dedupe_preserve_order(missing_tokens)


def build_recipe_tags(recipe_row: pd.Series, ingredient_lookup: dict[str, dict[str, Any]]) -> tuple[list[str], dict[str, list[str]], list[str], list[str]]:
    field_tags: dict[str, list[str]] = {}
    merged: list[str] = []
    for field in RECIPE_TAG_FIELDS:
        tags = split_tags(recipe_row.get(field, ""))
        field_tags[field] = tags
        merged.extend(tags)

    matched_names, matched_ingredient_rows, missing_tokens = match_ingredients_from_composition(recipe_row.get("成分组合", ""), ingredient_lookup)
    merged.extend(matched_names)

    for ingredient_row in matched_ingredient_rows:
        for field in INGREDIENT_TAG_FIELDS:
            merged.extend(split_tags(ingredient_row.get(field, "")))

    return dedupe_preserve_order(merged), field_tags, matched_names, missing_tokens


def build_recipe_side_metadata(recipe_df: pd.DataFrame, ingredient_lookup: dict[str, dict[str, Any]]) -> tuple[dict[str, dict[str, Any]], list[str]]:
    metadata: dict[str, dict[str, Any]] = {}
    missing_ingredients: list[str] = []
    for _, row in recipe_df.iterrows():
        recipe_id = clean_text(row.get("recipe_id", ""))
        if not recipe_id:
            continue
        tags, field_tags, matched_names, missing_tokens = build_recipe_tags(row, ingredient_lookup)
        metadata[recipe_id] = {
            "tags": tags,
            "field_tags": field_tags,
            "matched_ingredients": matched_names,
            "missing_ingredients": missing_tokens,
        }
        missing_ingredients.extend(missing_tokens)
    return metadata, dedupe_preserve_order(missing_ingredients)


def detect_milk_risk(recipe_row: pd.Series, recipe_meta: dict[str, Any], ingredient_lookup: dict[str, dict[str, Any]]) -> bool:
    recipe_text = "、".join(
        [
            clean_text(recipe_row.get("健康约束", "")),
            clean_text(recipe_row.get("成分组合", "")),
            clean_text(recipe_row.get("推荐解释", "")),
            clean_text(recipe_row.get("成分角色", "")),
            clean_text(recipe_row.get("饮品名称", "")),
        ]
    )
    if contains_any(recipe_text, MILK_RECIPE_KEYWORDS):
        return True
    for ingredient_name in recipe_meta.get("matched_ingredients", []):
        ingredient_row = ingredient_lookup.get(ingredient_name, {})
        if clean_text(ingredient_row.get("是否含乳", "")) in {"是", "高", "1", "true", "True"}:
            return True
        ingredient_text = "、".join([clean_text(ingredient_row.get(field, "")) for field in INGREDIENT_TAG_FIELDS])
        if contains_any(ingredient_text, MILK_RECIPE_KEYWORDS):
            return True
    return False


def detect_caffeine_risk(recipe_row: pd.Series, recipe_meta: dict[str, Any], ingredient_lookup: dict[str, dict[str, Any]]) -> bool:
    recipe_text = "、".join(
        [
            clean_text(recipe_row.get("健康约束", "")),
            clean_text(recipe_row.get("成分组合", "")),
            clean_text(recipe_row.get("推荐解释", "")),
            clean_text(recipe_row.get("成分角色", "")),
            clean_text(recipe_row.get("饮品名称", "")),
        ]
    )
    if contains_any(recipe_text, CAFFEINE_RECIPE_KEYWORDS | STRONG_STIMULUS_KEYWORDS):
        return True
    for ingredient_name in recipe_meta.get("matched_ingredients", []):
        ingredient_row = ingredient_lookup.get(ingredient_name, {})
        caffeine_flag = clean_text(ingredient_row.get("是否含咖啡因", ""))
        if caffeine_flag in {"高", "是", "1", "true", "True"}:
            return True
        ingredient_text = "、".join([clean_text(ingredient_row.get(field, "")) for field in INGREDIENT_TAG_FIELDS])
        if contains_any(ingredient_text, CAFFEINE_RECIPE_KEYWORDS | STRONG_STIMULUS_KEYWORDS):
            return True
    return False


def hard_constraint_filter(user_row: pd.Series, recipe_row: pd.Series, ingredient_info: dict[str, Any]) -> tuple[bool, str]:
    user_text = "、".join(
        clean_text(user_row.get(field, ""))
        for field in ["饮食限制", "身体状态标签", "心情状态标签", "系统解析标签", "时间段"]
        if clean_text(user_row.get(field, ""))
    )
    recipe_meta = ingredient_info.get("recipe_meta", {})
    ingredient_lookup = ingredient_info.get("ingredient_lookup", {})
    reasons: list[str] = []

    if contains_any(user_text, MILK_LIMIT_KEYWORDS) and detect_milk_risk(recipe_row, recipe_meta, ingredient_lookup):
        reasons.append("含乳")
    if contains_any(user_text, CAFFEINE_LIMIT_KEYWORDS) and detect_caffeine_risk(recipe_row, recipe_meta, ingredient_lookup):
        reasons.append("高咖啡因")
    if contains_any(user_text, NIGHT_KEYWORDS) and detect_caffeine_risk(recipe_row, recipe_meta, ingredient_lookup):
        reasons.append("夜间高刺激")

    if reasons:
        return False, normalize_join(dedupe_preserve_order(reasons))
    return True, ""


def compute_rule_scores(user_row: pd.Series, recipe_row: pd.Series, ingredient_info: dict[str, Any]) -> dict[str, Any]:
    user_tags, user_field_tags = build_user_tags(user_row)
    recipe_meta = ingredient_info.get("recipe_meta", {})
    recipe_field_tags = recipe_meta.get("field_tags", {})
    recipe_tags = recipe_meta.get("tags", [])

    user_state_tags = user_field_tags.get("身体状态标签", []) + user_field_tags.get("心情状态标签", []) + user_field_tags.get("体验需求标签", []) + user_field_tags.get("系统解析标签", [])
    recipe_state_tags = recipe_field_tags.get("适配身体状态", []) + recipe_field_tags.get("适配心情状态", []) + recipe_field_tags.get("体验标签", [])
    state_score = min(1.0, 0.45 * overlap_score(user_state_tags, recipe_state_tags) + 0.55 * overlap_score(user_tags, recipe_tags))

    flavor_score = min(1.0, overlap_score(user_field_tags.get("口味偏好", []), recipe_field_tags.get("感官标签", [])))

    user_scene_tags = user_field_tags.get("时间段", []) + user_field_tags.get("地点/场景", []) + user_field_tags.get("系统解析标签", [])
    recipe_scene_tags = recipe_field_tags.get("推荐解释", []) + recipe_field_tags.get("体验标签", []) + recipe_field_tags.get("冷热建议", [])
    scene_score = min(1.0, 0.5 * overlap_score(user_scene_tags, recipe_scene_tags) + 0.5 * overlap_score(user_field_tags.get("冷热偏好", []), recipe_field_tags.get("冷热建议", [])))

    health_score = 1.0
    user_limit_text = normalize_join(split_tags(user_row.get("饮食限制", "")))
    user_body_text = normalize_join(split_tags(user_row.get("身体状态标签", "")))
    recipe_text = normalize_join([recipe_row.get("健康约束", ""), recipe_row.get("甜度建议", ""), recipe_row.get("推荐解释", ""), recipe_row.get("饮品名称", "")])
    if contains_any(user_limit_text, LOW_SUGAR_KEYWORDS) and contains_any(recipe_text, HIGH_SWEET_KEYWORDS):
        health_score -= 0.35
    if contains_any(user_body_text, GASTRIC_SENSITIVE_KEYWORDS) and contains_any(recipe_text, ACID_GAS_KEYWORDS | CAFFEINE_RECIPE_KEYWORDS | STRONG_STIMULUS_KEYWORDS):
        health_score -= 0.35
    if contains_any(user_limit_text + "、" + user_body_text, CAFFEINE_LIMIT_KEYWORDS) and contains_any(recipe_text, CAFFEINE_RECIPE_KEYWORDS | STRONG_STIMULUS_KEYWORDS):
        health_score -= 0.35
    if contains_any(user_limit_text, MILK_LIMIT_KEYWORDS) and contains_any(recipe_text, MILK_RECIPE_KEYWORDS):
        health_score -= 0.35
    if contains_any(normalize_join(user_field_tags.get("时间段", []) + user_field_tags.get("系统解析标签", [])), NIGHT_KEYWORDS):
        if contains_any(recipe_text, CAFFEINE_RECIPE_KEYWORDS | STRONG_STIMULUS_KEYWORDS):
            health_score -= 0.25
        elif contains_any(recipe_text, {"茶", "温热", "低因", "低刺激"}):
            health_score += 0.05
    health_score = max(0.0, min(1.0, health_score))

    visual_score = min(1.0, overlap_score(user_field_tags.get("体验需求标签", []) + user_field_tags.get("心情状态标签", []), recipe_field_tags.get("视觉标签", [])))
    final_rule_score = state_score * 0.30 + flavor_score * 0.20 + scene_score * 0.15 + health_score * 0.25 + visual_score * 0.10

    return {
        "state_score": round(float(state_score), 4),
        "flavor_score": round(float(flavor_score), 4),
        "scene_score": round(float(scene_score), 4),
        "health_score": round(float(health_score), 4),
        "visual_score": round(float(visual_score), 4),
        "final_rule_score": round(float(final_rule_score), 4),
        "user_tags": user_tags,
        "recipe_tags": recipe_tags,
        "user_field_tags": user_field_tags,
        "recipe_field_tags": recipe_field_tags,
    }


def build_training_pairs(user_df: pd.DataFrame, recipe_df: pd.DataFrame, ingredient_lookup: dict[str, dict[str, Any]]) -> tuple[pd.DataFrame, dict[str, list[str]], dict[str, dict[str, Any]], list[str]]:
    recipe_metadata, missing_ingredient_tokens = build_recipe_side_metadata(recipe_df, ingredient_lookup)
    ingredient_info = {"recipe_meta": recipe_metadata, "ingredient_lookup": ingredient_lookup}

    rows: list[dict[str, Any]] = []
    user_tag_cache: dict[str, list[str]] = {}

    for _, user_row in user_df.iterrows():
        session_id = clean_text(user_row.get("session_id", ""))
        if not session_id:
            continue
        user_tags, _ = build_user_tags(user_row)
        user_tag_cache[session_id] = user_tags
        session_rows: list[dict[str, Any]] = []
        for _, recipe_row in recipe_df.iterrows():
            recipe_id = clean_text(recipe_row.get("recipe_id", ""))
            if not recipe_id:
                continue
            recipe_meta = recipe_metadata.get(recipe_id, {"tags": [], "field_tags": {}, "matched_ingredients": [], "missing_ingredients": []})
            score_info = compute_rule_scores(user_row, recipe_row, {"recipe_meta": recipe_meta, "ingredient_lookup": ingredient_lookup})
            passed, reason = hard_constraint_filter(user_row, recipe_row, ingredient_info)
            label = int(passed and score_info["final_rule_score"] >= 0.60)
            row = {
                "session_id": session_id,
                "user_id": clean_text(user_row.get("user_id", "")),
                "recipe_id": recipe_id,
                "饮品名称": clean_text(recipe_row.get("饮品名称", "")),
                "是否通过规则过滤": bool(passed),
                "过滤原因": reason,
                "state_score": score_info["state_score"],
                "flavor_score": score_info["flavor_score"],
                "scene_score": score_info["scene_score"],
                "health_score": score_info["health_score"],
                "visual_score": score_info["visual_score"],
                "final_rule_score": score_info["final_rule_score"],
                "label": label,
                "user_tags": normalize_join(score_info["user_tags"]),
                "recipe_tags": normalize_join(score_info["recipe_tags"]),
            }
            session_rows.append(row)

        passed_rows = [row for row in session_rows if row["是否通过规则过滤"]]
        positive_count = sum(row["label"] for row in session_rows)
        if passed_rows and positive_count < 5:
            promoted_rows = sorted(passed_rows, key=lambda item: item["final_rule_score"], reverse=True)[: min(5, len(passed_rows))]
            promoted_ids = {id(row) for row in promoted_rows}
            for row in session_rows:
                if id(row) in promoted_ids:
                    row["label"] = 1

        rows.extend(session_rows)

    training_df = pd.DataFrame(rows)
    if not training_df.empty:
        training_df = training_df.drop_duplicates(subset=["session_id", "recipe_id"], keep="first").reset_index(drop=True)
    return training_df, user_tag_cache, recipe_metadata, missing_ingredient_tokens


def build_vocab(tag_lists: Iterable[Iterable[str]]) -> tuple[list[str], dict[str, int]]:
    vocab_set: set[str] = set()
    for tags in tag_lists:
        for tag in tags:
            text = clean_text(tag)
            if text:
                vocab_set.add(text)
    if not vocab_set:
        vocab_set.add("__DUMMY__")
    vocab = sorted(vocab_set)
    return vocab, {token: index for index, token in enumerate(vocab)}


def encode_multihot(tags: Iterable[str], token_to_idx: dict[str, int]) -> np.ndarray:
    vector = np.zeros(len(token_to_idx), dtype=np.float32)
    for tag in tags:
        token = clean_text(tag)
        if token in token_to_idx:
            vector[token_to_idx[token]] = 1.0
    return vector


if TORCH_AVAILABLE:

    class TwinTowerNet(nn.Module):
        def __init__(self, input_dim: int):
            super().__init__()
            self.user_tower = nn.Sequential(nn.Linear(input_dim, 128), nn.ReLU(), nn.Dropout(0.2), nn.Linear(128, 64))
            self.recipe_tower = nn.Sequential(nn.Linear(input_dim, 128), nn.ReLU(), nn.Dropout(0.2), nn.Linear(128, 64))

        def forward(self, user_vector: torch.Tensor, recipe_vector: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
            user_embedding = F.normalize(self.user_tower(user_vector), p=2, dim=-1)
            recipe_embedding = F.normalize(self.recipe_tower(recipe_vector), p=2, dim=-1)
            cosine = F.cosine_similarity(user_embedding, recipe_embedding, dim=-1)
            logits = cosine * 5.0
            return logits, user_embedding, recipe_embedding


    class MLPRanker(nn.Module):
        def __init__(self, input_dim: int = 8) -> None:
            super().__init__()
            self.net = nn.Sequential(
                nn.Linear(input_dim, 32),
                nn.ReLU(),
                nn.Dropout(0.1),
                nn.Linear(32, 16),
                nn.ReLU(),
                nn.Linear(16, 1),
                nn.Sigmoid(),
            )

        def forward(self, features: torch.Tensor) -> torch.Tensor:
            return self.net(features).squeeze(-1)

else:

    class TwinTowerNet:
        def __init__(self, input_dim: int):
            rng = np.random.default_rng(RANDOM_SEED)
            self.input_dim = input_dim
            self.user_w1 = rng.normal(0, 0.1, size=(input_dim, 128)).astype(np.float32)
            self.user_w2 = rng.normal(0, 0.1, size=(128, 64)).astype(np.float32)
            self.recipe_w1 = rng.normal(0, 0.1, size=(input_dim, 128)).astype(np.float32)
            self.recipe_w2 = rng.normal(0, 0.1, size=(128, 64)).astype(np.float32)

        def _project(self, vector: np.ndarray, tower: str) -> np.ndarray:
            if tower == "user":
                hidden = np.maximum(vector @ self.user_w1, 0.0)
                embedding = hidden @ self.user_w2
            else:
                hidden = np.maximum(vector @ self.recipe_w1, 0.0)
                embedding = hidden @ self.recipe_w2
            norm = np.linalg.norm(embedding) + 1e-8
            return embedding / norm

        def user_embedding(self, vector: np.ndarray) -> np.ndarray:
            return self._project(vector, "user")

        def recipe_embedding(self, vector: np.ndarray) -> np.ndarray:
            return self._project(vector, "recipe")

        def similarity(self, user_vector: np.ndarray, recipe_vectors: np.ndarray) -> np.ndarray:
            user_embedding = self.user_embedding(user_vector)
            recipe_embeddings = np.array([self.recipe_embedding(row) for row in recipe_vectors], dtype=np.float32)
            return recipe_embeddings @ user_embedding

        def state_dict(self) -> dict[str, Any]:
            return {
                "user_w1": self.user_w1,
                "user_w2": self.user_w2,
                "recipe_w1": self.recipe_w1,
                "recipe_w2": self.recipe_w2,
                "input_dim": self.input_dim,
            }


    class MLPRanker:
        def __init__(self, input_dim: int = 8) -> None:
            self.input_dim = input_dim

        def state_dict(self) -> dict[str, Any]:
            return {"input_dim": self.input_dim, "fallback": True}


def build_ranker_features(
    twin_tower_similarity: float,
    state_score: float,
    flavor_score: float,
    scene_score: float,
    health_score: float,
    visual_score: float,
    makeability_score: float,
    novelty_score: float,
) -> list[float]:
    return [
        float(twin_tower_similarity),
        float(state_score),
        float(flavor_score),
        float(scene_score),
        float(health_score),
        float(visual_score),
        float(makeability_score),
        float(novelty_score),
    ]


def compute_rank_target_score(
    passed: bool,
    twin_tower_similarity: float,
    rule_score: float,
    makeability_score: float,
    novelty_score: float,
    label: int,
) -> tuple[float, float]:
    normalized_twin_similarity = (float(twin_tower_similarity) + 1.0) / 2.0
    normalized_twin_similarity = max(0.0, min(1.0, normalized_twin_similarity))
    if not passed:
        return 0.0, normalized_twin_similarity
    rank_target = (
        normalized_twin_similarity * 0.35
        + float(rule_score) * 0.45
        + float(makeability_score) * 0.10
        + float(novelty_score) * 0.05
        + float(label) * 0.05
    )
    return max(0.0, min(1.0, float(rank_target))), normalized_twin_similarity


def build_ranker_training_data(
    training_df: pd.DataFrame,
    user_df: pd.DataFrame,
    recipe_df: pd.DataFrame,
    ingredient_lookup: dict[str, dict[str, Any]],
    model: Any,
    token_to_idx: dict[str, int],
    recipe_metadata: dict[str, dict[str, Any]],
) -> tuple[pd.DataFrame, dict[str, Any]]:
    if training_df.empty:
        return pd.DataFrame(), {"ranker_train_sample_count": 0}

    recipe_rows = {clean_text(row.get("recipe_id", "")): row for _, row in recipe_df.iterrows()}

    recipe_ids: list[str] = []
    recipe_vectors: list[np.ndarray] = []
    for recipe_id in recipe_rows:
        if not recipe_id:
            continue
        recipe_ids.append(recipe_id)
        recipe_vectors.append(encode_multihot(recipe_metadata.get(recipe_id, {}).get("tags", []), token_to_idx))

    if not recipe_ids:
        return pd.DataFrame(), {"ranker_train_sample_count": 0}

    if TORCH_AVAILABLE and model is not None:
        model.eval()
        with torch.no_grad():
            recipe_tensor = torch.tensor(np.stack(recipe_vectors), dtype=torch.float32)
            recipe_embeddings = F.normalize(model.recipe_tower(recipe_tensor), p=2, dim=-1).cpu().numpy()
    else:
        recipe_embeddings = np.array([model.recipe_embedding(vec) for vec in recipe_vectors], dtype=np.float32)

    recipe_embedding_map = {recipe_id: recipe_embeddings[index] for index, recipe_id in enumerate(recipe_ids)}

    user_embedding_map: dict[str, np.ndarray] = {}
    for _, user_row in user_df.iterrows():
        session_id = clean_text(user_row.get("session_id", ""))
        if not session_id:
            continue
        user_tags, _ = build_user_tags(user_row)
        user_vector = encode_multihot(user_tags, token_to_idx)
        if TORCH_AVAILABLE and model is not None:
            with torch.no_grad():
                user_tensor = torch.tensor(user_vector[None, :], dtype=torch.float32)
                user_embedding = F.normalize(model.user_tower(user_tensor), p=2, dim=-1).squeeze(0).cpu().numpy()
        else:
            user_embedding = model.user_embedding(user_vector.astype(np.float32))
        user_embedding_map[session_id] = user_embedding

    rows: list[dict[str, Any]] = []
    for _, row in training_df.iterrows():
        session_id = clean_text(row.get("session_id", ""))
        recipe_id = clean_text(row.get("recipe_id", ""))
        if not session_id or not recipe_id:
            continue
        user_embedding = user_embedding_map.get(session_id)
        recipe_embedding = recipe_embedding_map.get(recipe_id)
        if user_embedding is None or recipe_embedding is None:
            continue
        similarity = float(np.dot(user_embedding, recipe_embedding))
        recipe_row = recipe_rows.get(recipe_id)
        makeability_score = to_numeric_score(recipe_row.get("可否机器制作", "") if recipe_row is not None else "", default=0.7)

        state_score = float(row.get("state_score", 0.0))
        flavor_score = float(row.get("flavor_score", 0.0))
        scene_score = float(row.get("scene_score", 0.0))
        health_score = float(row.get("health_score", 0.0))
        visual_score = float(row.get("visual_score", 0.0))
        rule_score = float(row.get("final_rule_score", 0.0))

        novelty_base = stable_random_float(session_id, recipe_id)
        novelty_score = 0.5 + 0.5 * novelty_base
        if state_score > 0.45:
            novelty_score -= 0.05
        if flavor_score > 0.35:
            novelty_score -= 0.05
        novelty_score = max(0.5, min(1.0, float(novelty_score)))

        passed = bool(row.get("是否通过规则过滤", False))
        label = int(row.get("label", 0))
        rank_target_score, normalized_twin_similarity = compute_rank_target_score(
            passed,
            similarity,
            rule_score,
            makeability_score,
            novelty_score,
            label,
        )

        rows.append(
            {
                "session_id": session_id,
                "user_id": clean_text(row.get("user_id", "")),
                "recipe_id": recipe_id,
                "饮品名称": clean_text(row.get("饮品名称", "")),
                "twin_tower_similarity": round(float(similarity), 4),
                "normalized_twin_similarity": round(float(normalized_twin_similarity), 4),
                "state_score": round(float(state_score), 4),
                "flavor_score": round(float(flavor_score), 4),
                "scene_score": round(float(scene_score), 4),
                "health_score": round(float(health_score), 4),
                "visual_score": round(float(visual_score), 4),
                "rule_score": round(float(rule_score), 4),
                "makeability_score": round(float(makeability_score), 4),
                "novelty_score": round(float(novelty_score), 4),
                "label": label,
                "rank_target_score": round(float(rank_target_score), 4),
            }
        )

    ranker_df = pd.DataFrame(rows)
    return ranker_df, {"ranker_train_sample_count": int(len(ranker_df))}


def train_mlp_ranker(ranker_df: pd.DataFrame) -> tuple[Any, dict[str, Any]]:
    if not TORCH_AVAILABLE:
        print("torch 未安装，MLP 排序模型将使用基线分数替代。")
        return None, {"ranker_epoch": 0, "ranker_final_loss": None, "ranker_input_dim": 8}

    model = MLPRanker(input_dim=8)
    if ranker_df.empty:
        return model, {"ranker_epoch": 0, "ranker_final_loss": None, "ranker_input_dim": 8}

    feature_cols = [
        "twin_tower_similarity",
        "state_score",
        "flavor_score",
        "scene_score",
        "health_score",
        "visual_score",
        "makeability_score",
        "novelty_score",
    ]
    x = torch.tensor(ranker_df[feature_cols].to_numpy(dtype=np.float32), dtype=torch.float32)
    y = torch.tensor(ranker_df["rank_target_score"].to_numpy(dtype=np.float32), dtype=torch.float32)

    batch_size = max(1, min(32, len(ranker_df)))
    dataset = TensorDataset(x, y)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.MSELoss()
    model.train()
    final_loss = 0.0
    for _epoch in range(80):
        epoch_loss = 0.0
        sample_count = 0
        for batch_x, batch_y in dataloader:
            optimizer.zero_grad()
            preds = model(batch_x)
            loss = criterion(preds, batch_y)
            loss.backward()
            optimizer.step()
            epoch_loss += float(loss.item()) * len(batch_y)
            sample_count += len(batch_y)
        final_loss = epoch_loss / max(sample_count, 1)

    return model, {"ranker_epoch": 80, "ranker_final_loss": round(float(final_loss), 6), "ranker_input_dim": 8}


def predict_mlp_rank_score(model: Any, feature_vector: list[float]) -> float:
    if not TORCH_AVAILABLE or model is None:
        return 0.0
    model.eval()
    with torch.no_grad():
        tensor = torch.tensor([feature_vector], dtype=torch.float32)
        score = model(tensor).squeeze(0).item()
    return float(score)


def compare_baseline_and_mlp(session_candidates: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    top1_changed = 0
    top3_changed = 0
    for session_id, candidates in session_candidates.items():
        if not candidates:
            continue
        baseline_sorted = sorted(candidates, key=lambda item: item.get("baseline_rank_score", 0.0), reverse=True)
        mlp_sorted = sorted(candidates, key=lambda item: item.get("mlp_rank_score", 0.0), reverse=True)
        if baseline_sorted[0].get("recipe_id") != mlp_sorted[0].get("recipe_id"):
            top1_changed += 1
        baseline_top3 = {item.get("recipe_id") for item in baseline_sorted[:3]}
        mlp_top3 = {item.get("recipe_id") for item in mlp_sorted[:3]}
        if baseline_top3 != mlp_top3:
            top3_changed += 1
    return {"top1_changed_sessions": top1_changed, "top3_changed_sessions": top3_changed}


def train_twin_tower(training_df: pd.DataFrame, vocab: list[str], token_to_idx: dict[str, int], user_tag_cache: dict[str, list[str]], recipe_metadata: dict[str, dict[str, Any]]) -> tuple[Any, dict[str, Any]]:
    if not TORCH_AVAILABLE:
        print("torch 未安装，请执行：pip install torch")
        model = TwinTowerNet(len(vocab))
        return model, {"epoch": 0, "final_loss": None, "vocab_size": len(vocab), "embedding_dim": 64}

    model = TwinTowerNet(len(vocab))
    if training_df.empty:
        return model, {"epoch": 0, "final_loss": None, "vocab_size": len(vocab), "embedding_dim": 64}

    user_vectors: list[np.ndarray] = []
    recipe_vectors: list[np.ndarray] = []
    labels: list[float] = []
    for _, row in training_df.iterrows():
        session_id = clean_text(row.get("session_id", ""))
        recipe_id = clean_text(row.get("recipe_id", ""))
        user_vectors.append(encode_multihot(user_tag_cache.get(session_id, []), token_to_idx))
        recipe_vectors.append(encode_multihot(recipe_metadata.get(recipe_id, {}).get("tags", []), token_to_idx))
        labels.append(float(row.get("label", 0)))

    x_user = torch.tensor(np.stack(user_vectors), dtype=torch.float32)
    x_recipe = torch.tensor(np.stack(recipe_vectors), dtype=torch.float32)
    y = torch.tensor(np.array(labels, dtype=np.float32), dtype=torch.float32)
    batch_size = max(1, min(32, len(training_df)))
    dataset = TensorDataset(x_user, x_recipe, y)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.BCEWithLogitsLoss()
    model.train()
    final_loss = 0.0
    for _epoch in range(50):
        epoch_loss = 0.0
        sample_count = 0
        for batch_user, batch_recipe, batch_label in dataloader:
            optimizer.zero_grad()
            logits, _, _ = model(batch_user, batch_recipe)
            loss = criterion(logits, batch_label)
            loss.backward()
            optimizer.step()
            epoch_loss += float(loss.item()) * len(batch_label)
            sample_count += len(batch_label)
        final_loss = epoch_loss / max(sample_count, 1)

    return model, {"epoch": 50, "final_loss": round(float(final_loss), 6), "vocab_size": len(vocab), "embedding_dim": 64}


def build_recommendation_reason(user_row: pd.Series, recipe_row: pd.Series, score_info: dict[str, Any]) -> tuple[str, str]:
    user_state = score_info["user_field_tags"].get("身体状态标签", []) + score_info["user_field_tags"].get("心情状态标签", []) + score_info["user_field_tags"].get("体验需求标签", [])
    recipe_state = score_info["recipe_field_tags"].get("适配身体状态", []) + score_info["recipe_field_tags"].get("适配心情状态", []) + score_info["recipe_field_tags"].get("体验标签", [])
    user_flavor = score_info["user_field_tags"].get("口味偏好", [])
    recipe_flavor = score_info["recipe_field_tags"].get("感官标签", [])
    user_scene = score_info["user_field_tags"].get("时间段", []) + score_info["user_field_tags"].get("地点/场景", []) + score_info["user_field_tags"].get("系统解析标签", [])
    recipe_scene = score_info["recipe_field_tags"].get("推荐解释", []) + score_info["recipe_field_tags"].get("冷热建议", [])
    visual = score_info["recipe_field_tags"].get("视觉标签", [])

    matched_key_tags = dedupe_preserve_order(
        [tag for tag in user_state if tag in recipe_state]
        + [tag for tag in user_flavor if tag in recipe_flavor]
        + [tag for tag in user_scene if tag in recipe_scene]
        + [tag for tag in score_info["user_field_tags"].get("体验需求标签", []) if tag in visual]
    )
    if not matched_key_tags:
        matched_key_tags = dedupe_preserve_order((user_state + user_flavor + user_scene + visual)[:5])

    reason = (
        f"该饮品与用户当前的【{normalize_join(user_state[:3]) or '身体状态/心情状态/体验需求'}】较匹配，"
        f"同时兼顾【{normalize_join(score_info['user_field_tags'].get('饮食限制', [])[:3]) or '饮食限制'}】与【{normalize_join(score_info['user_field_tags'].get('冷热偏好', [])[:3]) or '冷热偏好'}】，"
        f"适合作为当前场景下的个性化饮品推荐。"
    )
    basis = normalize_join(matched_key_tags[:8])
    return reason, basis


def generate_recommendations(
    user_df: pd.DataFrame,
    recipe_df: pd.DataFrame,
    ingredient_lookup: dict[str, dict[str, Any]],
    model: Any,
    token_to_idx: dict[str, int],
    training_summary: dict[str, Any],
    ranker_model: Any,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    recipe_metadata, missing_ingredient_tokens = build_recipe_side_metadata(recipe_df, ingredient_lookup)
    ingredient_info = {"recipe_meta": recipe_metadata, "ingredient_lookup": ingredient_lookup}

    recipe_ids: list[str] = []
    recipe_vectors: list[np.ndarray] = []
    recipe_rows: list[pd.Series] = []
    for _, recipe_row in recipe_df.iterrows():
        recipe_id = clean_text(recipe_row.get("recipe_id", ""))
        if not recipe_id:
            continue
        recipe_ids.append(recipe_id)
        recipe_vectors.append(encode_multihot(recipe_metadata.get(recipe_id, {}).get("tags", []), token_to_idx))
        recipe_rows.append(recipe_row)

    if not recipe_ids:
        empty_metrics = {
            "total_recommendations": 0,
            "sessions_with_top3": 0,
            "average_similarity": 0.0,
            "average_baseline_score": 0.0,
            "average_mlp_score": 0.0,
            "average_final_score": 0.0,
            "pass_filter_count": 0,
            "filtered_candidate_count": 0,
            "fallback_used_count": 0,
            "fallback_session_count": 0,
            "negative_similarity_top3_count": 0,
            "compliance_rate": 0.0,
            "insufficient_sessions": [],
            "baseline_vs_mlp": {"top1_changed_sessions": 0, "top3_changed_sessions": 0},
            "fallback_top3_samples": [],
            "missing_ingredient_tokens": missing_ingredient_tokens,
        }
        return pd.DataFrame(columns=REQUIRED_OUTPUT_COLUMNS), empty_metrics

    if TORCH_AVAILABLE and model is not None:
        model.eval()
        with torch.no_grad():
            recipe_tensor = torch.tensor(np.stack(recipe_vectors), dtype=torch.float32)
            recipe_embeddings = F.normalize(model.recipe_tower(recipe_tensor), p=2, dim=-1)
    else:
        recipe_embeddings = np.stack(recipe_vectors).astype(np.float32)

    records: list[dict[str, Any]] = []
    sessions_with_top3 = 0
    insufficient_sessions: list[str] = []
    pass_filter_count = 0
    filtered_candidate_count = 0
    fallback_used_count = 0
    fallback_session_count = 0
    negative_similarity_top3_count = 0
    fallback_top3_samples: list[str] = []
    session_candidates: dict[str, list[dict[str, Any]]] = {}

    for _, user_row in user_df.iterrows():
        session_id = clean_text(user_row.get("session_id", ""))
        if not session_id:
            continue
        user_tags, _ = build_user_tags(user_row)
        user_vector = encode_multihot(user_tags, token_to_idx)

        if TORCH_AVAILABLE and model is not None:
            with torch.no_grad():
                user_tensor = torch.tensor(user_vector[None, :], dtype=torch.float32)
                user_embedding = F.normalize(model.user_tower(user_tensor), p=2, dim=-1)
                similarities = torch.matmul(user_embedding, recipe_embeddings.T).squeeze(0).cpu().numpy()
        else:
            similarities = model.similarity(user_vector.astype(np.float32), recipe_embeddings)

        candidates: list[dict[str, Any]] = []
        for recipe_index, recipe_row in enumerate(recipe_rows):
            recipe_id = clean_text(recipe_row.get("recipe_id", ""))
            recipe_meta = recipe_metadata.get(recipe_id, {"tags": [], "field_tags": {}, "matched_ingredients": [], "missing_ingredients": []})
            score_info = compute_rule_scores(user_row, recipe_row, {"recipe_meta": recipe_meta, "ingredient_lookup": ingredient_lookup})
            passed, filter_reason = hard_constraint_filter(user_row, recipe_row, ingredient_info)
            if passed:
                pass_filter_count += 1
            else:
                filtered_candidate_count += 1
                continue


            makeability_score = to_numeric_score(recipe_row.get("可否机器制作", ""), default=0.7)
            novelty_base = stable_random_float(session_id, recipe_id)
            novelty_score = 0.5 + 0.5 * novelty_base
            if score_info["state_score"] > 0.45:
                novelty_score -= 0.05
            if score_info["flavor_score"] > 0.35:
                novelty_score -= 0.05
            novelty_score = max(0.5, min(1.0, novelty_score))

            baseline_rank_score = (
                float(similarities[recipe_index]) * 0.50
                + score_info["final_rule_score"] * 0.35
                + makeability_score * 0.10
                + novelty_score * 0.05
            )
            ranker_features = build_ranker_features(
                float(similarities[recipe_index]),
                score_info["state_score"],
                score_info["flavor_score"],
                score_info["scene_score"],
                score_info["health_score"],
                score_info["visual_score"],
                float(makeability_score),
                float(novelty_score),
            )
            mlp_rank_score = predict_mlp_rank_score(ranker_model, ranker_features)
            if not TORCH_AVAILABLE or ranker_model is None:
                mlp_rank_score = float(baseline_rank_score)
            final_rank_score = float(mlp_rank_score)
            reason, basis = build_recommendation_reason(user_row, recipe_row, score_info)
            candidates.append(
                {
                    "session_id": session_id,
                    "user_id": clean_text(user_row.get("user_id", "")),
                    "recipe_id": recipe_id,
                    "饮品名称": clean_text(recipe_row.get("饮品名称", "")),
                    "双塔相似度": round(float(similarities[recipe_index]), 4),
                    "规则综合分": score_info["final_rule_score"],
                    "状态匹配分": score_info["state_score"],
                    "风味偏好分": score_info["flavor_score"],
                    "场景适配分": score_info["scene_score"],
                    "健康约束分": score_info["health_score"],
                    "视觉适配分": score_info["visual_score"],
                    "制作可行性分": round(float(makeability_score), 4),
                    "新颖度分": round(float(novelty_score), 4),
                    "baseline_rank_score": round(float(baseline_rank_score), 4),
                    "mlp_rank_score": round(float(mlp_rank_score), 4),
                    "最终排序分": round(float(final_rank_score), 4),
                    "候选来源": "",
                    "是否通过规则过滤": True,
                    "过滤原因": filter_reason,
                    "推荐理由": reason,
                    "推荐标签依据": basis,
                }
            )

        session_candidates[session_id] = candidates
        primary_candidates = [
            item
            for item in candidates
            if float(item.get("双塔相似度", 0.0)) >= 0.0 or float(item.get("规则综合分", 0.0)) >= 0.50
        ]
        fallback_candidates = [item for item in candidates if item not in primary_candidates]
        primary_candidates = sorted(primary_candidates, key=lambda item: item["最终排序分"], reverse=True)
        fallback_candidates = sorted(fallback_candidates, key=lambda item: item["最终排序分"], reverse=True)

        selected: list[dict[str, Any]] = []
        if len(primary_candidates) >= 3:
            for item in primary_candidates[:3]:
                item["候选来源"] = "主候选"
                selected.append(item)
        else:
            for item in primary_candidates:
                item["候选来源"] = "主候选"
                selected.append(item)
            needed = 3 - len(selected)
            if needed > 0:
                fallback_session_count += 1
                for item in fallback_candidates[:needed]:
                    item["候选来源"] = "兜底补足"
                    selected.append(item)
                    fallback_used_count += 1
                    if len(fallback_top3_samples) < 20:
                        fallback_top3_samples.append(
                            f"{session_id}:{item.get('recipe_id', '')}:{item.get('饮品名称', '')}"
                        )

        if len(selected) >= 3:
            sessions_with_top3 += 1
        else:
            insufficient_sessions.append(session_id)

        for rank, item in enumerate(selected[:3], start=1):
            item["推荐排名"] = rank
            if float(item.get("双塔相似度", 0.0)) < 0.0:
                negative_similarity_top3_count += 1
            records.append(item)

    recommendation_df = pd.DataFrame(records)
    if not recommendation_df.empty:
        recommendation_df = recommendation_df.reset_index(drop=True)
        recommendation_df["recommendation_id"] = [f"REC{index:03d}" for index in range(1, len(recommendation_df) + 1)]
        recommendation_df = recommendation_df[[column for column in REQUIRED_OUTPUT_COLUMNS if column in recommendation_df.columns]]

    metrics = {
        "total_recommendations": int(len(recommendation_df)),
        "sessions_with_top3": int(sessions_with_top3),
        "average_similarity": round(float(recommendation_df["双塔相似度"].mean()), 4) if not recommendation_df.empty else 0.0,
        "average_baseline_score": round(float(recommendation_df["baseline_rank_score"].mean()), 4) if not recommendation_df.empty else 0.0,
        "average_mlp_score": round(float(recommendation_df["mlp_rank_score"].mean()), 4) if not recommendation_df.empty else 0.0,
        "average_final_score": round(float(recommendation_df["最终排序分"].mean()), 4) if not recommendation_df.empty else 0.0,
        "pass_filter_count": int(pass_filter_count),
        "filtered_candidate_count": int(filtered_candidate_count),
        "fallback_used_count": int(fallback_used_count),
        "fallback_session_count": int(fallback_session_count),
        "negative_similarity_top3_count": int(negative_similarity_top3_count),
        "compliance_rate": round(float(pass_filter_count / max(pass_filter_count + filtered_candidate_count, 1)), 4),
        "insufficient_sessions": insufficient_sessions,
        "baseline_vs_mlp": compare_baseline_and_mlp(session_candidates),
        "fallback_top3_samples": fallback_top3_samples,
        "missing_ingredient_tokens": missing_ingredient_tokens,
    }
    return recommendation_df, metrics


def write_vocab_json(vocab: list[str], token_to_idx: dict[str, int]) -> None:
    payload = {"vocab": vocab, "token_to_idx": token_to_idx, "vocab_size": len(vocab)}
    import json

    OUTPUT_VOCAB_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def save_outputs(recommendation_df: pd.DataFrame, training_df: pd.DataFrame, ranker_df: pd.DataFrame, model: Any, ranker_model: Any) -> None:
    import pickle

    recommendation_df.to_csv(OUTPUT_RECOMMENDATION_CSV, index=False, encoding="utf-8-sig")
    training_df.to_csv(OUTPUT_TRAINING_CSV, index=False, encoding="utf-8-sig")
    ranker_df.to_csv(OUTPUT_RANKER_TRAINING_CSV, index=False, encoding="utf-8-sig")
    with pd.ExcelWriter(OUTPUT_RECOMMENDATION_XLSX, engine="openpyxl") as writer:
        recommendation_df.to_excel(writer, sheet_name="推荐记录表", index=False)
        training_df.to_excel(writer, sheet_name="双塔训练样本", index=False)
        ranker_df.to_excel(writer, sheet_name="MLP排序训练样本", index=False)
    if TORCH_AVAILABLE and model is not None:
        torch.save(model.state_dict(), OUTPUT_MODEL_PT)
    elif model is not None:
        with OUTPUT_MODEL_PT.open("wb") as file_handle:
            pickle.dump(model.state_dict(), file_handle)
    else:
        OUTPUT_MODEL_PT.write_text("torch 未安装，未生成可训练模型。", encoding="utf-8")

    if TORCH_AVAILABLE and ranker_model is not None:
        torch.save(ranker_model.state_dict(), OUTPUT_RANKER_MODEL_PT)
    elif ranker_model is not None:
        with OUTPUT_RANKER_MODEL_PT.open("wb") as file_handle:
            pickle.dump(ranker_model.state_dict(), file_handle)
    else:
        OUTPUT_RANKER_MODEL_PT.write_text("torch 未安装，未生成可训练模型。", encoding="utf-8")


def write_mlp_report(
    report_path: Path,
    user_df: pd.DataFrame,
    recipe_df: pd.DataFrame,
    training_df: pd.DataFrame,
    ranker_df: pd.DataFrame,
    recommendation_df: pd.DataFrame,
    training_summary: dict[str, Any],
    ranker_summary: dict[str, Any],
    recommendation_metrics: dict[str, Any],
    missing_fields: dict[str, list[str]],
    missing_ingredient_tokens: list[str],
) -> None:
    lines: list[str] = []
    lines.append("双塔_MLP排序评估报告")
    lines.append("")
    lines.append("1. 数据规模")
    lines.append(f"- 用户输入数：{len(user_df)}")
    lines.append(f"- 饮品方案数：{len(recipe_df)}")
    lines.append(f"- 双塔训练样本数：{len(training_df)}")
    lines.append(f"- MLP 排序训练样本数：{len(ranker_df)}")
    lines.append(f"- 正样本数：{int(training_df['label'].sum()) if not training_df.empty and 'label' in training_df.columns else 0}")
    lines.append(f"- 负样本数：{int(len(training_df) - training_df['label'].sum()) if not training_df.empty and 'label' in training_df.columns else 0}")
    lines.append("")
    lines.append("2. 双塔模型训练结果")
    lines.append(f"- epoch：{training_summary.get('epoch', 0)}")
    lines.append(f"- final_loss：{training_summary.get('final_loss', 'N/A')}")
    lines.append(f"- vocab_size：{training_summary.get('vocab_size', 0)}")
    lines.append(f"- embedding_dim：{training_summary.get('embedding_dim', 64)}")
    lines.append("")
    lines.append("3. MLP 排序模型训练结果")
    lines.append(f"- ranker_epoch：{ranker_summary.get('ranker_epoch', 0)}")
    lines.append(f"- ranker_final_loss：{ranker_summary.get('ranker_final_loss', 'N/A')}")
    lines.append(f"- ranker_input_dim：{ranker_summary.get('ranker_input_dim', 8)}")
    lines.append(f"- ranker_train_sample_count：{ranker_summary.get('ranker_train_sample_count', len(ranker_df))}")
    lines.append("- 当前 MLP 排序模型使用双塔相似度、规则综合分、制作可行性、新颖度和弱监督标签共同构造排序目标，后续可替换为真实用户反馈得分。")
    lines.append("")
    lines.append("4. 推荐结果")
    lines.append(f"- 推荐记录总数：{len(recommendation_df)}")
    lines.append(f"- 每个 session 是否都有 Top3：{'是' if not recommendation_metrics.get('insufficient_sessions') else '否'}")
    lines.append(f"- 平均双塔相似度：{recommendation_metrics.get('average_similarity', 0.0)}")
    lines.append(f"- 平均 baseline_rank_score：{recommendation_metrics.get('average_baseline_score', 0.0)}")
    lines.append(f"- 平均 mlp_rank_score：{recommendation_metrics.get('average_mlp_score', 0.0)}")
    lines.append(f"- 平均最终排序分：{recommendation_metrics.get('average_final_score', 0.0)}")
    lines.append(f"- 使用兜底补足的推荐数量：{recommendation_metrics.get('fallback_used_count', 0)}")
    lines.append(f"- 使用兜底补足的 session 数量：{recommendation_metrics.get('fallback_session_count', 0)}")
    lines.append(f"- Top3 中双塔相似度为负的推荐数量：{recommendation_metrics.get('negative_similarity_top3_count', 0)}")
    fallback_samples = recommendation_metrics.get("fallback_top3_samples", [])
    if fallback_samples:
        lines.append(f"- Top3 中候选来源为“兜底补足”的推荐清单（最多20条）：{normalize_join(fallback_samples)}")
    direction_match_count = 0
    direction_total = 0
    if not recommendation_df.empty and "session_id" in recommendation_df.columns and "推荐标签依据" in recommendation_df.columns:
        for session_id in recommendation_df["session_id"].unique().tolist():
            user_rows = user_df[user_df["session_id"] == session_id]
            if user_rows.empty:
                continue
            direction_tags = split_tags(user_rows.iloc[0].get("推荐方向", ""))
            if not direction_tags:
                continue
            top1_row = recommendation_df[recommendation_df["session_id"] == session_id].sort_values("推荐排名").head(1)
            if top1_row.empty:
                continue
            direction_total += 1
            basis_tags = split_tags(top1_row.iloc[0].get("推荐标签依据", ""))
            if set(direction_tags) & set(basis_tags):
                direction_match_count += 1
    if direction_total > 0:
        lines.append(f"- 推荐方向一致性参考检查：{direction_match_count}/{direction_total}")
    lines.append("")
    lines.append("5. 约束合规")
    lines.append(f"- 总推荐数：{len(recommendation_df)}")
    lines.append(f"- 通过规则过滤的候选数：{recommendation_metrics.get('pass_filter_count', 0)}")
    lines.append(f"- 被过滤候选数量：{recommendation_metrics.get('filtered_candidate_count', 0)}")
    lines.append(f"- 约束合规率：{recommendation_metrics.get('compliance_rate', 0.0)}")
    lines.append("")
    lines.append("6. baseline 与 MLP 排序对比")
    baseline_vs_mlp = recommendation_metrics.get("baseline_vs_mlp", {})
    lines.append(f"- Top1 是否变化的 session 数量：{baseline_vs_mlp.get('top1_changed_sessions', 0)}")
    lines.append(f"- Top3 集合是否变化的 session 数量：{baseline_vs_mlp.get('top3_changed_sessions', 0)}")
    lines.append(f"- baseline 平均排序分：{recommendation_metrics.get('average_baseline_score', 0.0)}")
    lines.append(f"- MLP 平均排序分：{recommendation_metrics.get('average_mlp_score', 0.0)}")
    lines.append("")
    lines.append("7. 样例展示")
    sample_sessions = list(dict.fromkeys(recommendation_df["session_id"].tolist()))[:3] if not recommendation_df.empty and "session_id" in recommendation_df.columns else []
    if not sample_sessions:
        lines.append("- 暂无可展示的 session。")
    else:
        for session_id in sample_sessions:
            session_rows = recommendation_df[recommendation_df["session_id"] == session_id].sort_values("推荐排名")
            user_label = ""
            recommend_direction = ""
            if not user_df.empty and "session_id" in user_df.columns:
                match_row = user_df[user_df["session_id"] == session_id]
                if not match_row.empty:
                    user_label = normalize_join(split_tags(match_row.iloc[0].get("系统解析标签", ""))[:4])
                    recommend_direction = normalize_join(split_tags(match_row.iloc[0].get("推荐方向", ""))[:4])
            lines.append(f"- session_id：{session_id}")
            lines.append(f"  - 用户标签：{user_label or '无'}")
            if recommend_direction:
                lines.append(f"  - 推荐方向（参考）：{recommend_direction}")
            for _, row in session_rows.iterrows():
                lines.append(
                    "  - 推荐饮品：{name} | 双塔相似度：{sim} | 规则综合分：{rule} | baseline_rank_score：{base} | mlp_rank_score：{mlp} | 推荐理由：{reason}".format(
                        name=row.get("饮品名称", ""),
                        sim=row.get("双塔相似度", ""),
                        rule=row.get("规则综合分", ""),
                        base=row.get("baseline_rank_score", ""),
                        mlp=row.get("mlp_rank_score", ""),
                        reason=row.get("推荐理由", ""),
                    )
                )
    lines.append("")
    lines.append("8. 问题提醒")
    if recommendation_metrics.get("insufficient_sessions"):
        lines.append(f"- 以下 session 未达到 Top3：{normalize_join(recommendation_metrics.get('insufficient_sessions', []))}")
    else:
        lines.append("- 所有 session 均已输出 Top3。")
    if missing_ingredient_tokens:
        lines.append(f"- 成分组合中未匹配到成分表的条目：{normalize_join(missing_ingredient_tokens[:50])}")
    else:
        lines.append("- 未发现成分组合匹配缺失。")
    if not recommendation_df.empty and float(recommendation_df["视觉适配分"].mean()) == 0.0:
        lines.append("- 视觉标签映射表尚未正式接入，当前视觉分为预留特征。")
    for name, fields in missing_fields.items():
        if fields:
            lines.append(f"- {name} 缺失字段：{normalize_join(fields)}")
    lines.append("")
    lines.append("9. 备注")
    lines.append("- 当前 MLP 排序模型使用双塔相似度、规则综合分、制作可行性、新颖度和弱监督标签共同构造排序目标，后续可替换为真实用户反馈得分。")
    report_path.write_text("\n".join(lines), encoding="utf-8")


def prepare_tables() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, dict[str, list[str]]]:
    label_df = drop_empty_rows_cols(read_csv_auto(INPUT_FILES["标签字典表"]))
    ingredient_df = drop_empty_rows_cols(read_csv_auto(INPUT_FILES["饮品成分表"]))
    recipe_df = drop_empty_rows_cols(read_csv_auto(INPUT_FILES["饮品方案表"]))
    user_df = drop_empty_rows_cols(read_csv_auto(INPUT_FILES["用户输入表"]))

    user_aliases = {
        "session_id": ["session_id"],
        "user_id": ["user_id"],
        "时间段": ["时间段", "时段", "时间"],
        "地点/场景": ["地点/场景", "地点场景", "场景", "地点"],
        "身体状态标签": ["身体状态标签"],
        "心情状态标签": ["心情状态标签"],
        "体验需求标签": ["体验需求标签"],
        "口味偏好": ["口味偏好"],
        "冷热偏好": ["冷热偏好"],
        "饮食限制": ["饮食限制"],
        "地区标签": ["地区标签"],
        "兴趣标签": ["兴趣标签"],
        "系统解析标签": ["系统解析标签"],
        "推荐方向": ["推荐方向"],
    }
    recipe_aliases = {
        "recipe_id": ["recipe_id"],
        "饮品名称": ["饮品名称"],
        "成分组合": ["成分组合"],
        "成分角色": ["成分角色"],
        "用量等级": ["用量等级"],
        "适配身体状态": ["适配身体状态", "适用身体状态", "对应身体状态"],
        "适配心情状态": ["适配心情状态", "适用心情状态", "对应心情状态"],
        "感官标签": ["感官标签"],
        "体验标签": ["体验标签"],
        "健康约束": ["健康约束"],
        "甜度建议": ["甜度建议"],
        "冷热建议": ["冷热建议"],
        "推荐解释": ["推荐解释"],
        "视觉标签": ["视觉标签"],
        "可否机器制作": ["可否机器制作"],
    }
    ingredient_aliases = {
        "ingredient_id": ["ingredient_id"],
        "成分名称": ["成分名称"],
        "成分类别": ["成分类别"],
        "成分角色": ["成分角色"],
        "是否含咖啡因": ["是否含咖啡因"],
        "是否含乳": ["是否含乳"],
        "感官标签": ["感官标签"],
        "状态/体验标签": ["状态/体验标签"],
        "健康约束": ["健康约束"],
        "视觉标签": ["视觉标签"],
    }

    user_df = normalize_columns(user_df, user_aliases)
    recipe_df = normalize_columns(recipe_df, recipe_aliases)
    ingredient_df = normalize_columns(ingredient_df, ingredient_aliases)

    missing_fields = {
        "标签字典表": discover_missing_fields(label_df, ["标签分类", "tag_id", "标签名", "含义", "适用表/字段", "推荐使用建议", "同义词/避免写法"]),
        "饮品成分表": discover_missing_fields(ingredient_df, ["ingredient_id", "成分名称", "成分类别", "成分角色", "是否含咖啡因", "是否含乳", "感官标签", "状态/体验标签", "健康约束", "视觉标签"]),
        "饮品方案表": discover_missing_fields(recipe_df, ["recipe_id", "饮品名称", "成分组合", "成分角色", "用量等级", "适配身体状态", "适配心情状态", "感官标签", "体验标签", "健康约束", "甜度建议", "冷热建议", "推荐解释", "视觉标签", "可否机器制作"]),
        "用户输入表": discover_missing_fields(user_df, ["session_id", "user_id", "时间段", "地点/场景", "身体状态标签", "心情状态标签", "体验需求标签", "口味偏好", "冷热偏好", "饮食限制", "地区标签", "兴趣标签", "系统解析标签", "推荐方向"]),
    }
    return label_df, ingredient_df, recipe_df, user_df, missing_fields


def build_user_row_from_payload(payload: dict[str, list[str]], session_id: str = "API_SESSION", user_id: str = "API_USER") -> pd.Series:
    def to_joined(values: Iterable[str]) -> str:
        return normalize_join(dedupe_preserve_order(values))

    return pd.Series(
        {
            "session_id": session_id,
            "user_id": user_id,
            "时间段": "",
            "地点/场景": to_joined(payload.get("scene", [])),
            "身体状态标签": to_joined(payload.get("body", [])),
            "心情状态标签": to_joined(payload.get("mood", [])),
            "体验需求标签": to_joined(payload.get("needs", [])),
            "口味偏好": to_joined(payload.get("flavor_preference", [])),
            "冷热偏好": to_joined(payload.get("temperature_preference", [])),
            "饮食限制": to_joined(payload.get("limits", [])),
            "地区标签": "",
            "兴趣标签": "",
            "系统解析标签": "",
        }
    )


def recommend_for_user_input(
    payload: dict[str, list[str]],
    recipe_df: pd.DataFrame,
    ingredient_lookup: dict[str, dict[str, Any]],
    model: Any,
    token_to_idx: dict[str, int],
    ranker_model: Any,
    recipe_metadata: dict[str, dict[str, Any]] | None = None,
    recipe_vectors: list[np.ndarray] | None = None,
    recipe_rows: list[pd.Series] | None = None,
    recipe_embeddings: np.ndarray | None = None,
    top_k: int = 3,
) -> list[dict[str, Any]]:
    if recipe_metadata is None:
        recipe_metadata, _missing = build_recipe_side_metadata(recipe_df, ingredient_lookup)
    ingredient_info = {"recipe_meta": recipe_metadata, "ingredient_lookup": ingredient_lookup}

    if recipe_rows is None:
        recipe_rows = [row for _, row in recipe_df.iterrows()]

    if recipe_vectors is None:
        recipe_vectors = [encode_multihot(recipe_metadata.get(clean_text(row.get("recipe_id", "")), {}).get("tags", []), token_to_idx) for row in recipe_rows]

    if recipe_embeddings is None:
        if TORCH_AVAILABLE and model is not None:
            model.eval()
            with torch.no_grad():
                recipe_tensor = torch.tensor(np.stack(recipe_vectors), dtype=torch.float32)
                recipe_embeddings = F.normalize(model.recipe_tower(recipe_tensor), p=2, dim=-1).cpu().numpy()
        else:
            recipe_embeddings = np.stack(recipe_vectors).astype(np.float32)

    user_row = build_user_row_from_payload(payload)
    user_tags, _ = build_user_tags(user_row)
    user_vector = encode_multihot(user_tags, token_to_idx)

    if TORCH_AVAILABLE and model is not None:
        with torch.no_grad():
            user_tensor = torch.tensor(user_vector[None, :], dtype=torch.float32)
            user_embedding = F.normalize(model.user_tower(user_tensor), p=2, dim=-1).cpu().numpy()
        similarities = (user_embedding @ recipe_embeddings.T).squeeze(0)
    elif model is not None and hasattr(model, "similarity"):
        similarities = model.similarity(user_vector.astype(np.float32), recipe_embeddings)
    else:
        similarities = recipe_embeddings @ user_vector.astype(np.float32)

    candidates: list[dict[str, Any]] = []
    for index, recipe_row in enumerate(recipe_rows):
        recipe_id = clean_text(recipe_row.get("recipe_id", ""))
        if not recipe_id:
            continue
        recipe_meta = recipe_metadata.get(recipe_id, {"tags": [], "field_tags": {}, "matched_ingredients": [], "missing_ingredients": []})
        score_info = compute_rule_scores(user_row, recipe_row, {"recipe_meta": recipe_meta, "ingredient_lookup": ingredient_lookup})
        passed, filter_reason = hard_constraint_filter(user_row, recipe_row, ingredient_info)
        if not passed:
            continue

        makeability_score = to_numeric_score(recipe_row.get("可否机器制作", ""), default=0.7)
        novelty_base = stable_random_float(clean_text(user_row.get("session_id", "API_SESSION")), recipe_id)
        novelty_score = 0.5 + 0.5 * novelty_base
        if score_info["state_score"] > 0.45:
            novelty_score -= 0.05
        if score_info["flavor_score"] > 0.35:
            novelty_score -= 0.05
        novelty_score = max(0.5, min(1.0, float(novelty_score)))

        similarity_value = float(similarities[index])
        baseline_rank_score = similarity_value * 0.50 + score_info["final_rule_score"] * 0.35 + makeability_score * 0.10 + novelty_score * 0.05
        ranker_features = build_ranker_features(
            similarity_value,
            score_info["state_score"],
            score_info["flavor_score"],
            score_info["scene_score"],
            score_info["health_score"],
            score_info["visual_score"],
            float(makeability_score),
            float(novelty_score),
        )
        mlp_rank_score = predict_mlp_rank_score(ranker_model, ranker_features)
        if not TORCH_AVAILABLE or ranker_model is None:
            mlp_rank_score = float(baseline_rank_score)
        final_rank_score = float(mlp_rank_score)

        reason, basis = build_recommendation_reason(user_row, recipe_row, score_info)
        composition_tokens = parse_composition_tokens(recipe_row.get("成分组合", ""))
        visual_tags = recipe_meta.get("field_tags", {}).get("视觉标签", [])
        visual_mapping = [{"tag": tag, "visual": tag} for tag in visual_tags[:4]]

        candidates.append(
            {
                "recipe_id": recipe_id,
                "drink_name": clean_text(recipe_row.get("饮品名称", "")),
                "twin_tower_similarity": round(similarity_value, 4),
                "rule_score": round(float(score_info["final_rule_score"]), 4),
                "state_score": score_info["state_score"],
                "flavor_score": score_info["flavor_score"],
                "scene_score": score_info["scene_score"],
                "health_score": score_info["health_score"],
                "visual_score": score_info["visual_score"],
                "baseline_rank_score": round(float(baseline_rank_score), 4),
                "mlp_rank_score": round(float(mlp_rank_score), 4),
                "final_score": round(float(final_rank_score), 4),
                "candidate_source": "主候选",
                "reason": reason,
                "matched_tags": split_tags(basis),
                "tags": recipe_meta.get("tags", [])[:8],
                "ingredients": {
                    "base": composition_tokens[0] if composition_tokens else "",
                    "flavor": composition_tokens[1] if len(composition_tokens) > 1 else "",
                    "sweetness": clean_text(recipe_row.get("甜度建议", "")),
                    "texture": clean_text(recipe_row.get("用量等级", "")),
                    "decoration": clean_text(recipe_row.get("成分角色", "")),
                },
                "steps": [
                    "选择基础茶/果底",
                    "加入风味成分",
                    "调整甜度与冷热",
                    "生成专属杯身图案",
                ],
                "visual_mapping": visual_mapping,
                "filter_reason": filter_reason,
            }
        )

    candidates = sorted(candidates, key=lambda item: item.get("final_score", 0.0), reverse=True)
    top_candidates = candidates[: max(1, top_k)]
    for idx, item in enumerate(top_candidates, start=1):
        item["rank"] = idx
        item["recommendation_id"] = f"API_REC{idx:03d}"

    return top_candidates


def main() -> None:
    seed_everything(RANDOM_SEED)
    try:
        label_df, ingredient_df, recipe_df, user_df, missing_fields = prepare_tables()
        ingredient_lookup = build_ingredient_lookup(ingredient_df)
        training_df, user_tag_cache, recipe_metadata, missing_ingredient_tokens = build_training_pairs(user_df, recipe_df, ingredient_lookup)

        vocab_sources: list[list[str]] = []
        if not training_df.empty and "user_tags" in training_df.columns:
            vocab_sources.extend(training_df["user_tags"].map(split_tags).tolist())
        if not training_df.empty and "recipe_tags" in training_df.columns:
            vocab_sources.extend(training_df["recipe_tags"].map(split_tags).tolist())
        vocab, token_to_idx = build_vocab(vocab_sources)
        write_vocab_json(vocab, token_to_idx)

        model, training_summary = train_twin_tower(training_df, vocab, token_to_idx, user_tag_cache, recipe_metadata)
        ranker_df, ranker_data_summary = build_ranker_training_data(
            training_df,
            user_df,
            recipe_df,
            ingredient_lookup,
            model,
            token_to_idx,
            recipe_metadata,
        )
        ranker_model, ranker_summary = train_mlp_ranker(ranker_df)
        ranker_summary.update(ranker_data_summary)

        recommendation_df, recommendation_metrics = generate_recommendations(
            user_df,
            recipe_df,
            ingredient_lookup,
            model,
            token_to_idx,
            training_summary,
            ranker_model,
        )

        save_outputs(recommendation_df, training_df, ranker_df, model, ranker_model)
        write_mlp_report(
            OUTPUT_REPORT_TXT,
            user_df,
            recipe_df,
            training_df,
            ranker_df,
            recommendation_df,
            training_summary,
            ranker_summary,
            recommendation_metrics,
            missing_fields,
            missing_ingredient_tokens,
        )

        print("Top3 补足机制已完成：所有 session 均输出 Top3，并保留主候选/兜底补足标记。")
    except Exception as exc:
        print(f"运行失败：{exc}")
        if not TORCH_AVAILABLE:
            print("torch 未安装，请执行：pip install torch")
        sys.exit(1)


if __name__ == "__main__":
    main()