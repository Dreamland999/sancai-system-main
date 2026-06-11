"""Two-tower style recall: compute tag overlap between user state and recipe.

Supports both tag IDs (BS001) and tag names (疲惫) via auto-conversion.
"""

_tag_id_to_name = None
_tag_name_to_id = None


def _load_tag_maps():
    global _tag_id_to_name, _tag_name_to_id
    if _tag_id_to_name is not None:
        return
    from ..database import get_conn
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT tag_id, name FROM tag_dict")
    _tag_id_to_name = {}
    _tag_name_to_id = {}
    for row in c.fetchall():
        _tag_id_to_name[row["tag_id"]] = row["name"]
        _tag_name_to_id[row["name"]] = row["tag_id"]
    conn.close()


def _to_tag_names(tags):
    """Convert a mix of tag IDs and tag names to a set of tag names."""
    _load_tag_maps()
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


def _extract_recipe_tag_set(recipe):
    """Extract all relevant tag NAMES from recipe fields into a set."""
    tags = set()
    for field in ("suitable_body", "suitable_mood", "experience_tags",
                  "suitable_scenes", "sensory_tags"):
        val = recipe[field] or ""
        for t in val.replace("；", "、").replace(";", "、").split("、"):
            t = t.strip().rstrip("。，,.")
            if t:
                tags.add(t)
    return tags


def recall_candidates(recipes, body_states, mood_states, scene, experience_needs):
    """Score all recipes by tag overlap with user state and return Top-N.

    Uses Jaccard-like overlap: |user_tags ∩ recipe_tags| / max(|user_tags|, 1)

    Args:
        recipes: list of recipe Row objects
        body_states: BS tag IDs or names
        mood_states: MS tag IDs or names
        scene: CT tag ID or name
        experience_needs: EX tag IDs or names

    Returns:
        List of (recipe, overlap_score) sorted by score, Top-30
    """
    if isinstance(scene, list):
        scene = scene[0] if scene else ""
    scene = scene or ""

    user_tags = _to_tag_names(body_states)
    user_tags |= _to_tag_names(mood_states)
    user_tags |= _to_tag_names(experience_needs)
    scene_names = _to_tag_names([scene]) if scene else set()
    user_tags |= scene_names

    if not user_tags:
        return [(r, 0.0) for r in recipes]

    scored = []
    for r in recipes:
        recipe_tags = _extract_recipe_tag_set(r)
        overlap = len(user_tags & recipe_tags)
        if overlap == 0:
            scored.append((r, 0.0))
        else:
            jaccard = overlap / max(len(user_tags), 1)
            scored.append((r, jaccard))

    scored.sort(key=lambda x: x[1], reverse=True)
    from ..config import RECALL_SIZE
    return scored[:RECALL_SIZE]

