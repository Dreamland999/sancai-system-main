/**
 * 订单 / 支付 / 评价 相关接口
 *
 * 当前为 mock 模式。不接微信支付。
 */

import { isMock, mock } from '@/utils/request.js'

// ─── 订单创建 ──────────────────────────────────────

// 创建订单
export async function createOrder(orderData) {
  if (isMock()) {
    return mock({
      order_id: 'ORD20260605001',
      pickup_code: '305',
      status: 'pending',
    })()
  }
  // TODO: post('/api/orders', orderData)
}

// 获取订单详情（取餐码等）
export async function getOrderDetail(orderId) {
  if (isMock()) {
    return mock({
      order_id: orderId,
      pickup_code: '305',
      drink_name: '解暑纤果茶',
      status: 'ready',
      created_at: '2026-06-05T14:30:00',
    })()
  }
  // TODO: get('/api/orders/' + orderId)
}

// ─── 支付（不接微信支付，占位）───────────────────────

// 发起支付请求（mock 返回假支付参数）
export async function payOrder(orderId, method) {
  if (isMock()) {
    return mock({ paid: true, method: method || 'pickup' })()
  }
  // TODO: post('/api/orders/' + orderId + '/pay', { method })
}

// ─── 评价 ──────────────────────────────────────────

// 提交订单评价
export async function submitReview(orderId, rating, comment) {
  if (isMock()) return mock({ ok: true })()
  // TODO: post('/api/orders/' + orderId + '/review', { rating, comment })
}
