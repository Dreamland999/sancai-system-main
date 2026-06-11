import csv
import sqlite3
import os
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BACKEND_DIR.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

try:
    from config import DB_PATH, CSV_FILES
except ImportError:
    from backend.config import DB_PATH, CSV_FILES


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS tag_dict (
            tag_id TEXT PRIMARY KEY,
            category TEXT NOT NULL,
            name TEXT NOT NULL,
            meaning TEXT,
            applies_to TEXT,
            usage_tip TEXT,
            synonyms TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS ingredients (
            ingredient_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT,
            base_attributes TEXT,
            has_caffeine TEXT,
            has_dairy TEXT,
            sensory_tags TEXT,
            experience_tags TEXT,
            suitable_states TEXT,
            unsuitable_states TEXT,
            health_constraints TEXT,
            suitable_scenes TEXT,
            visual_tags TEXT,
            source TEXT,
            notes TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS recipes (
            recipe_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT,
            ingredients_combo TEXT,
            ingredient_roles TEXT,
            dosage_levels TEXT,
            suitable_body TEXT,
            suitable_mood TEXT,
            sensory_tags TEXT,
            experience_tags TEXT,
            health_constraints TEXT,
            suitable_scenes TEXT,
            sweetness TEXT,
            temperature TEXT,
            complexity TEXT,
            description TEXT,
            visual_tags TEXT,
            can_machine_make TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS user_sessions (
            session_id TEXT PRIMARY KEY,
            user_id TEXT,
            body_states TEXT,
            mood_states TEXT,
            scene_contexts TEXT,
            experience_needs TEXT,
            dietary_restrictions TEXT,
            raw_user_text TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS recommendations (
            recommendation_id TEXT PRIMARY KEY,
            session_id TEXT,
            recipe_id TEXT,
            score_total REAL,
            score_state_match REAL,
            score_flavor REAL,
            score_scene REAL,
            score_health REAL,
            score_visual REAL,
            match_reason TEXT,
            polished_text TEXT,
            visual_prompt TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES user_sessions(session_id),
            FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            feedback_id TEXT PRIMARY KEY,
            recommendation_id TEXT,
            user_id TEXT,
            rating REAL,
            feedback_text TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS visual_mappings (
            visual_id TEXT PRIMARY KEY,
            source_tag_id TEXT,
            color_palette TEXT,
            graphics TEXT,
            composition TEXT,
            reference_style TEXT,
            example_prompt TEXT
        )
    """)

    # New table for stores
    c.execute("""
        CREATE TABLE IF NOT EXISTS stores (
            store_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            address TEXT,
            distance REAL,
            latitude REAL,
            longitude REAL,
            is_open INTEGER DEFAULT 1
        )
    """)

    conn.commit()
    conn.close()


def import_tag_dict():
    conn = get_conn()
    c = conn.cursor()
    c.execute("DELETE FROM feedback")
    c.execute("DELETE FROM recommendations")
    c.execute("DELETE FROM user_sessions")
    c.execute("DELETE FROM visual_mappings")
    c.execute("DELETE FROM recipes")
    c.execute("DELETE FROM ingredients")
    c.execute("DELETE FROM tag_dict")

    seen = set()
    csv_path = CSV_FILES["tags"]
    if not os.path.exists(csv_path):
        print(f"[database] Warning: tags CSV not found at {csv_path}")
        conn.close()
        return 0

    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        current_category = ""
        header_found = False
        for row in reader:
            if not header_found:
                if len(row) >= 2 and row[0].strip() == "标签分类" and row[1].strip() == "tag_id":
                    header_found = True
                continue

            tag_id = row[1].strip() if len(row) > 1 else ""
            if not tag_id:
                continue
            allowed = "BMCSEHVI"
            if not tag_id[0] in allowed or len(tag_id) < 3:
                continue
            if tag_id in seen:
                continue
            seen.add(tag_id)

            cat_cell = row[0].strip() if len(row) > 0 else ""
            if cat_cell:
                current_category = cat_cell

            name = row[2].strip() if len(row) > 2 else ""
            meaning = row[3].strip() if len(row) > 3 else ""
            applies_to = row[4].strip() if len(row) > 4 else ""
            usage = row[5].strip() if len(row) > 5 else ""
            synonyms = row[6].strip() if len(row) > 6 else ""

            c.execute(
                "INSERT INTO tag_dict (tag_id, category, name, meaning, applies_to, usage_tip, synonyms) VALUES (?,?,?,?,?,?,?)",
                (tag_id, current_category, name, meaning, applies_to, usage, synonyms),
            )

    conn.commit()
    conn.close()
    return len(seen)


def import_ingredients():
    conn = get_conn()
    c = conn.cursor()
    count = 0
    csv_path = CSV_FILES["ingredients"]
    if not os.path.exists(csv_path):
        print(f"[database] Warning: ingredients CSV not found at {csv_path}")
        conn.close()
        return 0

    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader, None)

        col_map = {}
        for i, h in enumerate(header):
            h_clean = h.strip()
            if "ingredient_id" in h_clean or h_clean == "ingredient_id":
                col_map["id"] = i
            elif "成分名称" in h_clean:
                col_map["name"] = i
            elif "成分类别" in h_clean:
                col_map["category"] = i
            elif "基础属性" in h_clean:
                col_map["base_attr"] = i
            elif "是否含咖啡因" in h_clean:
                col_map["caffeine"] = i
            elif "是否含乳" in h_clean:
                col_map["dairy"] = i
            elif h_clean == "感官标签":
                col_map["sensory"] = i
            elif "状态" in h_clean and "体验" in h_clean:
                col_map["exp_tags"] = i
            elif h_clean == "适合状态":
                col_map["suitable"] = i
            elif h_clean == "不适合状态":
                col_map["unsuitable"] = i
            elif "健康约束" in h_clean:
                col_map["health"] = i
            elif "适合场景" in h_clean:
                col_map["scene"] = i
            elif h_clean == "视觉标签":
                col_map["visual"] = i
            elif "标签来源" in h_clean:
                col_map["source"] = i
            elif "备注" in h_clean:
                col_map["notes"] = i

        for row in reader:
            if not row or not row[col_map.get("id", 0)].strip():
                continue
            rid = row[col_map["id"]].strip()
            if not rid or rid == "ingredient_id" or not rid.startswith("I"):
                continue

            def g(k):
                return row[col_map[k]].strip() if k in col_map and len(row) > col_map[k] else ""

            c.execute("""INSERT INTO ingredients
                (ingredient_id, name, category, base_attributes, has_caffeine, has_dairy,
                 sensory_tags, experience_tags, suitable_states, unsuitable_states,
                 health_constraints, suitable_scenes, visual_tags, source, notes)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (rid, g("name"), g("category"), g("base_attr"), g("caffeine"),
                 g("dairy"), g("sensory"), g("exp_tags"), g("suitable"),
                 g("unsuitable"), g("health"), g("scene"), g("visual"),
                 g("source"), g("notes")))
            count += 1

    conn.commit()
    conn.close()
    return count


def import_recipes():
    conn = get_conn()
    c = conn.cursor()
    count = 0
    csv_path = CSV_FILES["recipes"]
    if not os.path.exists(csv_path):
        print(f"[database] Warning: recipes CSV not found at {csv_path}")
        conn.close()
        return 0

    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader, None)

        col_map = {}
        for i, h in enumerate(header):
            h_clean = h.strip()
            if "recipe_id" in h_clean or h_clean == "recipe_id":
                col_map["id"] = i
            elif h_clean == "饮品名称":
                col_map["name"] = i
            elif h_clean == "饮品类型":
                col_map["type"] = i
            elif h_clean == "成分组合":
                col_map["combo"] = i
            elif h_clean == "成分角色":
                col_map["roles"] = i
            elif h_clean == "用量等级":
                col_map["dosage"] = i
            elif "适配身体状态" in h_clean:
                col_map["body"] = i
            elif "适配心情状态" in h_clean:
                col_map["mood"] = i
            elif h_clean == "感官标签":
                col_map["sensory"] = i
            elif h_clean == "体验标签":
                col_map["exp_tags"] = i
            elif h_clean == "健康约束":
                col_map["health"] = i
            elif h_clean == "适合场景":
                col_map["scene"] = i
            elif "甜度建议" in h_clean:
                col_map["sweetness"] = i
            elif "冷热建议" in h_clean:
                col_map["temp"] = i
            elif "制作复杂度" in h_clean:
                col_map["complexity"] = i
            elif "推荐解释" in h_clean:
                col_map["desc"] = i
            elif h_clean == "视觉标签":
                col_map["visual"] = i
            elif "可否机器制作" in h_clean:
                col_map["machine"] = i

        for row in reader:
            if not row or not row[col_map.get("id", 0)].strip():
                continue
            rid = row[col_map["id"]].strip()
            if not rid or not rid.startswith("R"):
                continue

            def g(k):
                return row[col_map[k]].strip() if k in col_map and len(row) > col_map[k] else ""

            c.execute("""INSERT INTO recipes
                (recipe_id, name, type, ingredients_combo, ingredient_roles, dosage_levels,
                 suitable_body, suitable_mood, sensory_tags, experience_tags,
                 health_constraints, suitable_scenes, sweetness, temperature,
                 complexity, description, visual_tags, can_machine_make)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (rid, g("name"), g("type"), g("combo"), g("roles"), g("dosage"),
                 g("body"), g("mood"), g("sensory"), g("exp_tags"),
                 g("health"), g("scene"), g("sweetness"), g("temp"),
                 g("complexity"), g("desc"), g("visual"), g("machine")))
            count += 1

    conn.commit()
    conn.close()
    return count


def seed_stores():
    """Seed default stores if table is empty."""
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM stores")
    if c.fetchone()[0] > 0:
        conn.close()
        return 0

    stores = [
        ("ST001", "华南理工大学店", "五山路381号", 0.256, 23.148, 113.353),
        ("ST002", "广东工业大学店", "大学城外环西路100号", 1.2, 23.045, 113.388),
        ("ST003", "万胜围店", "新港东路1233号", 6.8, 23.100, 113.370),
        ("ST004", "琶洲店", "阅江西路222号", 4.5, 23.109, 113.364),
    ]
    for sid, name, addr, dist, lat, lng in stores:
        c.execute("INSERT INTO stores (store_id, name, address, distance, latitude, longitude) VALUES (?,?,?,?,?,?)",
                  (sid, name, addr, dist, lat, lng))
    conn.commit()
    conn.close()
    return len(stores)


def get_db_state():
    conn = get_conn()
    c = conn.cursor()
    tables = {}
    for t in ["tag_dict", "ingredients", "recipes", "user_sessions",
              "recommendations", "feedback", "visual_mappings", "stores"]:
        c.execute(f"SELECT COUNT(*) FROM {t}")
        tables[t] = c.fetchone()[0]
    conn.close()
    return tables


if __name__ == "__main__":
    init_db()
    n_tags = import_tag_dict()
    n_ing = import_ingredients()
    n_rec = import_recipes()
    try:
        from seed_visual_mappings import seed_visual_mappings
    except ImportError:
        from backend.seed_visual_mappings import seed_visual_mappings
    n_vis = seed_visual_mappings()
    n_stores = seed_stores()
    print(f"Imported: {n_tags} tags, {n_ing} ingredients, {n_rec} recipes, {n_vis} visual mappings, {n_stores} stores")
    state = get_db_state()
    for t, c_val in state.items():
        print(f"  {t}: {c_val} rows")
