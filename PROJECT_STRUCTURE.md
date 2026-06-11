# Project Structure (Updated 2026-06-05)

```
sancai-system/
│
├── miniapp/                         ← [active] 当前 uni-app 微信小程序
│   ├── App.vue                      入口组件
│   ├── main.js                      Vue 实例创建
│   ├── pages.json                   路由表（16 个页面 + 全局样式）
│   ├── manifest.json                小程序配置
│   ├── pages/
│   │   ├── figma-frame383-preview/  启动页 / Logo 页
│   │   ├── figma-frame400-preview/  首页 / 雨景首页
│   │   ├── figma-frame396-preview/  隐私弹窗
│   │   ├── figma-frame398-preview/  实时了解 / 面容 + 设备识别
│   │   ├── figma-frame382-preview/  AI 聆听识别中
│   │   ├── figma-frame394-preview/  状态显化（多状态页）
│   │   ├── figma-frame399-preview/  AI 定制聊天
│   │   ├── figma-frame390-preview/  专属食材搜集 loading
│   │   ├── figma-frame389-preview/  配方详情
│   │   ├── figma-frame391-preview/  自行调整（5 子状态）
│   │   ├── figma-frame388-preview/  支付选择
│   │   ├── figma-frame387-preview/  确定门店 / 自提售货机
│   │   ├── figma-frame385-preview/  订单生成 / 取餐码
│   │   ├── figma-frame386-preview/  完成订单 / 评价
│   │   ├── figma-frame384-preview/  食养局分类入口
│   │   └── figma-frame401-preview/  安神局 / 食材选择
│   ├── api/                         Mock API 模块（接后端前占位）
│   │   ├── ai.js                    AI 对话 & 食材推荐
│   │   ├── device.js                设备/蓝牙
│   │   ├── order.js                 订单/评价
│   │   ├── recipe.js                食材/配方
│   │   ├── store.js                 门店
│   │   └── user.js                  用户/隐私/状态采集
│   ├── utils/
│   │   ├── nav.js                   路由辅助（goBack, safeGo, safeNavigateTo）
│   │   └── request.js              HTTP 封装（当前 USE_MOCK = true）
│   └── static/
│       ├── figma-frame382/ ~ frame401/  各页面静态资源
│       ├── figma-home/                    首页静态资源
│       └── fonts/                         字体文件
│
├── backend/                         ← [active] FastAPI 后端
│   ├── main.py                      入口，13 个 API 端点
│   ├── schemas.py                   Pydantic 模型（UserStateRequest, RecommendResponse 等）
│   ├── recommender_service.py       推荐引擎（加载 algorithm/ 模型）
│   ├── emotion_service.py           面部情绪识别服务
│   ├── database.py                  SQLite 初始化 + 种子数据
│   ├── seed_visual_mappings.py      视觉标签映射
│   ├── config.py                    环境变量配置
│   ├── llm/
│   │   ├── deepseek.py              DeepSeek API 调用
│   │   └── image_gen.py             通义万相图片生成
│   ├── models/                      面部识别 ONNX 模型
│   ├── recommend/                   推荐相关模块
│   └── requirements.txt             FastAPI 依赖
│
├── algorithm/                       ← [active_support] 推荐算法 & 模型权重（不可删）
│   ├── twin_tower_model.pt          双塔模型 (795 KB)
│   ├── mlp_ranker_model.pt          MLP 排序模型 (6.5 KB)
│   ├── twin_tower_vocab.json        词表 (32 KB)
│   └── twin_tower_recommendation.py 双塔 + MLP 核心代码 (77 KB)
│
├── data/                            ← [active_support] 数据源（不可删）
│   ├── sancai.db                    SQLite 数据库（gitignore 忽略但运行时必需）
│   ├── 标签字典表_最终检查版.csv
│   ├── 饮品成分表_最终检查版.csv
│   ├── 饮品方案表_最终检查版.csv
│   ├── 用户输入表_最终检查版.csv
│   └── 视觉标签映射表.csv
│
├── app/                             ← [legacy] 旧 React 18 + Vite 5 H5 前端
│   │                                 未被 miniapp 或 backend 引用
│   │                                 暂时保留作历史参考
│   ├── package.json                 "stateful-drink-demo"
│   ├── vite.config.js
│   └── src/
│
├── autohtml-project2/               ← [source material] Figma/AutoHTML 导出工具
│   │                                 不参与运行时
│   │                                 保留用于追溯 Figma → Vue 转化链路
│   ├── sandbox.config.json
│   ├── package.json
│   └── src/Frame400/
│
├── reports/                         ← [archive] 算法训练 & 评估产物
│   ├── 双塔_MLP排序评估报告.txt
│   ├── 双塔训练样本.csv
│   ├── MLP排序训练样本.csv
│   ├── 推荐记录表_双塔_MLP排序版.csv
│   └── 推荐记录表_双塔_MLP排序版.xlsx
│
├── scripts/                         ← [archive] 数据预处理脚本（已执行完毕）
│   ├── process_final_check.py
│   └── process_four_tables.py
│
├── archive/                         ← [archive] 历史归档
│   ├── old_outputs/
│   └── old_reports/
│
├── .env.example                     环境变量模板
├── .gitignore
├── requirements.txt                 算法依赖
├── README.md
├── PROJECT_STRUCTURE.md              本文件
└── 项目推进记录_2025-05-24.txt       早期开发记录
```

---
## 目录分类速查

| 目录 | 分类 | 可删? |
|------|------|------|
| `miniapp/` | active（当前小程序） | ❌ |
| `backend/` | active（当前后端） | ❌ |
| `algorithm/` | active_support（模型+算法） | ❌ |
| `data/` | active_support（数据源） | ❌ |
| `app/` | legacy（旧 React 前端） | 🔶 不可 |
| `autohtml-project2/` | source_material（Figma 来源） | 🔶 不可 |
| `reports/` | archive（训练产物） | 🔶 不可 |
| `scripts/` | archive（预处理脚本） | 🔶 不可 |
| `archive/` | archive（历史归档） | 🔶 不可 |

---
## 接口字段对齐说明

`/api/recommend` 请求以 `backend/schemas.py:UserStateRequest` 为准：

| 字段 | 类型 | 说明 |
|------|------|------|
| `scene` | `List[str]` | 使用场景 |
| `body` | `List[str]` | 身体状况 |
| `mood` | `List[str]` | 情绪状态 |
| `needs` | `List[str]` | 需求偏好 |
| `limits` | `List[str]` | 限制条件（过敏等） |
| `flavor_preference` | `List[str]` | 口味偏好 |
| `temperature_preference` | `List[str]` | 温度偏好 |

> ⚠️ 前端 mock API 接后端时，字段名必须对齐上述 schema，不要用旧字段名。
