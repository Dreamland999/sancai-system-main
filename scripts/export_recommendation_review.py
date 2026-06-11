"""
推荐结果人工审查导出脚本
读取用户输入表，批量调用 RecommenderService，导出 top3 结果
"""
from __future__ import annotations
import csv, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "backend"))

import pandas as pd
from recommender_service import RecommenderService

FIELD_MAP = {
    '地点/场景': 'scene',
    '身体状态标签': 'body',
    '心情状态标签': 'mood',
    '口味偏好': 'flavor_preference',
    '冷热偏好': 'temperature_preference',
    '饮食限制': 'limits',
}

OUTPUT_COLS = [
    'input_id', 'body', 'mood', 'scene', 'flavor_preference', 'temperature_preference',
    'limits', '推荐方向',
    'top1_recipe_id', 'top1_name', 'top1_score', 'top1_reason',
    'top2_recipe_id', 'top2_name', 'top2_score', 'top2_reason',
    'top3_recipe_id', 'top3_name', 'top3_score', 'top3_reason',
    'manual_choice', 'manual_note',
]

def ssplit(v):
    if not v or str(v).strip() in ('', 'nan'): return []
    return [t.strip() for t in str(v).replace('，', ',').replace('、', ',').replace('；', ',').split(',') if t.strip()]

def main():
    from schemas import UserStateRequest

    print('Loading data...')
    user_df = pd.read_csv(ROOT / 'data' / '用户输入表_最终检查版.csv', dtype=str, keep_default_na=False, encoding='utf-8-sig')
    print(f'  users: {len(user_df)} rows, cols: {list(user_df.columns)}')

    print('Loading RecommenderService...')
    s = RecommenderService()
    print(f'  model_mode={s.model_mode} vocab={s.vocab_size} recipes={len(s.recipe_rows)}')

    reports_dir = ROOT / 'reports'
    reports_dir.mkdir(exist_ok=True)

    rows = []
    success = 0; fail = 0

    for idx, urow in user_df.iterrows():
        body = ssplit(urow.get('身体状态标签', ''))
        mood = ssplit(urow.get('心情状态标签', ''))
        scene = ssplit(urow.get('地点/场景', ''))
        flavor = ssplit(urow.get('口味偏好', ''))
        temp = ssplit(urow.get('冷热偏好', ''))
        limits = ssplit(urow.get('饮食限制', ''))
        direction = urow.get('推荐方向', '')

        row = {
            'input_id': f'U{idx+1:04d}',
            'body': '、'.join(body),
            'mood': '、'.join(mood),
            'scene': '、'.join(scene),
            'flavor_preference': '、'.join(flavor),
            'temperature_preference': '、'.join(temp),
            'limits': '、'.join(limits),
            '推荐方向': direction,
        }

        try:
            payload = UserStateRequest(
                scene=scene, body=body, mood=mood, needs=[],
                limits=limits, flavor_preference=flavor, temperature_preference=temp
            )
            r = s.recommend(payload)
            recs = r.get('recommendations', [])
            for j in range(3):
                if j < len(recs):
                    d = recs[j]
                    row[f'top{j+1}_recipe_id'] = d.get('recipe_id', '')
                    row[f'top{j+1}_name'] = d.get('name', '')
                    row[f'top{j+1}_score'] = round(d.get('score', 0), 4)
                    row[f'top{j+1}_reason'] = d.get('match_reason', '')[:120]
                else:
                    row[f'top{j+1}_recipe_id'] = ''
                    row[f'top{j+1}_name'] = ''
                    row[f'top{j+1}_score'] = ''
                    row[f'top{j+1}_reason'] = ''
            row['manual_choice'] = ''
            row['manual_note'] = ''
            rows.append(row)
            success += 1
        except Exception as e:
            print(f'  [FAIL] U{idx+1:04d}: {e}')
            fail += 1

        if (idx + 1) % 100 == 0:
            print(f'  progress: {idx+1}/{len(user_df)}')

    # Write full CSV
    out = reports_dir / 'recommendation_review_top3.csv'
    with out.open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=OUTPUT_COLS, extrasaction='ignore')
        w.writeheader()
        w.writerows(rows)
    print(f'\n[export] Full CSV: {out} ({len(rows)} rows)')

    # Priority filter (max 50)
    priority = []
    for r in sorted(rows, key=lambda x: abs(float(x.get('top1_score', 0) or 0) - float(x.get('top2_score', 0) or 0))):
        if len(priority) >= 50:
            break
        s1 = float(r.get('top1_score', 0) or 0)
        s2 = float(r.get('top2_score', 0) or 0)
        has_limits = bool(r.get('limits', ''))
        has_temp = bool(r.get('temperature_preference', ''))
        gap = abs(s1 - s2)
        if gap < 0.03 or has_limits or has_temp:
            priority.append(r)

    if priority:
        out2 = reports_dir / 'recommendation_review_priority.csv'
        with out2.open('w', encoding='utf-8-sig', newline='') as f:
            w = csv.DictWriter(f, fieldnames=OUTPUT_COLS, extrasaction='ignore')
            w.writeheader()
            w.writerows(priority)
        print(f'[export] Priority CSV: {out2} ({len(priority)} rows)')

    print(f'\nDone. Total={len(user_df)} Success={success} Fail={fail} Priority={len(priority)}')


if __name__ == '__main__':
    main()
