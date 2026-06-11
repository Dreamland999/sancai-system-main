from __future__ import annotations

from collections import Counter, defaultdict
import csv
import re
from pathlib import Path
from typing import Iterable

import pandas as pd


ROOT = Path(__file__).resolve().parent
INPUT_FILES = {
    '标签字典表': ROOT / '数据 - 标签字典表.csv',
    '饮品成分表': ROOT / '数据 - 饮品成分表_清洗版.csv',
    '饮品方案表': ROOT / '数据 - 饮品方案表.csv',
    '用户输入表': ROOT / '数据 - 用户输入表.csv',
}
OUTPUT_FILES = {
    '标签字典表': ROOT / '标签字典表_终版.csv',
    '饮品成分表': ROOT / '饮品成分表_终版.csv',
    '饮品方案表': ROOT / '饮品方案表_终版.csv',
    '用户输入表': ROOT / '用户输入表_终版.csv',
}
OUTPUT_XLSX = ROOT / '数据_四表清洗终版.xlsx'
REPORT_TXT = ROOT / '数据清洗检查报告.txt'

CSV_ENCODINGS = ('utf-8-sig', 'utf-8', 'gbk')
ALLOWED_ROLE_TOKENS = ['基底', '风味', '甜度', '口感', '装饰', '辅助']

LABEL_DICT_FINAL_COLUMNS = ['标签分类', 'tag_id', '标签名', '含义', '适用表/字段', '推荐使用建议', '同义词/避免写法']
INGREDIENT_ROLE_COLUMNS = ['ingredient_id', '成分名称', '成分类别', '成分角色', '基础属性', '是否含咖啡因', '是否含乳', '感官标签', '状态/体验标签', '适合状态', '不适合状态', '健康约束', '适合场景', '视觉标签', '标签来源建议', '备注']
SCHEME_EXPLANATORY_COLUMN = '字段'
SCHEME_RECIPE_ID_COL = 'recipe_id'


LABEL_TEXT_REPLACEMENTS = {
    '治疗': '具体疗效或医疗化表达',
    '治愈': '具体疗效或医疗化表达',
    '疗愈': '具体疗效或医疗化表达',
    '助眠': '具体疗效或医疗化表达',
    '镇静': '具体疗效或医疗化表达',
    '燃脂': '具体疗效或医疗化表达',
    '降糖': '具体疗效或医疗化表达',
    '促消化': '具体疗效或医疗化表达',
    '不失眠': '具体疗效或医疗化表达',
    '医学': '具体疗效或医疗化表达',
}

INGREDIENT_REMARK_REPLACEMENTS = {
    '助眠': '具体疗效',
    '镇静': '具体疗效',
    '治疗': '具体疗效',
    '治愈': '具体疗效',
    '疗愈': '具体疗效',
    '燃脂': '具体疗效',
    '降糖': '具体疗效',
    '促消化': '具体疗效',
    '医学': '具体疗效',
    '清热': '日常体验描述',
    '减脂': '日常体验描述',
    '功效': '日常体验描述',
}

SCHEME_RECOMMENDATION_REPLACEMENTS = {
    '治愈': '安抚感',
    '疗愈': '安抚感',
    '燃脂': '低负担',
    '促消化': '清爽解腻',
    '不失眠': '低刺激',
    '解郁': '放松',
    '助眠': '放松',
    '降糖': '低糖',
    '医学': '日常体验',
    '治疗': '日常体验',
}

USER_INPUT_VALUE_MAP = {
    '想清爽': '清爽',
    '想温暖': '温热',
    '想补水': '轻补充',
    '想补充': '轻补充',
    '想平静': '想放松',
    '想稳定': '专注',
    '用眼疲劳': '疲惫',
    '用眼疲惫': '疲惫',
    '眼睛累': '疲惫',
    '身体不适': '低刺激',
    '怕冷': '寒冷天气',
    '空腹不适': '轻补充',
    '久坐疲惫': '疲惫',
    '用脑疲惫': '疲惫',
    '季节不适': '低刺激',
    '炎热不适': '炎热天气',
    '深夜': '夜间',
    '焦虑': '紧张',
}

SPECIAL_ROLE_BY_NAME = {
    '蜂蜜': '甜度、风味',
    '代糖': '甜度',
    '黑糖': '甜度、风味',
    '果粒': '口感、装饰',
    '奶泡': '口感、装饰',
    '冰块': '辅助',
    '气泡水': '基底、口感',
    '苏打水': '基底、口感',
    '咖啡冻': '口感、风味',
    '美式咖啡液': '基底、风味',
}

ROLE_BY_CATEGORY = {
    '茶基类': '基底',
    '咖啡基类': '基底、风味',
    '奶基类': '基底、口感',
    '可可类': '风味、基底',
    '气泡基类': '基底、口感',
    '果味类': '风味、装饰',
    '花草类': '风味、装饰',
    '甜味辅料类': '甜度、风味',
}

COMMON_ROLE_FALLBACKS = {
    '辅料类': {
        '冰块': '辅助',
        '果粒': '口感、装饰',
        '奶泡': '口感、装饰',
        '咖啡冻': '口感、风味',
        '气泡水': '基底、口感',
        '苏打水': '基底、口感',
    }
}

ROLE_TOKEN_RE = re.compile(r'[、,，;/；|\n]+')
TOKEN_SPLIT_RE = re.compile(r'[、,，;/；|\n]+')
COMMENTARY_SPLIT_RE = re.compile(r'[、,，;/；|\n]+')
HEADER_HINTS = {
    '标签字典表': ['标签分类', 'tag_id', '标签名', '含义', '适用表/字段', '推荐使用建议', '同义词/避免写法'],
    '饮品方案表': ['recipe_id', '饮品名称', '饮品类型', '成分组合', '成分角色'],
    '用户输入表': ['session_id', 'user_id', '时间段', '地点/场景'],
}

INVALID_TAG_TERMS = ['治疗', '治愈', '疗愈', '助眠', '镇静', '燃脂', '降糖', '促消化', '不失眠', '医学']


def clean_cell(value: object) -> str:
    if value is None:
        return ''
    text = str(value).replace('\u3000', ' ').strip()
    return text


def normalize_text_frame(df: pd.DataFrame) -> pd.DataFrame:
    return df.apply(lambda col: col.map(clean_cell))


def drop_all_empty(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    non_empty_cols = [col for col in df.columns if not df[col].map(clean_cell).eq('').all()]
    df = df[non_empty_cols].copy()
    non_empty_rows = [not row.map(clean_cell).eq('').all() for _, row in df.iterrows()]
    return df.loc[non_empty_rows].reset_index(drop=True)


def read_csv_with_fallback(path: Path) -> pd.DataFrame:
    last_error: Exception | None = None
    for encoding in CSV_ENCODINGS:
        try:
            return pd.read_csv(path, dtype=str, keep_default_na=False, encoding=encoding, engine='python')
        except Exception as exc:  # pragma: no cover - fallback loop
            last_error = exc
    raise last_error  # type: ignore[misc]


def row_matches_sequence(row: pd.Series, sequence: list[str]) -> bool:
    values = [clean_cell(value) for value in row.tolist()]
    for offset in range(0, len(values) - len(sequence) + 1):
        if values[offset:offset + len(sequence)] == sequence:
            return True
    return False


def find_header_row(df: pd.DataFrame, sequence: list[str]) -> int:
    for index, row in df.iterrows():
        if row_matches_sequence(row, sequence):
            return index
    raise ValueError(f'未找到表头：{sequence}')


def split_tokens(text: str) -> list[str]:
    tokens = []
    for token in TOKEN_SPLIT_RE.split(clean_cell(text)):
        token = token.strip().strip('。').strip('.')
        if token:
            tokens.append(token)
    return tokens


def dedupe_preserve_order(items: Iterable[str]) -> list[str]:
    seen = set()
    result = []
    for item in items:
        if item and item not in seen:
            seen.add(item)
            result.append(item)
    return result


def replace_terms(text: str, replacements: dict[str, str], stats: Counter[str]) -> str:
    value = clean_cell(text)
    if not value:
        return ''
    for old, new in replacements.items():
        occurrences = value.count(old)
        if occurrences:
            stats[old] += occurrences
            value = value.replace(old, new)
    value = re.sub(r'\s+', ' ', value).strip()
    return value


def normalize_role_text(role_text: str) -> str:
    tokens = []
    for token in ROLE_TOKEN_RE.split(clean_cell(role_text)):
        token = token.strip()
        if token in ALLOWED_ROLE_TOKENS and token not in tokens:
            tokens.append(token)
    return '、'.join(tokens)


def assign_ingredient_role(row: pd.Series) -> str:
    name = clean_cell(row.get('成分名称', ''))
    category = clean_cell(row.get('成分类别', ''))

    if name in SPECIAL_ROLE_BY_NAME:
        return SPECIAL_ROLE_BY_NAME[name]

    if '可可' in name:
        return '风味、基底'

    if category in ROLE_BY_CATEGORY:
        return ROLE_BY_CATEGORY[category]

    if category in COMMON_ROLE_FALLBACKS:
        for key, value in COMMON_ROLE_FALLBACKS[category].items():
            if key in name:
                return value

    if '冰块' in name:
        return '辅助'
    if '果粒' in name:
        return '口感、装饰'
    if '奶泡' in name:
        return '口感、装饰'
    if '咖啡冻' in name:
        return '口感、风味'
    return ''


def trim_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = normalize_text_frame(df)
    return drop_all_empty(df)


def normalize_list_column(value: object, mapping: dict[str, str]) -> str:
    text = clean_cell(value)
    if not text:
        return ''
    items = []
    for token in split_tokens(text):
        items.append(mapping.get(token, token))
    return '、'.join(dedupe_preserve_order(items))


def parse_composition(text: str) -> list[str]:
    tokens = []
    for token in TOKEN_SPLIT_RE.split(clean_cell(text)):
        token = token.strip().strip('。').strip('.')
        token = re.sub(r'\s+', '', token)
        if token:
            tokens.append(token)
    return dedupe_preserve_order(tokens)


def contains_name(candidate: str, names: set[str]) -> bool:
    if candidate in names:
        return True
    # Allow obvious punctuation cleanup only; do not auto-fix or broaden matching heavily.
    candidate_no_suffix = re.sub(r'(饮料|饮品)$', '', candidate)
    if candidate_no_suffix != candidate and candidate_no_suffix in names:
        return True
    return False


def normalize_scheme_machine_flag(value: object) -> str:
    text = clean_cell(value)
    mapping = {
        '须预制': '需预制',
        '需要预制': '需预制',
        '否': '暂不适合',
        '是': '是',
    }
    return mapping.get(text, text)


def clean_scheme_recommendation(text: object, stats: Counter[str]) -> str:
    return replace_terms(clean_cell(text), SCHEME_RECOMMENDATION_REPLACEMENTS, stats)


def clean_ingredient_remark(text: object, stats: Counter[str]) -> str:
    return replace_terms(clean_cell(text), INGREDIENT_REMARK_REPLACEMENTS, stats)


def normalize_label_dict_text(text: object, stats: Counter[str]) -> str:
    return replace_terms(clean_cell(text), LABEL_TEXT_REPLACEMENTS, stats)


def normalize_user_input_values(text: object) -> str:
    return normalize_list_column(text, USER_INPUT_VALUE_MAP)


def keep_formal_label_dict(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    header_idx = find_header_row(df, HEADER_HINTS['标签字典表'])
    body = df.iloc[header_idx + 1:].copy().reset_index(drop=True)
    body = body.iloc[:, :len(LABEL_DICT_FINAL_COLUMNS)].copy()
    body.columns = LABEL_DICT_FINAL_COLUMNS
    body = trim_dataframe(body)

    # Drop repeated header rows and malformed rows.
    repeated_header = body['tag_id'].eq('tag_id') | body['标签名'].eq('标签名')
    body = body.loc[~repeated_header].reset_index(drop=True)
    body['标签分类'] = body['标签分类'].replace('', pd.NA).ffill().fillna('')
    body = body[body['tag_id'].str.fullmatch(r'[A-Z]{2,4}\d{3}', na=False)].reset_index(drop=True)

    text_stats = Counter()
    for column in ['标签名', '含义', '适用表/字段', '推荐使用建议', '同义词/避免写法']:
        body[column] = body[column].map(lambda value: normalize_label_dict_text(value, text_stats))
    body = body[LABEL_DICT_FINAL_COLUMNS]

    issue_lines = []
    duplicate_tag_id = body.loc[body.duplicated('tag_id', keep=False), 'tag_id'].tolist()
    duplicate_tag_name = body.loc[body.duplicated('标签名', keep=False), '标签名'].tolist()
    issue_lines.append(f'标签字典表：有效行 {len(body)}，列数 {len(body.columns)}')
    issue_lines.append(f'标签字典表：重复 tag_id {sorted(set(duplicate_tag_id)) if duplicate_tag_id else "无"}')
    issue_lines.append(f'标签字典表：重复 标签名 {sorted(set(duplicate_tag_name)) if duplicate_tag_name else "无"}')
    issue_lines.append(f'标签字典表：功效/医疗化表达替换统计 {dict(text_stats) if text_stats else "无"}')
    return body, issue_lines


def keep_formal_ingredient(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str], Counter[str]]:
    df = trim_dataframe(df)
    if '成分角色' not in df.columns:
        insert_at = df.columns.get_loc('成分类别') + 1 if '成分类别' in df.columns else len(df.columns)
        df.insert(insert_at, '成分角色', '')

    df = df.loc[~df.astype(str).apply(lambda row: row.eq('标签分类').all(), axis=1)].reset_index(drop=True)

    text_stats = Counter()
    df['备注'] = df['备注'].map(lambda value: clean_ingredient_remark(value, text_stats) if '备注' in df.columns else value)
    df['成分角色'] = df.apply(
        lambda row: normalize_role_text(row['成分角色']) if clean_cell(row.get('成分角色', '')) else normalize_role_text(assign_ingredient_role(row)),
        axis=1,
    )

    # Ensure all roles are valid and fill blanks again if normalization removed everything.
    role_is_blank = df['成分角色'].eq('')
    if role_is_blank.any():
        df.loc[role_is_blank, '成分角色'] = df.loc[role_is_blank].apply(lambda row: normalize_role_text(assign_ingredient_role(row)), axis=1)

    if 'ingredient_id' in df.columns:
        id_dupes = df.loc[df.duplicated('ingredient_id', keep=False), 'ingredient_id'].tolist()
    else:
        id_dupes = []
    name_dupes = df.loc[df.duplicated('成分名称', keep=False), '成分名称'].tolist() if '成分名称' in df.columns else []

    issue_lines = []
    issue_lines.append(f'饮品成分表：有效行 {len(df)}，列数 {len(df.columns)}')
    issue_lines.append(f'饮品成分表：重复 ingredient_id {sorted(set(id_dupes)) if id_dupes else "无"}')
    issue_lines.append(f'饮品成分表：重复 成分名称 {sorted(set(name_dupes)) if name_dupes else "无"}')
    issue_lines.append(f'饮品成分表：功效/医疗化表达替换统计 {dict(text_stats) if text_stats else "无"}')

    ordered_columns = [col for col in INGREDIENT_ROLE_COLUMNS if col in df.columns]
    extra_columns = [col for col in df.columns if col not in ordered_columns]
    df = df[ordered_columns + extra_columns].copy()
    return df, issue_lines, text_stats


def keep_formal_scheme(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str], Counter[str], list[str]]:
    body = trim_dataframe(df)

    if body.empty:
        raise ValueError('饮品方案表清洗后为空，请检查源文件。')

    # The source CSV already stores the formal header in the first row of column names.
    # The first column is a description column named “字段”; remove it from the final table.
    if clean_cell(body.columns[0]) == SCHEME_EXPLANATORY_COLUMN:
        body = body.iloc[:, 1:].copy()

    body = trim_dataframe(body)

    if SCHEME_RECIPE_ID_COL not in body.columns:
        raise ValueError('饮品方案表未找到 recipe_id 列。')

    # Remove any repeated header-like rows that may appear in the data body.
    body = body[body[SCHEME_RECIPE_ID_COL].ne('recipe_id')]
    if '饮品名称' in body.columns:
        body = body[body['饮品名称'].ne('饮品名称')]
    body = body.reset_index(drop=True)

    desired_front = [
        'recipe_id', '饮品名称', '饮品类型', '成分组合', '成分角色', '用量等级', '适配身体状态', '适配心情状态',
        '感官标签', '体验标签', '健康约束', '适合场景', '甜度建议', '冷热建议', '制作复杂度', '推荐解释',
        '视觉标签', '可否机器制作',
    ]
    present_front = [col for col in desired_front if col in body.columns]
    other_columns = [col for col in body.columns if col not in present_front]
    body = body[present_front + other_columns].copy()

    text_stats = Counter()
    if '可否机器制作' in body.columns:
        body['可否机器制作'] = body['可否机器制作'].map(normalize_scheme_machine_flag)
    if '推荐解释' in body.columns:
        body['推荐解释'] = body['推荐解释'].map(lambda value: clean_scheme_recommendation(value, text_stats))
    if '成分角色' in body.columns:
        body['成分角色'] = body['成分角色'].map(lambda value: normalize_list_column(value, {}))
    for column in ['适配身体状态', '适配心情状态', '感官标签', '体验标签', '健康约束', '适合场景', '视觉标签']:
        if column in body.columns:
            body[column] = body[column].map(lambda value: normalize_list_column(value, {}))

    recipe_dupes = body.loc[body.duplicated('recipe_id', keep=False), 'recipe_id'].tolist() if 'recipe_id' in body.columns else []
    name_dupes = body.loc[body.duplicated('饮品名称', keep=False), '饮品名称'].tolist() if '饮品名称' in body.columns else []

    ingredient_names = set()
    ingredient_ref = OUTPUT_FILES['饮品成分表']
    if ingredient_ref.exists():
        ingredient_names = set(pd.read_csv(ingredient_ref, dtype=str, keep_default_na=False)['成分名称'].map(clean_cell).tolist())

    missing_ingredients: list[str] = []
    if '成分组合' in body.columns:
        for value in body['成分组合'].tolist():
            for item in parse_composition(value):
                if not contains_name(item, ingredient_names):
                    missing_ingredients.append(item)
    missing_ingredients = sorted(set(missing_ingredients))

    issue_lines = []
    issue_lines.append(f'饮品方案表：有效行 {len(body)}，列数 {len(body.columns)}')
    issue_lines.append(f'饮品方案表：重复 recipe_id {sorted(set(recipe_dupes)) if recipe_dupes else "无"}')
    issue_lines.append(f'饮品方案表：重复 饮品名称 {sorted(set(name_dupes)) if name_dupes else "无"}')
    issue_lines.append(f'饮品方案表：缺失成分 {missing_ingredients if missing_ingredients else "无"}')
    issue_lines.append(f'饮品方案表：功效/医疗化表达替换统计 {dict(text_stats) if text_stats else "无"}')

    return body, issue_lines, text_stats, missing_ingredients


def keep_formal_user_input(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    header_idx = find_header_row(df, HEADER_HINTS['用户输入表'])
    header_values = [clean_cell(value) for value in df.iloc[header_idx].tolist()]
    body = df.iloc[header_idx + 1:].copy().reset_index(drop=True)
    body = trim_dataframe(body)

    usable_columns = [column for column in header_values if column]
    body = body.iloc[:, :len(usable_columns)].copy()
    body.columns = usable_columns
    body = trim_dataframe(body)

    # Remove any repeated header rows that may appear in the body.
    body = body[~body.astype(str).apply(lambda row: row.tolist()[:4] == HEADER_HINTS['用户输入表'][:4], axis=1)]
    body = body.reset_index(drop=True)

    # Keep only formal rows with session_id like S001.
    if 'session_id' not in body.columns:
        raise ValueError('用户输入表未找到 session_id 列。')
    body = body[body['session_id'].str.fullmatch(r'S\d{3}', na=False)].reset_index(drop=True)

    text_columns_to_normalize = ['身体状态标签', '心情状态标签', '体验需求标签', '系统解析标签']
    for column in text_columns_to_normalize:
        if column in body.columns:
            body[column] = body[column].map(normalize_user_input_values)

    session_dupes = body.loc[body.duplicated('session_id', keep=False), 'session_id'].tolist() if 'session_id' in body.columns else []
    empty_user_ids = body.index[body.get('user_id', pd.Series(dtype=str)).map(clean_cell).eq('')].tolist() if 'user_id' in body.columns else []

    issue_lines = []
    issue_lines.append(f'用户输入表：有效行 {len(body)}，列数 {len(body.columns)}')
    issue_lines.append(f'用户输入表：重复 session_id {sorted(set(session_dupes)) if session_dupes else "无"}')
    issue_lines.append(f'用户输入表：user_id 为空的行 {empty_user_ids if empty_user_ids else "无"}')

    return body, issue_lines


def collect_label_names(label_df: pd.DataFrame) -> set[str]:
    return set(label_df['标签名'].map(clean_cell).tolist())


def split_for_cross_check(text: object) -> list[str]:
    tokens = []
    for token in COMMENTARY_SPLIT_RE.split(clean_cell(text)):
        token = token.strip().strip('。').strip('.')
        if token:
            tokens.append(token)
    return tokens


def cross_check_labels(label_names: set[str], user_df: pd.DataFrame, scheme_df: pd.DataFrame) -> list[str]:
    issues = []
    user_fields = ['身体状态标签', '心情状态标签', '体验需求标签', '系统解析标签']
    scheme_fields = ['适配身体状态', '适配心情状态', '感官标签', '体验标签', '健康约束', '视觉标签']

    user_unknown = []
    for field in user_fields:
        if field not in user_df.columns:
            continue
        for value in user_df[field].tolist():
            for token in split_for_cross_check(value):
                if token not in label_names:
                    user_unknown.append(f'{field}:{token}')

    scheme_unknown = []
    for field in scheme_fields:
        if field not in scheme_df.columns:
            continue
        for value in scheme_df[field].tolist():
            for token in split_for_cross_check(value):
                if token not in label_names:
                    scheme_unknown.append(f'{field}:{token}')

    missing_ingredients = []
    if '成分组合' in scheme_df.columns:
        ingredient_names = set(INPUT_FILES['饮品成分表'].exists() and pd.read_csv(OUTPUT_FILES['饮品成分表'], dtype=str, keep_default_na=False)['成分名称'].map(clean_cell).tolist() or [])
        for value in scheme_df['成分组合'].tolist():
            for token in parse_composition(value):
                if not contains_name(token, ingredient_names):
                    missing_ingredients.append(token)

    issues.append(f'跨表检查：用户输入表非标准标签词 {sorted(set(user_unknown)) if user_unknown else "无"}')
    issues.append(f'跨表检查：饮品方案表非标准标签词 {sorted(set(scheme_unknown)) if scheme_unknown else "无"}')
    issues.append(f'跨表检查：饮品方案表成分组合缺失项 {sorted(set(missing_ingredients)) if missing_ingredients else "无"}')
    return issues


def write_outputs(tables: dict[str, pd.DataFrame]) -> None:
    for name, df in tables.items():
        df.to_csv(OUTPUT_FILES[name], index=False, encoding='utf-8-sig')

    with pd.ExcelWriter(OUTPUT_XLSX, engine='openpyxl') as writer:
        tables['标签字典表'].to_excel(writer, sheet_name='标签字典表', index=False)
        tables['饮品成分表'].to_excel(writer, sheet_name='饮品成分表', index=False)
        tables['饮品方案表'].to_excel(writer, sheet_name='饮品方案表', index=False)
        tables['用户输入表'].to_excel(writer, sheet_name='用户输入表', index=False)


def build_report_lines(
    tables: dict[str, pd.DataFrame],
    label_issues: list[str],
    ingredient_issues: list[str],
    scheme_issues: list[str],
    user_issues: list[str],
    cross_issues: list[str],
) -> list[str]:
    lines = ['数据清洗检查报告', '']
    for name, df in tables.items():
        lines.append(f'{name}：行数 {len(df)}，列数 {len(df.columns)}')
    lines.append('')
    lines.append('重复 ID 与异常检查')
    lines.extend(label_issues)
    lines.extend(ingredient_issues)
    lines.extend(scheme_issues)
    lines.extend(user_issues)
    lines.append('')
    lines.append('跨表检查')
    lines.extend(cross_issues)
    return lines


def main() -> None:
    raw_label = read_csv_with_fallback(INPUT_FILES['标签字典表'])
    raw_ingredient = read_csv_with_fallback(INPUT_FILES['饮品成分表'])
    raw_scheme = read_csv_with_fallback(INPUT_FILES['饮品方案表'])
    raw_user = read_csv_with_fallback(INPUT_FILES['用户输入表'])

    label_df, label_issues = keep_formal_label_dict(raw_label)
    ingredient_df, ingredient_issues, ingredient_stats = keep_formal_ingredient(raw_ingredient)

    # Write ingredient table early so the scheme cross-check can reference the finalized component names.
    ingredient_df.to_csv(OUTPUT_FILES['饮品成分表'], index=False, encoding='utf-8-sig')

    scheme_df, scheme_issues, scheme_stats, scheme_missing = keep_formal_scheme(raw_scheme)
    user_df, user_issues = keep_formal_user_input(raw_user)

    cross_issues = cross_check_labels(collect_label_names(label_df), user_df, scheme_df)

    tables = {
        '标签字典表': label_df,
        '饮品成分表': ingredient_df,
        '饮品方案表': scheme_df,
        '用户输入表': user_df,
    }
    write_outputs(tables)

    report_lines = build_report_lines(
        tables=tables,
        label_issues=label_issues,
        ingredient_issues=ingredient_issues,
        scheme_issues=scheme_issues,
        user_issues=user_issues,
        cross_issues=cross_issues,
    )
    report_lines.insert(7, f'饮品成分表：功效/医疗化表达替换统计 {dict(ingredient_stats) if ingredient_stats else "无"}')
    report_lines.insert(8, f'饮品方案表：功效/医疗化表达替换统计 {dict(scheme_stats) if scheme_stats else "无"}')
    report_lines.insert(9, f'饮品方案表：成分组合缺失项 {scheme_missing if scheme_missing else "无"}')
    REPORT_TXT.write_text('\n'.join(report_lines), encoding='utf-8')

    print(f'标签字典表：行数 {len(label_df)}，列数 {len(label_df.columns)}')
    print(f'饮品成分表：行数 {len(ingredient_df)}，列数 {len(ingredient_df.columns)}')
    print(f'饮品方案表：行数 {len(scheme_df)}，列数 {len(scheme_df.columns)}')
    print(f'用户输入表：行数 {len(user_df)}，列数 {len(user_df.columns)}')
    print('发现的问题清单：')
    for line in report_lines[1:]:
        if line:
            print(line)
    print('清洗完成，已生成四张终版 CSV、一个 Excel 汇总文件和检查报告。')


if __name__ == '__main__':
    main()