# Sancai AI 中医饮品系统

基于双塔+MLP的AI推荐引擎，为售卖机大屏和微信小程序提供智能中医草本饮品推荐。

## 功能

- AI对话：DeepSeek 驱动的自然语言交互
- 面部情绪识别：MobileFaceNet + YuNet 实时分析
- 推荐引擎：双塔召回 + MLP精排 + LLM润色
- 38页完整UI：售卖机大屏 + 手机端
- 数据库：SQLite + CSV 导入

---
## 项目结构

```
sancai-system/
├── miniapp/                 ← 当前主前端（uni-app 微信小程序）
│   ├── pages/               # 16 个 Figma 预览页面
│   ├── pages.json           # 路由注册
│   ├── static/figma-*/      # Figma 导出静态资源
│   ├── api/                 # Mock API 模块（接后端前占位）
│   └── utils/               # 路由 & 请求工具
│
├── backend/                 ← 当前后端（FastAPI）
│   ├── main.py              # 13 个 API 端点
│   ├── schemas.py           # Pydantic 请求/响应模型
│   ├── recommender_service.py
│   └── llm/                 # DeepSeek & 通义万相
│
├── algorithm/               ← 推荐算法与模型权重（不可删）
│   ├── twin_tower_model.pt
│   ├── mlp_ranker_model.pt
│   ├── twin_tower_vocab.json
│   └── twin_tower_recommendation.py
│
├── data/                    ← 数据源（SQLite + CSV，不可删）
│   ├── sancai.db
│   ├── 标签字典表_最终检查版.csv
│   ├── 饮品成分表_最终检查版.csv
│   ├── 饮品方案表_最终检查版.csv
│   └── 用户输入表_最终检查版.csv
│
├── app/                     ← [legacy] 旧 React/Vite H5 前端
│                               当前 miniapp 不依赖，保留作历史参考
│
├── autohtml-project2/       ← [source material] Figma/AutoHTML 导出来源
│                               不参与运行时，保留用于追溯设计来源
│
├── reports/                 ← [archive] 算法训练/评估输出
├── scripts/                 ← [archive] 数据预处理脚本
├── archive/                 ← [archive] 历史归档
├── .env.example             # 环境变量模板
└── requirements.txt         # 算法依赖
```

## 启动

### 后端

```bash
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

### 前端（uni-app 微信小程序）

1. 用 HBuilderX 打开 `miniapp/` 目录
2. 运行 → 微信开发者工具
3. 编译产物在 `miniapp/unpackage/dist/dev/mp-weixin/`，**不要手改**

> 旧 React 前端 `app/` 为 legacy，`cd app && npm run dev` 不再是当前前端启动方式。

---
## 核心接口：POST /api/recommend

前端接推荐接口时，必须以 `backend/schemas.py` 的 `UserStateRequest` 为准。

### 请求体

```json
{
  "scene": [],
  "body": [],
  "mood": [],
  "needs": [],
  "limits": [],
  "flavor_preference": [],
  "temperature_preference": []
}
```

### 响应体（`RecommendResponse`）

```json
{
  "session_id": "...",
  "status": {},
  "avoided_items": [],
  "pipeline": [],
  "model_mode": "twin_tower_mlp",
  "recommendations": [
    {
      "recipe_id": "...",
      "name": "...",
      "type": "",
      "score": 0.92,
      "match_reason": "",
      "polished_text": "",
      "visual_prompt": "",
      "visual_mapping": [],
      "image_url": null,
      "health_notes": [],
      "description": "",
      "sweetness": "",
      "temperature": ""
    }
  ]
}
```

### 所有 API 端点

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/health` | 健康检查 |
| GET | `/api/options` | 获取标签选项 |
| POST | `/api/recommend` | 核心推荐 |
| POST | `/api/feedback` | 提交反馈 |
| GET | `/api/recipes` | 配方列表 |
| GET | `/api/recipes/{recipe_id}` | 配方详情 |
| GET | `/api/tags` | 标签字典 |
| GET | `/api/ingredients` | 食材列表 |
| GET | `/api/history/{user_id}` | 用户历史 |
| POST | `/api/image/generate` | AI 生成饮品图 |
| POST | `/api/chat` | AI 对话 |
| POST | `/api/emotion/predict` | 面部情绪识别 |
| GET | `/api/stores` | 门店列表 |
