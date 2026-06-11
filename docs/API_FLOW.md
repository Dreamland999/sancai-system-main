# API 接口文档

所有接口 base URL：`http://127.0.0.1:8000`

---

## 1. POST /api/chat — AI 对话

**请求**：
```json
{
  "message": "我最近有点累，想喝一杯适合放松的饮品",
  "user_id": "preview_user",
  "context": { "recommend_input": { "body": ["乏力"] } }
}
```

**响应**：
```json
{
  "reply": "累的时候来杯温热的花草茶最舒服了~茉莉加薄荷，清凉安神又解乏。",
  "session_id": "CHAT_001"
}
```

**被调用**：Frame399 `onSend()`

**fallback**：mock reply `"今天高温，建议来一杯清热解暑的茉莉薄荷茶~"`

**依赖**：`LLM_MOCK_MODE=false` + `DEEPSEEK_API_KEY` 时调用 DeepSeek

---

## 2. POST /api/intent/parse — 标签解析

**请求**：
```json
{
  "message": "我最近睡不好，有点烦，想喝热一点不要太甜",
  "context": {}
}
```

**响应**：
```json
{
  "scene": [],
  "body": ["失眠"],
  "mood": ["烦躁"],
  "needs": [],
  "limits": [],
  "flavor_preference": ["低甜"],
  "temperature_preference": ["热饮"]
}
```

**被调用**：Frame399 `onSend()`（并行于 chat）

**fallback**：前端 14 条关键词规则 + 后端 14 条关键词规则

**依赖**：`LLM_MOCK_MODE=false` + `DEEPSEEK_API_KEY` 时调用 DeepSeek

---

## 3. POST /api/recommend — 饮品推荐

**请求**（7 个 List[str] 字段）：
```json
{
  "scene": [],
  "body": ["乏力", "失眠"],
  "mood": ["烦躁"],
  "needs": [],
  "limits": [],
  "flavor_preference": ["低甜"],
  "temperature_preference": ["热饮"]
}
```

**响应**：
```json
{
  "session_id": "S0036",
  "model_mode": "twin_tower_mlp",
  "recommendations": [
    {
      "recipe_id": "R078",
      "name": "茉莉薄荷茶",
      "score": 0.93,
      "match_reason": "茉莉安神，薄荷提神，适合疲惫烦躁时饮用",
      "polished_text": "...",
      "visual_prompt": "...",
      "description": "清热解暑，平复烦躁",
      "sweetness": "半糖",
      "temperature": "热饮",
      "health_notes": [],
      "image_url": null
    }
  ]
}
```

**被调用**：Frame390 `fetchRecommend()`

**fallback**：mock 推荐结果（结构一致）

**依赖**：`algorithm/` 双塔 + MLP 模型

---

## 4. POST /api/feedback — 行为事件上报

**请求**：
```json
{
  "recommendation_id": "",
  "session_id": "S0036",
  "user_id": "preview_user",
  "recipe_id": "R078",
  "event_type": "view_recommendation",
  "payload": { "page": "Frame389" },
  "timestamp": "2026-06-06T12:00:00"
}
```

**响应**：
```json
{ "status": "saved", "message": "已记录（行为事件）。" }
```

**被调用**：Frame389/391/387/385/386 的关键交互节点

**fallback**：静默失败，不弹 toast

**保存**：JSONL (`backend/feedback_log.jsonl`) + SQLite（仅 recommendation_id 非空时）

---

## 5. 其他接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/health | 健康检查 |
| GET | /api/options | 标签选项 |
| GET | /api/recipes | 配方列表 |
| GET | /api/recipes/{id} | 配方详情 |
| GET | /api/tags | 标签字典 |
| GET | /api/ingredients | 食材列表 |
| GET | /api/stores | 门店列表 |
| POST | /api/emotion/predict | 面部情绪（未接） |
| POST | /api/image/generate | 图片生成（未接） |

---

## 推荐输入 7 字段

| 字段 | 类型 | 来源 |
|------|------|------|
| `scene` | List[str] | 使用场景（未用） |
| `body` | List[str] | Frame394 选择 + intent 解析 |
| `mood` | List[str] | intent 解析 |
| `needs` | List[str] | intent 解析 |
| `limits` | List[str] | intent 解析 |
| `flavor_preference` | List[str] | intent 解析 |
| `temperature_preference` | List[str] | intent 解析 |

---

## feedback event_type

| event_type | 含义 | 触发位置 |
|------------|------|----------|
| `view_recommendation` | 查看推荐 | Frame389 mounted |
| `click_adjust` | 进入调整 | Frame389 莲花点击 |
| `enter_payment` | 进入支付 | Frame391 sprinkle 确定 |
| `select_store` | 选择门店 | Frame387 门店卡片 |
| `create_order` | 生成订单 | Frame385 条形码 |
| `submit_review` | 提交评价 | Frame386 完成 |
