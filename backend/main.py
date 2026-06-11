from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BACKEND_DIR.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from config import TOP_K

# ─── Service & DB imports ────────────────────────────────
try:
    from backend.recommender_service import RecommenderService
    from backend.schemas import (
        ChatRequest, ChatResponse,
        FeedbackRequest, FeedbackResponse,
        ImageGenerateRequest, ImageGenerateResponse,
        IntentParseRequest, IntentParseResponse,
        OptionsResponse, RecommendItem, RecommendResponse,
        StoreItem, StoreListResponse,
        StateInferRequest, StateInferResponse,
        UserStateRequest,
    )
    from backend.database import get_conn, init_db, seed_stores
except ImportError:
    from recommender_service import RecommenderService
    from schemas import (
        ChatRequest, ChatResponse,
        FeedbackRequest, FeedbackResponse,
        ImageGenerateRequest, ImageGenerateResponse,
        IntentParseRequest, IntentParseResponse,
        OptionsResponse, RecommendItem, RecommendResponse,
        StoreItem, StoreListResponse,
        StateInferRequest, StateInferResponse,
        UserStateRequest,
    )
    from database import get_conn, init_db, seed_stores

app = FastAPI(title="Sancai AI Herbal Drink", version="1.0.0")

# Serve static files for miniapp resources (video, etc.)
STATIC_DIR = BACKEND_DIR.parent / "miniapp" / "static"
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Serve video files from backend/static/video (not bundled in miniapp)
VIDEO_DIR = BACKEND_DIR / "static" / "video"
if VIDEO_DIR.exists():
    app.mount("/video", StaticFiles(directory=str(VIDEO_DIR)), name="video")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

service = RecommenderService()


@app.on_event("startup")
def startup():
    init_db()
    seed_stores()

    # LLM config log (safe, no key)
    try:
        from config import LLM_MOCK_MODE, DEEPSEEK_MODEL, DEEPSEEK_API_KEY
    except ImportError:
        from backend.config import LLM_MOCK_MODE, DEEPSEEK_MODEL, DEEPSEEK_API_KEY
    key_loaded = bool(DEEPSEEK_API_KEY and DEEPSEEK_API_KEY != "")
    print(f"[Startup] LLM_MOCK_MODE={LLM_MOCK_MODE}")
    print(f"[Startup] DEEPSEEK_MODEL={DEEPSEEK_MODEL}")
    print(f"[Startup] DEEPSEEK_API_KEY loaded={key_loaded}")
    if LLM_MOCK_MODE:
        print("[Startup] WARNING: Mock mode ON, all LLM calls use fallback. Set LLM_MOCK_MODE=false in .env to enable real DeepSeek.")


# ─── Health ───────────────────────────────────────────────

@app.get("/api/health")
def health() -> Dict[str, str]:
    return {"status": "ok", "message": "Sancai AI backend v1.0"}


# ─── Options ──────────────────────────────────────────────

@app.get("/api/options", response_model=OptionsResponse)
def options() -> OptionsResponse:
    return service.get_options()


# ─── Recommend (core: dual-tower + MLP + DeepSeek polish) ─

@app.post("/api/recommend", response_model=RecommendResponse)
def recommend(payload: UserStateRequest) -> Dict[str, Any]:
    try:
        result = service.recommend(payload)
        return result
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


# ─── Feedback (dual-write: SQLite + JSONL) ────────────────

@app.post("/api/feedback", response_model=FeedbackResponse)
def feedback(payload: FeedbackRequest) -> FeedbackResponse:
    return service.save_feedback(payload)


# ─── Recipes ──────────────────────────────────────────────

@app.get("/api/recipes")
def list_recipes(search: Optional[str] = None, type: Optional[str] = None, limit: int = 20):
    conn = get_conn()
    c = conn.cursor()
    query = "SELECT * FROM recipes WHERE 1=1"
    params = []
    if search:
        query += " AND name LIKE ?"
        params.append(f"%{search}%")
    if type:
        query += " AND type LIKE ?"
        params.append(f"%{type}%")
    query += " LIMIT ?"
    params.append(limit)
    c.execute(query, params)
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return {"count": len(rows), "recipes": rows}


@app.get("/api/recipes/{recipe_id}")
def get_recipe(recipe_id: str):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM recipes WHERE recipe_id = ?", (recipe_id,))
    row = c.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return dict(row)


# ─── Tags ─────────────────────────────────────────────────

@app.get("/api/tags")
def list_tags(category: Optional[str] = None):
    conn = get_conn()
    c = conn.cursor()
    if category:
        c.execute("SELECT * FROM tag_dict WHERE category LIKE ?", (f"%{category}%",))
    else:
        c.execute("SELECT * FROM tag_dict")
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return {"count": len(rows), "tags": rows}


# ─── Ingredients ─────────────────────────────────────────

@app.get("/api/ingredients")
def list_ingredients(category: Optional[str] = None, limit: int = 80):
    conn = get_conn()
    c = conn.cursor()
    if category:
        c.execute("SELECT * FROM ingredients WHERE category LIKE ? LIMIT ?",
                  (f"%{category}%", limit))
    else:
        c.execute("SELECT * FROM ingredients LIMIT ?", (limit,))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return {"count": len(rows), "ingredients": rows}


# ─── History ──────────────────────────────────────────────

@app.get("/api/history/{user_id}")
def get_history(user_id: str, limit: int = 20):
    conn = get_conn()
    c = conn.cursor()
    if user_id == "default":
        c.execute("""SELECT r.*, rec.name, rec.type FROM recommendations r
            JOIN recipes rec ON r.recipe_id = rec.recipe_id
            ORDER BY r.created_at DESC LIMIT ?""", (limit,))
    else:
        c.execute("""SELECT r.*, rec.name, rec.type FROM recommendations r
            JOIN recipes rec ON r.recipe_id = rec.recipe_id
            JOIN user_sessions s ON r.session_id = s.session_id
            WHERE s.user_id = ? ORDER BY r.created_at DESC LIMIT ?""",
            (user_id, limit))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return {"count": len(rows), "history": rows}


# ─── Image Generate (通义万相) ─────────────────────────────

@app.post("/api/image/generate", response_model=ImageGenerateResponse)
def generate_image(payload: ImageGenerateRequest):
    try:
        from llm.image_gen import generate_image as gen_img
    except ImportError:
        from backend.llm.image_gen import generate_image as gen_img

    result = gen_img(payload.visual_prompt)
    return ImageGenerateResponse(
        status=result["status"],
        image_url=result.get("image_url"),
        prompt=result["prompt"],
        task_id=result.get("task_id"),
    )


# ─── Chat (DeepSeek AI dialogue) ──────────────────────────

@app.post("/api/chat", response_model=ChatResponse)
def chat(payload: ChatRequest):
    try:
        from llm.deepseek import _deepseek_polish
    except ImportError:
        from backend.llm.deepseek import _deepseek_polish

    try:
        from config import LLM_MOCK_MODE
    except ImportError:
        from backend.config import LLM_MOCK_MODE

    if LLM_MOCK_MODE:
        print("[Chat] LLM_MOCK_MODE=true, returning mock reply")
        return ChatResponse(
            reply="我在这里陪你梳理状态和偏好。你现在身体感觉怎么样？有没有特别想喝的冷暖口味？",
            session_id="CHAT_MOCK_001",
        )

    try:
        import requests
        from config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, DEEPSEEK_MODEL

        system_prompt = """你是一个叫"小才"的AI状态理解助手，负责帮用户梳理身体状态、心情和饮用偏好。
你的职责是追问和整理用户状态，不是推荐饮品。
严禁输出任何具体饮品名、配方名、茶名、饮品名称（如"薄荷茶""菊花茶""茉莉茶"等）。
只允许：追问身体感觉、追问心情、追问冷热/口味偏好、总结已确认的状态。
回复自然温暖，2-3句话，80字以内。"""

        resp = requests.post(
            f"{DEEPSEEK_BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": DEEPSEEK_MODEL,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": payload.message},
                ],
                "temperature": 0.8,
                "max_tokens": 200,
            },
            timeout=15,
        )
        if resp.status_code == 200:
            data = resp.json()
            reply = data["choices"][0]["message"]["content"].strip()
            return ChatResponse(reply=reply, session_id="CHAT_001")
        else:
            return ChatResponse(
                reply="抱歉，我暂时无法回复，请稍后再试~",
                session_id=None,
            )
    except Exception as e:
        print(f"[Chat] DeepSeek error: {e}")
        return ChatResponse(
            reply="让我想想…你今天想喝点什么感觉的饮品呢？清爽解渴还是温暖放松？",
            session_id="CHAT_FALLBACK",
        )


# ─── Emotion ──────────────────────────────────────────────


@app.post("/api/emotion/predict")
async def predict_emotion(file: UploadFile = File(...)):
    """上传人脸图片，返回情绪分析结果。

    接收 multipart/form-data，字段名: file
    返回: { success, emotion, emotion_cn, confidence, scores, message }
    """
    try:
        from emotion_service import get_service
    except ImportError:
        from backend.emotion_service import get_service

    image_bytes = await file.read()
    service = get_service()
    return service.predict(image_bytes)


# ─── Stores ───────────────────────────────────────────────

# ─── Intent Parse (chat message → recommend tags) ──────────

KEYWORD_RULES = [
    # body
    (["睡不好","困","想睡","没睡好","犯困","好困","昏昏沉沉"], "body", "困倦"),
    (["累","疲惫","没力气","没精神","好累","乏","精疲力尽"], "body", "疲劳"),
    (["状态很好","身体良好","没啥不舒服","感觉不错","我很好","精神不错","状态不错","身体不错"], "body", "良好"),
    (["饿","饥饿","肚子饿","没吃饭","空腹"], "body", "饥饿"),
    (["饱","吃饱","吃撑","吃太饱"], "body", "饱腹"),
    (["有点热","感觉热","很热","好热","太热","出汗"], "body", "感觉有点热"),
    (["有点冷","感觉冷","很冷","好冷","太冷","冻"], "body", "感觉有点冷"),
    (["渴","口干","想喝水","口渴","缺水"], "body", "口渴"),
    # mood
    (["开心","高兴","愉快","快乐","挺好的","挺好的呀","哈哈"], "mood", "开心"),
    (["平静","还行","还可以","一般般","不好不坏","没啥情绪"], "mood", "平静"),
    (["兴奋","激动","期待","太好","哇","燃"], "mood", "兴奋"),
    (["低落","不开心","沮丧","难过","抑郁","emo"], "mood", "低落"),
    (["烦","烦躁","烦死了","烦闷","心浮气躁","毛躁"], "mood", "烦躁"),
    (["紧张","焦虑","慌","不安","压力","担心"], "mood", "紧张"),
    (["无聊","没什么意思","没事干","闷","闲"], "mood", "无聊"),
    (["孤单","孤独","寂寞","一个人"], "mood", "孤单"),
    # scene
    (["家","家里","在家","宿舍","寝室","房间"], "scene", "家/宿舍"),
    (["学校","教学楼","上课","教室","课堂"], "scene", "学校/教学楼"),
    (["图书馆","自习室","自习","看书","学习区"], "scene", "图书馆/自习室"),
    (["办公室","公司","上班","工位","开会"], "scene", "办公室/公司"),
    (["餐厅","食堂","吃饭","就餐","饭堂"], "scene", "餐厅/食堂"),
    (["健身房","运动场","操场","锻炼","健身"], "scene", "健身房/运动场"),
    (["咖啡店","奶茶店","喝咖啡","喝奶茶"], "scene", "咖啡店/奶茶店"),
    (["公园","户外","外面","野餐","散步"], "scene", "公园/户外"),
    # needs
    (["放松","安神","助眠","休息","静一静"], "needs", "安神"),
    (["提神","精神","清醒","醒脑","醒了"], "needs", "提神"),
    (["解暑","清凉","降温","消暑"], "needs", "解暑"),
    (["暖身","暖一点","暖和","驱寒"], "needs", "暖身"),
    # scene fix
    (["商场","逛街","购物","商业区","mall"], "scene", "商场/商业街"),
    (["地铁","公交","车站","通勤","路上","坐车"], "scene", "地铁/公交/车站"),
    # flavor
    (["清爽","清淡"], "flavor_preference", "清爽"),
    (["奶香","奶味","牛奶","奶盖"], "flavor_preference", "奶香"),
    (["茶香","茶味","茶底"], "flavor_preference", "茶香"),
    (["果香","果味","水果"], "flavor_preference", "果香"),
    (["花香","花的味道","花味","花茶"], "flavor_preference", "花香"),
    (["咖啡香","咖啡"], "flavor_preference", "咖啡香"),
    (["酸","酸感","柠檬","青柠","微酸"], "flavor_preference", "酸感"),
    (["甜","甜感","蜂蜜","甜食"], "flavor_preference", "甜感"),
    (["苦","苦感","微苦"], "flavor_preference", "苦感"),
    (["气泡","气泡感","汽水","碳酸"], "flavor_preference", "气泡感"),
    # temperature (互斥)
    (["热一点","温热","热饮","暖的","想喝热的","热"], "temperature_preference", "热饮"),
    (["冰","冷饮","加冰","冰的","想喝冷的","想喝冰","冷","凉"], "temperature_preference", "冷饮"),
    (["常温","不冰不热","温的就行"], "temperature_preference", "常温"),
    # limits
    (["低糖","控糖","少糖","不甜","不要太甜","少甜"], "limits", "低糖"),
    (["低刺激","不刺激","温和","不要太刺激"], "limits", "低刺激"),
    (["咖啡因敏感","咖啡因过敏","不喝咖啡","不要咖啡因","无咖啡因"], "limits", "咖啡因敏感慎用"),
    (["乳糖不耐","不喝奶","不要奶","不含乳"], "limits", "乳糖不耐慎用"),
    (["过敏","过敏原","坚果过敏"], "limits", "过敏风险"),
]


def _keyword_parse(message: str) -> dict:
    """关键词匹配，返回 7 类标签数组。"""
    result = {k: [] for k in [
        "scene", "body", "mood", "needs", "limits",
        "flavor_preference", "temperature_preference",
    ]}
    text = message.lower()
    for keywords, field, value in KEYWORD_RULES:
        for kw in keywords:
            if kw.lower() in text:
                if value not in result[field]:
                    result[field].append(value)
                break
    return result


@app.post("/api/intent/parse", response_model=IntentParseResponse)
def parse_intent(payload: IntentParseRequest):
    """从用户聊天消息中解析推荐标签。

    优先调 DeepSeek，失败/未配置时走关键词 fallback。
    """
    try:
        from config import LLM_MOCK_MODE
    except ImportError:
        from backend.config import LLM_MOCK_MODE

    # 真实 DeepSeek 模式：请求大模型返回 JSON
    if not LLM_MOCK_MODE:
        try:
            import requests
            from config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, DEEPSEEK_MODEL

            system_prompt = """你是一个饮品推荐标签解析器。根据用户的话，输出以下 7 个数组（只输出 JSON，不要解释）：
{"scene":[],"body":[],"mood":[],"needs":[],"limits":[],"flavor_preference":[],"temperature_preference":[]}
body 可选值：良好、饥饿、饱腹、口渴、疲劳、感觉有点冷、感觉有点热、困倦
mood 可选值：开心、平静、兴奋、低落、烦躁、紧张、无聊、孤单
scene 可选值：家/宿舍、学校/教学楼、图书馆/自习室、办公室/公司、餐厅/食堂、健身房/运动场、咖啡店/奶茶店、商场/商业街、地铁/公交/车站、公园/户外
needs 可选值：安神、提神、放松、解暑、暖身
flavor_preference 可选值：清爽、奶香、茶香、果香、花香、咖啡香、酸感、甜感、苦感、气泡感
temperature_preference 可选值：热饮、冷饮、常温
limits 可选值：低糖、低刺激、咖啡因敏感慎用、乳糖不耐慎用、过敏风险"""

            resp = requests.post(
                f"{DEEPSEEK_BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": DEEPSEEK_MODEL,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": payload.message},
                    ],
                    "temperature": 0.3,
                    "max_tokens": 300,
                },
                timeout=10,
            )
            if resp.status_code == 200:
                import json
                data = resp.json()
                raw = data["choices"][0]["message"]["content"].strip()
                # 尝试从回复中提取 JSON
                if "{" in raw and "}" in raw:
                    start = raw.index("{")
                    end = raw.rindex("}") + 1
                    parsed = json.loads(raw[start:end])
                    return IntentParseResponse(**parsed)
        except Exception as e:
            print(f"[Intent] DeepSeek parse failed, fallback keyword: {e}")

    # 关键词 fallback
    tags = _keyword_parse(payload.message)
    return IntentParseResponse(**tags)


@app.get("/api/stores", response_model=StoreListResponse)
def list_stores():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM stores ORDER BY distance ASC")
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    stores = [
        StoreItem(
            store_id=r["store_id"],
            name=r["name"],
            address=r.get("address", ""),
            distance=r.get("distance", 0.0),
            is_open=bool(r.get("is_open", 1)),
        )
        for r in rows
    ]
    return StoreListResponse(stores=stores)


# ─── State Infer (AI 状态推理) ─────────────────────────────

STATE_INFER_SYSTEM = """你是一个饮品推荐状态推测助手。只做状态标签整理，不推荐具体饮品。

输出规则：
1. 只输出一个 JSON，不要解释。
2. JSON 格式：{"summary":"<80字确认话术，严禁包含任何饮品名、茶名、配方名>","state_guess":{"scene":[],"body":[],"mood":[],"needs":[],"limits":[],"flavor_preference":[],"temperature_preference":[]}}
3. body 可选值（最多2个）：良好、饥饿、饱腹、口渴、疲劳、感觉有点冷、感觉有点热、困倦
4. mood 可选值（最多2个）：开心、平静、兴奋、低落、烦躁、紧张、无聊、孤单
5. needs 可选值（最多2个）：安神、提神、放松、解暑、暖身
6. flavor_preference 可选值（最多2个）：清爽、奶香、茶香、果香、花香、咖啡香、酸感、甜感、苦感、气泡感
7. temperature_preference 可选值（最多1个，绝对互斥）：热饮、冷饮、常温
8. scene 可选值（最多1个）：家/宿舍、学校/教学楼、图书馆/自习室、办公室/公司、餐厅/食堂、健身房/运动场、咖啡店/奶茶店、商场/商业街、地铁/公交/车站、公园/户外
9. limits 可选值（最多2个）：低糖、低刺激、咖啡因敏感慎用、乳糖不耐慎用、过敏风险
10. mood 优先级：recommend_input.mood 非空时必须原样保留，不要覆盖，不要合并 emotion_result。只有 recommend_input.mood 为空时，才使用 emotion_result.emotion_cn 映射到 mood。
11. recommend_input 已有字段为基础，与用户消息推测合并。
12. 用户没说冷热/口味偏好时，不要凭空添加。
13. time_of_day 只作参考，不自动生成 scene。
14. summary 语气友好，必须以 recommend_input.mood 为准描述心境（如果 recommend_input.mood 非空）；只有 mood 为空时才用 emotion_result。严禁包含任何饮品名称。"""


def _rule_state_infer(message: str, emotion_result: dict, recommend_input: dict,
                      user_profile: dict, context: dict) -> dict:
    """纯规则 fallback — 不依赖 LLM。"""
    state = {
        "scene": [],
        "body": [],
        "mood": [],
        "needs": [],
        "limits": [],
        "flavor_preference": [],
        "temperature_preference": [],
    }
    mi = recommend_input or {}
    up = user_profile or {}

    # 1. 保留已有 recommend_input 字段
    for f in state:
        if mi.get(f):
            state[f] = list(mi[f])

    # 2. mood 优先级：recommend_input.mood 非空 → 原样保留，不合并 emotion_result
    EMOTION_MOOD = {"开心": "开心", "平静": "平静", "低落": "低落",
                    "生气": "烦躁", "害怕": "紧张"}
    state_mood_empty = not state["mood"] or len(state["mood"]) == 0
    if state_mood_empty and emotion_result and emotion_result.get("emotion_cn"):
        cn = emotion_result["emotion_cn"]
        mapped = EMOTION_MOOD.get(cn)
        if mapped:
            state["mood"] = [mapped]

    # 3. 消息关键词推断
    text = message.lower()
    if any(kw in text for kw in ["睡不好","失眠","入睡","多梦","浅睡"]):
        if "失眠" not in state["body"]: state["body"].append("失眠")
        if "安神" not in state["needs"]: state["needs"].append("安神")
    if any(kw in text for kw in ["累","疲惫","没力气","乏力","没精神"]):
        if "乏力" not in state["body"]: state["body"].append("乏力")
    if any(kw in text for kw in ["焦虑","烦","烦躁","心慌","紧张"]):
        if "烦躁" not in state["mood"]: state["mood"].append("烦躁")
    if any(kw in text for kw in ["低落","不开心","沮丧","难过"]):
        if "低落" not in state["mood"]: state["mood"].append("低落")
    if any(kw in text for kw in ["放松","安神","助眠","休息"]):
        if "安神" not in state["needs"]: state["needs"].append("安神")
    if any(kw in text for kw in ["提神","精神","清醒","醒脑"]):
        if "提神" not in state["needs"]: state["needs"].append("提神")
    if any(kw in text for kw in ["热一点","温热","热饮","暖的","想喝热的"]):
        if "热饮" not in state["temperature_preference"]: state["temperature_preference"].append("热饮")
    if any(kw in text for kw in ["不甜","少糖","低糖","无糖","不要太甜"]):
        if "低甜" not in state["flavor_preference"]: state["flavor_preference"].append("低甜")
    if any(kw in text for kw in ["清爽","清淡","解暑"]):
        if "清爽" not in state["flavor_preference"]: state["flavor_preference"].append("清爽")
    if any(kw in text for kw in ["冰","冷饮","加冰","冰的"]):
        if "冷饮" not in state["temperature_preference"]: state["temperature_preference"].append("冷饮")

    # 4. time_of_day 只作参考，不自动写入 scene
    # (removed — scene 只来自 Frame394 或用户聊天明确表达)

    # 5. 合并长期偏好（仅当已初始化）
    # flavor / limits: 合并去重
    for f in ["flavor_preference", "limits"]:
        if up.get(f):
            for v in up[f]:
                if v not in state[f]:
                    state[f].append(v)
    # temperature: 本次优先，无本次才用长期（互斥，不合并）
    if up.get("temperature_preference") and not state["temperature_preference"]:
        state["temperature_preference"] = list(up["temperature_preference"][:1])

    # 6. 生成 summary
    mood_tags = state["mood"]
    body_tags = state["body"]

    # 仅当 recommend_input.mood 为空时，情绪来源才是摄像头
    ri_mood = (recommend_input or {}).get("mood", [])
    camera_is_source = (not ri_mood) or len(ri_mood) == 0

    parts = []
    if mood_tags:
        if camera_is_source:
            parts.append(f"识别到你当前心境偏{mood_tags[0]}")
        else:
            parts.append(f"你当前心境偏{mood_tags[0]}")
    if body_tags:
        parts.append(f"记录到你有{'、'.join(body_tags)}")
    flavor = state["flavor_preference"]
    temp = state["temperature_preference"]
    pref_parts = []
    if flavor:
        pref_parts.append("、".join(flavor))
    if temp:
        pref_parts.append("、".join(temp))
    pref_str = "、".join(pref_parts) if pref_parts else ""
    if pref_str:
        parts.append(f"偏好{pref_str}")

    if parts:
        summary = "小才" + "，也".join(parts) + "。是否用这些状态为你定制饮品？"
    else:
        summary = "小才已收到你的信息。是否为你推荐一杯饮品？"

    if len(summary) > 80:
        summary = summary[:77] + "..."

    confidence = 0.75 if parts else 0.5
    return {"summary": summary, "state_guess": state, "confidence": confidence, "need_confirm": True}


@app.post("/api/state/infer", response_model=StateInferResponse)
def infer_state(payload: StateInferRequest):
    """AI 状态推理 — 综合 emotion_result + recommend_input + 消息 + 偏好。"""
    try:
        from config import LLM_MOCK_MODE
    except ImportError:
        from backend.config import LLM_MOCK_MODE

    emo = payload.emotion_result.dict() if payload.emotion_result else {}
    inp = payload.recommend_input.dict() if payload.recommend_input else {}
    up  = payload.user_profile.dict() if payload.user_profile else {}
    ctx = payload.context.dict() if payload.context else {}

    # 真实 LLM 模式
    if not LLM_MOCK_MODE:
        try:
            import json
            import requests
            from config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, DEEPSEEK_MODEL

            user_content = json.dumps({
                "message": payload.message,
                "emotion_result": emo,
                "recommend_input": inp,
                "user_profile": up,
                "context": ctx,
            }, ensure_ascii=False)
            resp = requests.post(
                f"{DEEPSEEK_BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": DEEPSEEK_MODEL,
                    "messages": [
                        {"role": "system", "content": STATE_INFER_SYSTEM},
                        {"role": "user", "content": user_content},
                    ],
                    "temperature": 0.3,
                    "max_tokens": 400,
                },
                timeout=15,
            )
            if resp.status_code == 200:
                data = resp.json()
                raw = data["choices"][0]["message"]["content"].strip()
                if "{" in raw and "}" in raw:
                    start = raw.index("{")
                    end = raw.rindex("}") + 1
                    parsed = json.loads(raw[start:end])
                    return StateInferResponse(
                        summary=parsed.get("summary", ""),
                        state_guess=parsed.get("state_guess", {}),
                        confidence=parsed.get("confidence", 0.8),
                        need_confirm=True,
                    )
        except Exception as e:
            print(f"[StateInfer] DeepSeek failed, fallback rule: {e}")

    result = _rule_state_infer(payload.message, emo, inp, up, ctx)
    return StateInferResponse(**result)


# ─── Run ──────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
