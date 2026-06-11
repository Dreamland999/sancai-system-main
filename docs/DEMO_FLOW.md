# 演示流程

## 演示前准备

### 1. 启动后端

```bash
cd sancai-system
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

验证：浏览器打开 `http://127.0.0.1:8000/api/health` → `{"status":"ok"}`

### 2. 微信开发者工具设置

- 用 HBuilderX 打开 `miniapp/` 目录 → 运行到微信开发者工具
- 详情 → 本地设置 → 勾选「不校验合法域名、web-view、TLS 版本以及 HTTPS 证书」

### 3. Mock 模式

当前 `.env.example` 中 `LLM_MOCK_MODE=true`，/api/chat 和 /api/intent/parse 使用关键词/固定回复。
如需真实 DeepSeek，设置 `LLM_MOCK_MODE=false` 并填入 `DEEPSEEK_API_KEY`。

---

## 演示路径

### 完整制作流程（约 2 分钟）

| 步骤 | 页面 | 操作 | 后端接口 | 预期结果 |
|------|------|------|----------|----------|
| 1 | **Frame383** 启动页 | 点击页面 | — | 跳转首页 |
| 2 | **Frame400** 首页 | 点击「制作」 | — | 跳转隐私弹窗 |
| 3 | **Frame396** 隐私弹窗 | 勾选 → 确定 | — | 跳转实时了解 |
| 4 | **Frame398** 实时了解 | 开始识别 | — | 跳转识别中 |
| 5 | **Frame382** 识别中 | 点击莲花 | — | 跳转状态显化 |
| 6 | **Frame394** 状态显化 | 选「乏力」→ 下一步 | — | 保存 recommend_input |
| 7 | **Frame399** AI定制 | 点击输入框 | `POST /api/chat` + `POST /api/intent/parse` | 显示 AI 回复，合并标签 |
| 8 | **Frame399** | 点击绿色圆圈 | — | 跳转 loading |
| 9 | **Frame390** loading | 自动 | `POST /api/recommend` | 保存 recommend_result，跳配方详情 |
| 10 | **Frame389** 配方详情 | 自动展示 | `POST /api/feedback` | 显示推荐饮品名/功效/甜度/温度 |
| 11 | **Frame389** | 点击莲花 | `POST /api/feedback` | 跳转自行调整 |
| 12 | **Frame391** 自行调整 | 点 5 次「下一步」 | — | top → middle → iceSugar → package → sprinkle |
| 13 | **Frame391** | sprinkle 点确定 | `POST /api/feedback` | 跳转支付 |
| 14 | **Frame388** 支付 | 附近自提 | — | 跳转门店 |
| 15 | **Frame387** 门店 | 点击门店卡片 | `POST /api/feedback` | 跳转订单生成 |
| 16 | **Frame385** 订单生成 | 点击条形码 | `POST /api/feedback` | 跳转评价 |
| 17 | **Frame386** 评价 | 点击完成 | `POST /api/feedback` | 回首页 |

### 食养局分支（约 1 分钟）

| 步骤 | 页面 | 操作 | 说明 |
|------|------|------|------|
| 1 | Frame400 | 点击「食材库」 | 跳转食养局 |
| 2 | Frame384 | 点击「安神匣」 | 跳转安神局 |
| 3 | Frame401 | 点击任一食材 → 下一步 | 跳转 loading |
| 4 | Frame390 → Frame389 | 自动 | 汇入主流程 |

### 快速测试（跳过面容/聊天）

```
Frame383 启动页 → 首页 → 制作 → 隐私弹窗 → 勾选 → 确定
→ 实时了解 → 开始识别 → 识别中 → 莲花 → 状态显化
→ 选标签 → 下一步 → AI定制 → 绿色圆圈 → loading → 配方详情
```

---

## 后端日志预期

启动后端后，完成一次完整流程，后端终端应依次出现：

```
POST /api/chat 200 OK
POST /api/intent/parse 200 OK
POST /api/recommend 200 OK
POST /api/feedback 200 OK        ← view_recommendation
POST /api/feedback 200 OK        ← click_adjust
POST /api/feedback 200 OK        ← enter_payment
POST /api/feedback 200 OK        ← select_store
POST /api/feedback 200 OK        ← create_order
POST /api/feedback 200 OK        ← submit_review
```

## 失败 fallback

| 接口 | 失败行为 |
|------|----------|
| /api/chat | 返回 mock reply，聊天不白屏 |
| /api/intent/parse | 前端关键词 fallback，不影响推荐 |
| /api/recommend | 返回 mock 推荐结果，配方页不白屏 |
| /api/feedback | 静默失败，console.error，不阻断流程 |

关闭后端后，完整流程仍可走通，仅 console 出现错误日志。

---

## feedback 日志查看

```bash
python scripts/inspect_feedback.py
python scripts/inspect_feedback.py --csv    # 导出 CSV
```
