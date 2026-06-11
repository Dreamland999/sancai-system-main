#!/usr/bin/env python
"""Feedback 数据检查脚本

用法：
    python scripts/inspect_feedback.py              # 终端打印汇总
    python scripts/inspect_feedback.py --csv         # 额外导出 CSV 到 reports/
    python scripts/inspect_feedback.py --recent 20   # 显示最新 N 条

不依赖复杂环境，标准库即可运行。
"""

import json
import os
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
JSONL_PATH = PROJECT_ROOT / "backend" / "feedback_log.jsonl"
REPORTS_DIR = PROJECT_ROOT / "reports"
CSV_PATH = REPORTS_DIR / "feedback_events.csv"


def load_events():
    if not JSONL_PATH.exists():
        print(f"[!] 文件不存在: {JSONL_PATH}")
        print("    请先走一遍主流程让后端产生 feedback 日志。")
        return []

    events = []
    with open(JSONL_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                print(f"[!] 跳过无效行: {line[:80]}...")
    return events


def print_summary(events):
    print("=" * 60)
    print(f"  Feedback 数据检查 — {JSONL_PATH}")
    print(f"  总事件数: {len(events)}")
    print("=" * 60)

    if not events:
        return

    # 按 event_type 统计
    type_counts = Counter(e.get("event_type") or "(旧记录/无event_type)" for e in events)
    print("\n[event_type 分布]")
    for t, c in type_counts.most_common():
        print(f"  {c:>5}  {t}")

    # 按 recipe_id 统计
    recipe_counts = Counter(e.get("recipe_id") or "(无)" for e in events)
    print("\n[recipe_id 分布]")
    for r, c in recipe_counts.most_common():
        print(f"  {c:>5}  {r}")

    # 按 session_id 聚合用户路径
    session_paths = defaultdict(list)
    for e in events:
        sid = e.get("session_id") or "(无)"
        session_paths[sid].append(e.get("event_type") or "?")
    print(f"\n[session 数量: {len(session_paths)}]")
    for sid, path in list(session_paths.items())[:5]:
        arrow = " → ".join(path)
        print(f"  {sid[:20]:20s}  {arrow}")

    # 最新 10 条
    recent = int("--recent" in " ".join(sys.argv) and sys.argv[sys.argv.index("--recent") + 1] if "--recent" in sys.argv else "10")
    n = min(recent, len(events))
    if n > 0:
        print(f"\n[最近 {n} 条]")
        for e in events[-n:]:
            ts = e.get("timestamp", "")[:19]
            et = e.get("event_type") or "?"
            rid = e.get("recipe_id") or "-"
            sid = (e.get("session_id") or "")[:16]
            extra = ""
            p = e.get("payload") or {}
            if isinstance(p, dict) and p:
                extra = json.dumps(p, ensure_ascii=False)[:60]
            print(f"  {ts}  {et:22s}  recipe={rid:8s}  sid={sid}  {extra}")


def export_csv(events):
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    fieldnames = ["timestamp", "session_id", "user_id", "recipe_id", "event_type", "payload_json"]
    with open(CSV_PATH, "w", encoding="utf-8-sig", newline="") as f:
        f.write(",".join(fieldnames) + "\n")
        for e in events:
            ts = e.get("timestamp", "")[:19]
            sid = e.get("session_id", "")
            uid = e.get("user_id", "")
            rid = e.get("recipe_id", "")
            et = e.get("event_type", "")
            pl = json.dumps(e.get("payload", {}), ensure_ascii=False).replace('"', '""')
            f.write(f'{ts},{sid},{uid},{rid},{et},"{pl}"\n')

    size_kb = CSV_PATH.stat().st_size / 1024
    print(f"\n[CSV 导出] {CSV_PATH}  ({size_kb:.1f} KB, {len(events)} 行)")


if __name__ == "__main__":
    events = load_events()
    print_summary(events)

    if "--csv" in sys.argv and events:
        export_csv(events)
