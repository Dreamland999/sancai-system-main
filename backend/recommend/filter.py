"""Hard-constraint filtering. Removes recipes that conflict with user health limitations."""

LACTOSE_INGREDIENTS = ["牛奶", "鲜奶", "酸奶", "奶盖", "芝士", "淡奶油", "炼乳", "奶泡", "乳酸菌"]
HIGH_CAFFEINE = ["咖啡", "浓缩咖啡", "美式咖啡液", "抹茶"]
STRONG_ACID = ["柠檬", "百香果", "青柠", "菠萝", "洛神花"]
STRONG_BUBBLE = ["气泡水", "苏打水"]


def filter_by_constraints(recipes, restrictions, scene, body_states):
    """Filter recipes by hard health constraints and scene rules.

    Args:
        recipes: list of recipe dicts from DB (Row objects)
        restrictions: list of HC tag IDs, e.g. ['HC001', 'HC002']
        body_states: list of BS tag IDs, e.g. ['BS005', 'BS006']
        scene: CT tag ID like 'CT003' or list

    Returns:
        Filtered list of recipe dicts
    """
    if isinstance(scene, list):
        scene = scene[0] if scene else ""

    hard_filters = _resolve_filters(restrictions, body_states)
    filtered = []
    for r in recipes:
        if _passes_filter(r, hard_filters, scene):
            filtered.append(r)
    return filtered


def _resolve_filters(restrictions, body_states):
    """Map HC tags and BS tags to concrete exclusion rules."""
    filters = set()
    all_tags = set(restrictions or []) | set(body_states or [])
    for tag in all_tags:
        tag_upper = tag.upper()
        if tag_upper in ("BS005", "HC008", "HC003"):
            filters.add("no_dairy")
        if tag_upper in ("BS006", "HC007", "HC002"):
            filters.add("no_high_caffeine")
        if tag_upper in ("BS004", "HC005", "HC004"):
            filters.add("no_harsh")
        if tag_upper in ("BS007", "HC009", "HC001"):
            filters.add("low_sugar")
        if tag_upper == "HC010":
            filters.add("no_allergen")
        if tag_upper == "HC006":
            filters.add("no_nighttime_risk")
    return filters


def _passes_filter(recipe, hard_filters, scene):
    health_tags = (recipe["health_constraints"] or "").lower()

    if "no_dairy" in hard_filters:
        combo = recipe["ingredients_combo"] or ""
        has_dairy = any(d in combo for d in LACTOSE_INGREDIENTS)
        if has_dairy:
            return False

    if "no_high_caffeine" in hard_filters:
        combo = recipe["ingredients_combo"] or ""
        has_high = any(c in combo for c in HIGH_CAFFEINE)
        if has_high:
            return False

    if "no_harsh" in hard_filters:
        if "胃敏感慎用" in health_tags or "胃敏感" in health_tags:
            return False
        combo = recipe["ingredients_combo"] or ""
        if any(a in combo for a in STRONG_ACID):
            return False
        if any(b in combo for b in STRONG_BUBBLE) and any(
            a in combo for a in STRONG_ACID
        ):
            return False

    if "low_sugar" in hard_filters:
        sweetness = (recipe["sweetness"] or "").lower()
        if "高糖" in sweetness:
            return False

    if "no_allergen" in hard_filters:
        combo = recipe["ingredients_combo"] or ""
        has_nut = any(n in combo for n in ["杏仁", "坚果"])
        has_honey = "蜂蜜" in combo
        if has_nut or has_honey:
            return False

    if "no_nighttime_risk" in hard_filters:
        if "夜间慎用" in health_tags:
            return False

    if scene and scene.upper() == "CT003":
        if "夜间慎用" in health_tags:
            return False
        combo = recipe["ingredients_combo"] or ""
        if any(c in combo for c in HIGH_CAFFEINE):
            return False

    return True
