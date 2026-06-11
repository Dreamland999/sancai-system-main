# 已知限制与未完成内容

## UI 层面

- **16 个页面均为 Figma preview**，使用 AutoHTML 导出的静态布局，未经 UI 设计师精修
- Frame399 聊天输入为简化版（固定默认消息，无真实键盘输入）
- Frame391 子状态（top/middle/iceSugar/package/sprinkle）的视觉为初步对齐，细节仍需调整
- 返回按钮在部分页面为 48rpx 小图标，虽已包 80rpx 热区但视觉偏小

## 功能层面

### 未接入的能力

| 能力 | 说明 |
|------|------|
| 微信支付 | Frame388 仅 showToast 占位 |
| 地图/定位 | Frame387 使用静态 mock 门店列表 |
| 相机 | Frame399 相机按钮为 showToast 占位 |
| 语音输入 | Frame399 语音按钮为 showToast 占位 |
| 蓝牙设备 | Frame398/382 设备连接为 showToast 占位 |
| 面部情绪识别 | `/api/emotion/predict` 后端已实现，前端未接 |

### 缺失页面

| 页面 | 入口 |
|------|------|
| 配方列表页 | Frame400「配方库」→ showToast |
| 百料匣 / 解郁匣 / 舒愉匣 | Frame384 三匣 → showToast |
| 配送地址页 | Frame388「配送服务」→ showToast |
| 历史记录页 | 多个页面「历史」→ showToast |
| 个人中心 | 无入口 |

### AI 能力

- `/api/intent/parse` 当前主要使用关键词 fallback，不是微调模型
- `/api/chat` 使用通用 DeepSeek-chat，system prompt 为基础饮品顾问角色
- LLM_MOCK_MODE=true 时所有 AI 回复为固定文本

## 推荐引擎

- 依赖已有双塔 + MLP 模型（`algorithm/`），模型基于静态 CSV 数据训练
- 推荐结果随标签变化，但不保证每次都能命中用户预期
- `visual_mapping` / `visual_prompt` 字段存在但前端未用于 UI 渲染
- 无在线学习，新增 feedback 数据尚未用于模型更新

## Feedback 系统

- 行为事件已采集到 `backend/feedback_log.jsonl`（JSONL 格式）
- SQLite 仅对传统 feedback（含 recommendation_id）写入
- 已提供 `scripts/inspect_feedback.py` 查看和导出
- 尚未接入 MLP 排序模型的训练/评估流程
- 尚未计算用户偏好画像（如甜度偏好概率）

## 技术债务

- `app/` 为旧 React/Vite 前端，已标记 legacy 但未删除
- `autohtml-project2/` 为 Figma 导出来源工具，不参与运行时
- `archive/` 为历史空目录
- `miniapp/unpackage/` 为编译产物，不应手改
- pages.json 注册了 16 个 preview 页面，未对正式页面做规划

## 演示建议

- 后端需保持运行 `uvicorn`
- 微信开发者工具需勾选「不校验合法域名」
- 真机预览需配置合法域名或使用局域网 IP
- 建议先用 Mock 模式（`LLM_MOCK_MODE=true`）走通完整流程，再切真实 API
