from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent
INPUT_FILES = {
    '标签字典表': ROOT / '标签字典表_终版.csv',
    '饮品成分表': ROOT / '饮品成分表_终版.csv',
    '饮品方案表': ROOT / '饮品方案表_终版.csv',
    '用户输入表': ROOT / '用户输入表_终版.csv',
}
OUTPUT_FILES = {
    '标签字典表': ROOT / '标签字典表_最终检查版.csv',
    '饮品成分表': ROOT / '饮品成分表_最终检查版.csv',
    '饮品方案表': ROOT / '饮品方案表_最终检查版.csv',
    '用户输入表': ROOT / '用户输入表_最终检查版.csv',
}

CSV_ENCODINGS = ('utf-8-sig', 'utf-8', 'gbk')
LIST_SPLIT_RE = re.compile(r'[、,，;/；|\n]+')


SCHEME_INGREDIENT_REPLACEMENTS = {
    '薄荷': '薄荷叶',
    '奶油': '淡奶油',
    '乳酸菌饮料': '乳酸菌饮品',
}

SCHEME_EXACT_TOKEN_REPLACEMENTS = {
    '夜间降低茶基': '夜间慎用',
    '气泡': '气泡元素',
}

LABEL_DICT_REPLACEMENT = {
    '具体疗效或医疗化表达疲劳、恢复体力': '恢复体力等具体疗效',
}

USER_INPUT_REPLACEMENTS = {
    '加班后疲惫': '疲惫',
    '社交后疲惫': '疲惫',
    '久坐疲惫': '疲惫',
    '用脑疲惫': '疲惫',
    '午后犯困': '困倦',
    '起床困难': '困倦',
    '需要轻补充': '轻补充',
    '想恢复': '轻补充',
    '想专注': '专注',
    '想低刺激': '低刺激',
    '想陪伴': '陪伴',
    '想清醒': '提神',
    '想舒缓': '放松',
    '想解渴': '清爽',
    '开心': '想满足',
    '兴奋': '想释放',
}


def clean_cell(value: object) -> str:
    if value is None:
        return ''
    return str(value).replace('\u3000', ' ').strip()


def read_csv_fallback(path: Path) -> pd.DataFrame:
    last_error: Exception | None = None
    for encoding in CSV_ENCODINGS:
        try:
            return pd.read_csv(path, dtype=str, keep_default_na=False, encoding=encoding, engine='python')
        except Exception as exc:  # pragma: no cover - fallback path
            last_error = exc
    raise last_error  # type: ignore[misc]


def trim_empty(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    df = df.apply(lambda col: col.map(clean_cell))
    non_empty_cols = [col for col in df.columns if not df[col].eq('').all()]
    df = df[non_empty_cols].copy()
    non_empty_rows = ~df.eq('').all(axis=1)
    return df.loc[non_empty_rows].reset_index(drop=True)


def replace_text(text: object, replacements: dict[str, str], stats: Counter[str]) -> str:
    value = clean_cell(text)
    if not value:
        return ''
    for old, new in replacements.items():
        count = value.count(old)
        if count:
            stats[old] += count
            value = value.replace(old, new)
    return re.sub(r'\s+', ' ', value).strip()


def replace_scheme_component_text(text: object, stats: Counter[str]) -> str:
    value = clean_cell(text)
    if not value:
        return ''
    tokens = []
    for token in LIST_SPLIT_RE.split(value):
        token = token.strip()
        if not token:
            continue
        if '-' in token:
            left, right = token.split('-', 1)
            new_left = SCHEME_INGREDIENT_REPLACEMENTS.get(left, left)
            if new_left != left:
                stats[left] += 1
            token = f'{new_left}-{right}'
        else:
            new_token = SCHEME_INGREDIENT_REPLACEMENTS.get(token, token)
            if new_token != token:
                stats[token] += 1
            token = new_token
        tokens.append(token)
    result = []
    for token in tokens:
        if token not in result:
            result.append(token)
    return '、'.join(result)


def replace_scheme_exact_tokens(text: object, stats: Counter[str]) -> str:
    value = clean_cell(text)
    if not value:
        return ''
    tokens = []
    for token in LIST_SPLIT_RE.split(value):
        token = token.strip()
        if not token:
            continue
        new_token = SCHEME_EXACT_TOKEN_REPLACEMENTS.get(token, token)
        if new_token != token:
            stats[token] += 1
        tokens.append(new_token)
    result = []
    for token in tokens:
        if token not in result:
            result.append(token)
    return '、'.join(result)


def normalize_list_value(text: object, replacements: dict[str, str], stats: Counter[str]) -> str:
    value = clean_cell(text)
    if not value:
        return ''
    tokens = []
    for token in LIST_SPLIT_RE.split(value):
        token = token.strip()
        if not token:
            continue
        token = replacements.get(token, token)
        tokens.append(token)
    result = []
    for token in tokens:
        if token not in result:
            result.append(token)
    return '、'.join(result)


def normalize_scheme_table(df: pd.DataFrame) -> tuple[pd.DataFrame, Counter[str]]:
    df = trim_empty(df)
    stats = Counter()
    for column in ['成分组合', '成分角色', '用量等级']:
        if column in df.columns:
            df[column] = df[column].map(lambda value: replace_scheme_component_text(value, stats))
    for column in ['健康约束', '视觉标签']:
        if column in df.columns:
            df[column] = df[column].map(lambda value: replace_scheme_exact_tokens(value, stats))
    return df, stats


def normalize_user_table(df: pd.DataFrame) -> pd.DataFrame:
    df = trim_empty(df)
    target_columns = ['身体状态标签', '心情状态标签', '体验需求标签']
    for column in target_columns:
        if column not in df.columns:
            continue
        df[column] = df[column].map(lambda value: normalize_list_value(value, USER_INPUT_REPLACEMENTS, Counter()))
    return df


def normalize_label_dict(df: pd.DataFrame) -> pd.DataFrame:
    df = trim_empty(df)
    stats = Counter()
    for column in df.columns:
        df[column] = df[column].map(lambda value: replace_text(value, LABEL_DICT_REPLACEMENT, stats))
    return df


def ingredient_names_from_df(df: pd.DataFrame) -> set[str]:
    if '成分名称' not in df.columns:
        return set()
    return set(df['成分名称'].map(clean_cell).tolist())


def parse_tokens(text: object) -> list[str]:
    value = clean_cell(text)
    if not value:
        return []
    return [token.strip() for token in LIST_SPLIT_RE.split(value) if token.strip()]


def print_table_size(name: str, df: pd.DataFrame) -> None:
    print(f'{name}：行数 {len(df)}，列数 {len(df.columns)}')


def main() -> None:
    label_df = normalize_label_dict(read_csv_fallback(INPUT_FILES['标签字典表']))
    ingredient_df = trim_empty(read_csv_fallback(INPUT_FILES['饮品成分表']))
    scheme_df, scheme_stats = normalize_scheme_table(read_csv_fallback(INPUT_FILES['饮品方案表']))
    user_df = normalize_user_table(read_csv_fallback(INPUT_FILES['用户输入表']))

    for name, df in {
        '标签字典表': label_df,
        '饮品成分表': ingredient_df,
        '饮品方案表': scheme_df,
        '用户输入表': user_df,
    }.items():
        df.to_csv(OUTPUT_FILES[name], index=False, encoding='utf-8-sig')

    ingredient_names = ingredient_names_from_df(ingredient_df)
    scheme_missing = []
    if '成分组合' in scheme_df.columns:
        for value in scheme_df['成分组合']:
            for token in parse_tokens(value):
                if token not in ingredient_names:
                    scheme_missing.append(token)
    scheme_missing = sorted(set(scheme_missing))

    label_names = set(label_df['标签名'].map(clean_cell).tolist()) if '标签名' in label_df.columns else set()
    user_check_columns = ['身体状态标签', '心情状态标签', '体验需求标签']
    user_unknown = []
    for column in user_check_columns:
        if column not in user_df.columns:
            continue
        for value in user_df[column]:
            for token in parse_tokens(value):
                if token not in label_names:
                    user_unknown.append(token)
    user_unknown = sorted(set(user_unknown))

    print_table_size('标签字典表', label_df)
    print_table_size('饮品成分表', ingredient_df)
    print_table_size('饮品方案表', scheme_df)
    print_table_size('用户输入表', user_df)
    print('检查结果：')
    print(f'饮品方案表成分组合缺失项：{scheme_missing if scheme_missing else "无"}')
    print(f'用户输入表身体状态/心情状态/体验需求标签的非字典词：{user_unknown if user_unknown else "无"}')
    print(f'饮品方案表替换统计：{dict(scheme_stats) if scheme_stats else "无"}')
    print('清洗完成，已生成四张最终检查版 CSV。')


if __name__ == '__main__':
    main()