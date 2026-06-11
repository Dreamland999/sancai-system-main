"""Generate match reasons and visual prompts for a recommendation."""


def generate_explanation(recipe, dim_scores, body_states, mood_states, scene, restrictions):
    """Generate a short match reason based on the dimension scores.

    Returns a concise Chinese string explaining why this drink fits.
    """
    reasons = []

    if dim_scores.get("state_match", 0) >= 0.6:
        reasons.append("状态匹配度高")
    if dim_scores.get("flavor", 0) >= 0.5:
        sensory = recipe["sensory_tags"] or ""
        if sensory:
            tags = [t.strip() for t in sensory.split(",") if t.strip()]
            if tags:
                reasons.append(f"风味{tags[0]}")

    if dim_scores.get("scene", 0) >= 0.5:
        reasons.append("场景适配")

    health = dim_scores.get("health", 0)
    if health >= 0.9:
        reasons.append("健康友好")
    elif health >= 0.7:
        reasons.append("无明显冲突")

    sweet = recipe["sweetness"] or ""
    if sweet:
        reasons.append(sweet)

    temp = recipe["temperature"] or ""
    if temp:
        reasons.append(temp)

    result = "，".join(reasons[:4])
    if not result:
        result = recipe["description"] or "适合当前状态"
    return result


def build_health_notes(recipe):
    """Extract health warnings from recipe constraints."""
    hc = recipe["health_constraints"] or ""
    if not hc:
        return []
    notes = []
    tag_text = hc.lower()
    if "胃敏感" in tag_text:
        notes.append("胃敏感慎用")
    if "咖啡因" in tag_text:
        notes.append("含咖啡因，敏感人群慎用")
    if "乳糖" in tag_text:
        notes.append("含乳制品")
    if "控糖" in tag_text:
        notes.append("甜度偏高，控糖慎选")
    if "过敏" in tag_text:
        notes.append("含过敏风险成分")
    if "夜间" in tag_text:
        notes.append("夜间慎用")
    return notes


def build_visual_prompt(recipe, user_body=None, user_mood=None, user_scene=None):
    """Build a structured visual generation prompt from recipe and user tags.

    Looks up visual_mappings table for exact color palettes and graphic elements.
    Merges recipe visual tags with user state visual mappings for richer results.
    """
    from ..database import get_conn
    conn = get_conn()
    c = conn.cursor()

    all_source_tags = set()

    recipe_tags = recipe["visual_tags"] or ""
    for t in _split_tags(recipe_tags):
        all_source_tags.add(t)

    for tags in (user_body or [], user_mood or [], [user_scene] if user_scene else []):
        for t in _split_tags(tags):
            all_source_tags.add(t)

    if not all_source_tags:
        conn.close()
        return ""

    colors = []
    graphics = []
    compositions = []
    styles = []

    query_tags = list(all_source_tags)
    for tag in query_tags:
        # Try exact tag_id match first
        c.execute("""SELECT color_palette, graphics, composition, reference_style
            FROM visual_mappings WHERE source_tag_id = ?""", (tag,))
        row = c.fetchone()
        # If not found, try matching by tag name (for Chinese names like 冷色, 气泡 etc.)
        if not row:
            c.execute("""SELECT color_palette, graphics, composition, reference_style
                FROM visual_mappings WHERE source_tag_id IN
                (SELECT tag_id FROM tag_dict WHERE name = ?)""", (tag,))
            row = c.fetchone()
        # If still not found, try partial name match in tag_dict
        if not row:
            c.execute("""SELECT vm.color_palette, vm.graphics, vm.composition, vm.reference_style
                FROM visual_mappings vm JOIN tag_dict td ON vm.source_tag_id = td.tag_id
                WHERE td.name LIKE ?""", (f"%{tag}%",))
            row = c.fetchone()
        if row:
            if row["color_palette"]:
                colors.extend(row["color_palette"].split())
            if row["graphics"]:
                graphics.append(row["graphics"])
            if row["composition"]:
                compositions.append(row["composition"])
            if row["reference_style"]:
                styles.append(row["reference_style"])

    if not colors and not graphics:
        c.execute("SELECT color_palette, graphics FROM visual_mappings WHERE source_tag_id LIKE ?",
                  (f"VI%",))
        for row in c.fetchall():
            if row["color_palette"]:
                colors.extend(row["color_palette"].split()[:2])
            if row["graphics"]:
                graphics.append(row["graphics"])
    conn.close()

    unique_colors = list(dict.fromkeys(colors))[:5]
    unique_graphics = list(dict.fromkeys(graphics))[:4]
    unique_compositions = list(dict.fromkeys(compositions))[:2]
    unique_styles = list(dict.fromkeys(styles))[:2]

    name = recipe["name"] or "饮品"
    rtype = recipe["type"] or "清爽型"

    prompt_parts = [f"饮品名称：{name}", f"饮品风格：{rtype}"]
    if unique_colors:
        prompt_parts.append(f"色板约束（HEX）：{'、'.join(unique_colors)}")
    if unique_graphics:
        prompt_parts.append(f"图形元素：{'；'.join(unique_graphics)}")
    if unique_compositions:
        prompt_parts.append(f"构图方式：{'；'.join(unique_compositions)}")
    if unique_styles:
        prompt_parts.append(f"风格参考：{'；'.join(unique_styles)}")
    prompt_parts.extend([
        "禁止：复杂3D渲染、写实照片风格、多文字排版、真实人像",
    ])
    return "\n".join(prompt_parts)


def _split_tags(tags):
    if not tags:
        return []
    if isinstance(tags, str):
        return [t.strip() for t in tags.replace("；", "、").replace(";", "、").split("、")
                if t.strip().rstrip("。，,.")]
    if isinstance(tags, list):
        result = []
        for t in tags:
            result.extend(_split_tags(t))
        return result
    return []
