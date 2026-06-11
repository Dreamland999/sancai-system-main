"""Fine-ranking: compute 5-dimension scores and rank Top-K.

Supports both tag IDs and tag names.
"""

_tag_id_to_name = None


def _load_tag_map():
    global _tag_id_to_name
    if _tag_id_to_name is not None:
        return
    from ..database import get_conn
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT tag_id, name FROM tag_dict")
    _tag_id_to_name = {}
    for row in c.fetchall():
        _tag_id_to_name[row["tag_id"]] = row["name"]
    conn.close()


def _to_tag_names(tags):
    """Convert mixed tag IDs and tag names to a set of tag names."""
    _load_tag_map()
    result = set()
    if not tags:
        return result
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",") if t.strip()]
    for t in tags:
        t = t.strip()
        if not t:
            continue
        if t in _tag_id_to_name:
            result.add(_tag_id_to_name[t])
        else:
            result.add(t)
    return result


def _extract_field_tags(val):
    """Extract tag names from a recipe field value (Chinese-separated text)."""
    if not val:
        return set()
    tags = set()
    for t in val.replace("；", "、").replace(";", "、").split("、"):
        t = t.strip().rstrip("。，,.")
        if t:
            tags.add(t)
    return tags


def _score_overlap(recipe, field, user_set):
    """Score tag overlap between recipe field and user tag set (0.0-1.0)."""
    recipe_tags = _extract_field_tags(recipe[field] or "")
    if not recipe_tags or not user_set:
        return 0.0
    overlap = len(recipe_tags & user_set)
    if overlap == 0:
        return 0.0
    return min(overlap / max(len(user_set), 1), 1.0)


def rank_candidates(scored_recipes, body_states, mood_states, scene,
                    experience_needs, restrictions, top_k=3):
    """Score each candidate on 5 dimensions and return Top-K.

    Dimensions:
        1. State match: body + mood + experience overlap
        2. Flavor: sensory tag overlap
        3. Scene: scene tag overlap
        4. Health: fewer constraint warnings = higher score
        5. Visual: visual tag overlap (placeholder)

    Formula: state×0.30 + flavor×0.20 + scene×0.15 + health×0.25 + visual×0.10
    """
    from ..config import SCORE_WEIGHTS, TOP_K
    top_k = top_k or TOP_K

    user_state_tags = (_to_tag_names(body_states) | _to_tag_names(mood_states)
                       | _to_tag_names(experience_needs))
    restriction_tags = _to_tag_names(restrictions)
    scene_set = _to_tag_names([scene] if isinstance(scene, str) else (scene or []))

    results = []
    for recipe, _overlap in scored_recipes:
        dims = {}

        body_match = _score_overlap(recipe, "suitable_body", user_state_tags)
        mood_match = _score_overlap(recipe, "suitable_mood", user_state_tags)
        exp_match = _score_overlap(recipe, "experience_tags", user_state_tags)
        dims["state_match"] = max(body_match, mood_match, exp_match)

        dims["flavor"] = _score_overlap(recipe, "sensory_tags", user_state_tags)
        if dims["flavor"] == 0:
            recipe_flav = _extract_field_tags(recipe["sensory_tags"] or "")
            overlap = len(recipe_flav & user_state_tags)
            dims["flavor"] = min(overlap / max(len(user_state_tags), 1), 1.0)

        dims["scene"] = _score_overlap(recipe, "suitable_scenes", scene_set)

        dims["health"] = _health_score(recipe, restriction_tags, scene_set)

        dims["visual"] = _score_overlap(recipe, "visual_tags", user_state_tags)
        if dims["visual"] == 0:
            dims["visual"] = 0.5

        total = (dims["state_match"] * SCORE_WEIGHTS["state_match"]
               + dims["flavor"] * SCORE_WEIGHTS["flavor"]
               + dims["scene"] * SCORE_WEIGHTS["scene"]
               + dims["health"] * SCORE_WEIGHTS["health"]
               + dims["visual"] * SCORE_WEIGHTS["visual"])

        results.append((recipe, round(total, 4), dims))

    results.sort(key=lambda x: x[1], reverse=True)
    return results[:top_k]


def _health_score(recipe, restriction_names, scene_set):
    """Score health compatibility. 1.0 = fully compatible."""
    hc_text = recipe["health_constraints"] or ""
    health_tags = _extract_field_tags(hc_text)
    if not health_tags:
        return 1.0

    penalty = 0.0
    for h in health_tags:
        h_lower = h.lower()
        if any(w in h_lower for w in ("胃敏感", "hc005")):
            penalty += 0.15
        if any(w in h_lower for w in ("控糖", "hc009")):
            penalty += 0.1
        if any(w in h_lower for w in ("咖啡因", "hc007")):
            penalty += 0.1
        if any(w in h_lower for w in ("乳糖", "hc008")):
            penalty += 0.1
        if any(w in h_lower for w in ("过敏", "hc010")):
            penalty += 0.1
        if any(w in h_lower for w in ("夜间", "hc006")):
            night_scene = any("夜间" in s for s in scene_set)
            if night_scene:
                penalty += 0.2

    return max(0.0, 1.0 - penalty)
