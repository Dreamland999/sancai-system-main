/**
 * POST /api/recommend 推荐接口
 *
 * 优先走真实后端，失败时 fallback 到 mock。
 */

import { post } from '@/utils/request.js'

const BASE_URL = 'http://10.191.133.249:8000'

function defaultPayload() {
  return {
    scene: [],
    body: [],
    mood: [],
    needs: [],
    limits: [],
    flavor_preference: [],
    temperature_preference: [],
  }
}

function mockResult() {
  return {
    session_id: 'mock-session',
    status: {},
    avoided_items: [],
    pipeline: ['rules', 'dual-tower', 'mlp-rank'],
    model_mode: 'fallback_mock',
    recommendations: [
      {
        recipe_id: 'mock-001',
        name: '桃气西瓜冰沙',
        type: '安神',
        score: 0.92,
        match_reason: '西瓜清热解暑，茉莉花茶安神宁心，适合夏日烦躁时饮用',
        polished_text: '精选西瓜与茉莉花茶的清新组合，带来凉爽安宁的夏日体验。',
        visual_prompt: '',
        visual_mapping: [],
        image_url: null,
        health_notes: [],
        description: '清热解暑，平复烦躁，补水消肿，唤醒活力',
        sweetness: '半糖',
        temperature: '冰',
      },
    ],
  }
}

/**
 * 调用 /api/recommend，失败时返回 mock
 * @param {object} input - 用户状态标签
 * @param {number} timeout - 超时毫秒数
 */
export async function recommend(input = {}, timeout = 5000) {
  // 补齐缺失字段
  const payload = { ...defaultPayload(), ...input }

  // 超时 Promise
  const timeoutP = new Promise((_, reject) =>
    setTimeout(() => reject(new Error('timeout')), timeout)
  )

  try {
    const result = await Promise.race([
      uni.request({
        url: BASE_URL + '/api/recommend',
        method: 'POST',
        data: payload,
        header: { 'Content-Type': 'application/json' },
      }).then(res => {
        if (res.statusCode === 200 && res.data) {
          return res.data
        }
        throw new Error('status ' + res.statusCode)
      }),
      timeoutP,
    ])
    console.log('[recommend] success, model_mode:', result.model_mode)
    return result
  } catch (err) {
    console.error('[recommend failed]', err)
    return mockResult()
  }
}
