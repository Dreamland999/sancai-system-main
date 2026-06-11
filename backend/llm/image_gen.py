"""通义万相 Wan2.7-Image API integration for visual generation.

Uses DashScope multimodal-generation endpoint.
Supports both real API calls and mock mode for testing.
"""

import json
import time
try:
    from ..config import WANXIANG_API_KEY, IMAGE_MOCK_MODE
except ImportError:
    from config import WANXIANG_API_KEY, IMAGE_MOCK_MODE

WANXIANG_ENDPOINT = "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation"


def generate_image(visual_prompt, mock=None):
    """Generate an image via 通义万相 Wan2.7-Image.

    Args:
        visual_prompt: structured prompt string from explain.build_visual_prompt()
        mock: override IMAGE_MOCK_MODE. None = use config default.

    Returns:
        dict with keys: status, image_url, prompt, task_id
    """
    if mock is None:
        mock = IMAGE_MOCK_MODE

    if mock or not WANXIANG_API_KEY:
        return {"status": "mock", "image_url": None, "prompt": visual_prompt, "task_id": None}

    return _call_wanxiang(visual_prompt)


def _call_wanxiang(visual_prompt):
    """Call 通义万相 Wan2.7-Image via DashScope multimodal generation API."""
    import requests

    image_prompt = _build_prompt(visual_prompt)

    payload = {
        "model": "wan2.7-image",
        "input": {
            "messages": [{
                "role": "user",
                "content": [{"text": image_prompt}],
            }],
        },
        "parameters": {
            "size": "2K",
            "n": 1,
            "watermark": False,
        },
    }

    try:
        resp = requests.post(
            WANXIANG_ENDPOINT,
            headers={
                "Authorization": f"Bearer {WANXIANG_API_KEY}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=60,
        )
        if resp.status_code == 200:
            data = resp.json()
            choices = data.get("output", {}).get("choices", [])
            if choices:
                url = choices[0].get("message", {}).get("content", [{}])[0].get("image", "")
                if url:
                    return {"status": "generated", "image_url": url, "prompt": image_prompt, "task_id": None}
            results = data.get("output", {}).get("results", [])
            if results:
                return {"status": "generated", "image_url": results[0].get("url", ""), "prompt": image_prompt, "task_id": None}
            return {"status": "completed", "image_url": None, "prompt": image_prompt, "task_id": data.get("request_id", "")}

        print(f"[Wanxiang] API error {resp.status_code}: {resp.text[:200]}")
    except Exception as e:
        print(f"[Wanxiang] Exception: {e}")

    return {"status": "error", "image_url": None, "prompt": image_prompt, "task_id": None}


def _build_prompt(structured_prompt):
    """Convert structured visual prompt to a concise natural description."""
    if not structured_prompt:
        return "一杯现代茶饮，简约设计风格，干净背景，柔和色调，无文字"
    # Take first 800 chars, Wan2.7 handles it well
    return structured_prompt.strip()[:800]
