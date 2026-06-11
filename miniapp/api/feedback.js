/**
 * POST /api/feedback 行为事件上报
 *
 * 失败时静默，不阻断主流程。
 */

const BASE_URL = 'http://10.197.196.246:8000'

/**
 * @param {string} eventType
 * @param {object} extra - 额外 payload
 */
export function sendFeedback(eventType, extra = {}) {
  const result = uni.getStorageSync('recommend_result') || {}
  const input = uni.getStorageSync('recommend_input') || {}

  const payload = {
    recommendation_id: '',
    session_id: result.session_id || '',
    user_id: 'preview_user',
    recipe_id: (result.recommendations?.[0]?.recipe_id) || '',
    event_type: eventType,
    payload: { ...extra, recommend_input: input },
    timestamp: new Date().toISOString(),
  }

  console.log('[feedback] send', eventType, payload.session_id)

  uni.request({
    url: BASE_URL + '/api/feedback',
    method: 'POST',
    data: payload,
    header: { 'Content-Type': 'application/json' },
    success(res) {
      if (res.statusCode === 200) {
        console.log('[feedback] ok', eventType)
      } else {
        console.error('[feedback] status', res.statusCode)
      }
    },
    fail(err) {
      console.error('[feedback] fail', eventType, err.errMsg || err)
    },
  })
}
