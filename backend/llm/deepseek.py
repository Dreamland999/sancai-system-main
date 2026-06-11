"""DeepSeek API integration for polishing recommendation text.

Uses real DeepSeek API by default. Falls back to template if API unavailable.
"""

try:
    from ..config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, LLM_MOCK_MODE
except ImportError:
    from config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, LLM_MOCK_MODE

SYSTEM_PROMPT = """你是一个饮品推荐助手。用户告诉你 ta 的身体状态、心情和场景，你为 ta 推荐饮品。

规则：
- 像朋友口吻，自然不做作，不用"亲""宝贝"
- 不写医疗功效词：养胃、助眠、治疗、缓解疲劳、提神醒脑
- 写真实体感：清清爽爽、喝完很舒服、困的时候来一杯刚好
- 2-3 句话，80 字以内
- 必须带健康提示：含咖啡因提醒、乳糖提醒等"""


def polish_recommendation(name, rtype, match_reason, description, health_notes, mock=None):
    """Polish a recommendation with DeepSeek or fallback template."""
    if mock is None:
        mock = LLM_MOCK_MODE

    if mock or not DEEPSEEK_API_KEY:
        return _template_polish(name, rtype, match_reason, description, health_notes)

    return _deepseek_polish(name, rtype, match_reason, description, health_notes)


def _template_polish(name, rtype, match_reason, description, health_notes):
    """Fallback template when API unavailable."""
    type_map = {
        "清爽型": "清爽解渴",
        "顺滑型": "顺滑可口",
        "提神型": "帮你清醒",
        "柔和型": "温和舒适",
        "香浓型": "浓香暖心",
    }
    feel = ""
    for k, v in type_map.items():
        if k in (rtype or ""):
            feel = v
            break
    if not feel:
        feel = "刚刚好"

    parts = [f"{name}，{feel}。"]

    if description:
        short = description.split("。")[0].rstrip("，。")
        if len(short) < 40:
            parts = [f"{name}，{short}。"]

    if health_notes:
        notes_text = "；".join(health_notes[:2])
        parts.append(f" 提示：{notes_text}")

    return "".join(parts)


def _deepseek_polish(name, rtype, match_reason, description, health_notes):
    """Call DeepSeek API for polished recommendation."""
    import requests

    health_str = "、".join(health_notes) if health_notes else "无特殊限制"

    user_msg = f"""推荐饮品：{name}（{rtype}）
匹配原因：{match_reason}
饮品描述：{description}
健康提示：{health_str}

请为这杯饮品写一段自然的推荐语："""

    try:
        resp = requests.post(
            f"{DEEPSEEK_BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_msg},
                ],
                "temperature": 0.8,
                "max_tokens": 200,
            },
            timeout=15,
        )
        if resp.status_code == 200:
            data = resp.json()
            return data["choices"][0]["message"]["content"].strip()
        else:
            print(f"[DeepSeek] API error {resp.status_code}: {resp.text[:200]}")
    except Exception as e:
        print(f"[DeepSeek] Exception: {e}")

    return _template_polish(name, rtype, match_reason, description, health_notes)
