/**
 * AI 对话 / 定制 相关接口
 *
 * sendMessage 优先走真实后端 /api/chat，失败时 fallback mock。
 */

import { isMock, mock } from '@/utils/request.js'

const BASE_URL = 'http://10.197.196.246:8000'

// ─── AI 对话 ────────────────────────────────────────

function mockReply() {
  return { reply: '今天高温，建议来一杯清热解暑的茉莉薄荷茶~', session_id: 'mock-chat' }
}

/**
 * 发送对话消息，返回 AI 回复
 * @param {string} text 用户消息
 * @param {object} context 上下文信息
 * @param {number} timeout 超时 ms
 */
export async function sendMessage(text, context = {}, timeout = 8000) {
  console.log('[chat] start sendMessage')

  const payload = {
    message: text,
    user_id: 'preview_user',
    context: context || {},
  }
  const url = BASE_URL + '/api/chat'

  console.log('[chat] request url:', url)
  console.log('[chat] request payload:', payload)

  try {
    const result = await new Promise((resolve, reject) => {
      const timer = setTimeout(() => reject(new Error('chat timeout')), timeout)
      uni.request({
        url,
        method: 'POST',
        data: payload,
        header: { 'Content-Type': 'application/json' },
        success(res) {
          clearTimeout(timer)
          console.log('[chat] real response:', res.data)
          if (res.statusCode === 200 && res.data) {
            resolve(res.data)
          } else {
            reject(new Error('status ' + res.statusCode))
          }
        },
        fail(err) {
          clearTimeout(timer)
          console.error('[chat] request fail:', err)
          reject(err)
        },
      })
    })
    console.log('[chat] success, session_id:', result.session_id)
    return result
  } catch (err) {
    console.error('[chat failed, fallback mock]', err)
    console.log('[chat] using mock fallback')
    return mockReply()
  }
}

// 获取对话历史
export async function getChatHistory() {
  if (isMock()) {
    return mock([
      { role: 'ai', text: '今天感觉怎么样？' },
      { role: 'user', text: '有点烦躁' },
      { role: 'ai', text: '夏天容易心浮气躁，来杯安神的茶吧' },
    ])()
  }
  // TODO: get('/api/chat/history')
}

// ─── 食材推荐（AI 驱动）──────────────────────────────

// 根据用户状态获取推荐食材
export async function getRecommendIngredients(stateTags) {
  if (isMock()) {
    return mock([
      { id: 'jasmine', name: '茉莉花茶', score: 0.92 },
      { id: 'mint', name: '薄荷叶', score: 0.87 },
      { id: 'melon', name: '西瓜', score: 0.81 },
    ])()
  }
  // TODO: post('/api/ai/recommend/ingredients', { tags: stateTags })
}
