/**
 * 用户 / 隐私授权 / 状态采集 相关接口
 *
 * 当前为 mock 模式，接后端时去掉 mock 改为真实 POST / GET。
 */

import { isMock, mock } from '@/utils/request.js'

// ─── 隐私授权 ──────────────────────────────────────

// 提交隐私授权同意
export async function agreePrivacy() {
  if (isMock()) return mock(true)()
  // TODO: post('/api/user/privacy/agree')
}

// 查询用户隐私授权状态
export async function getPrivacyStatus() {
  if (isMock()) return mock({ agreed: false })()
  // TODO: get('/api/user/privacy/status')
}

// ─── 信息采集 ──────────────────────────────────────

// 提交身体状况采集数据
export async function submitHealthSurvey(data) {
  if (isMock()) return mock({ ok: true })()
  // TODO: post('/api/user/health-survey', data)
}

// ─── 面部 & 设备信息 ────────────────────────────────

// 提交面部扫描结果（先用占位，后续接相机）
export async function submitFaceScan(imageBase64) {
  if (isMock()) return mock({ face_id: 'mock-face-001' })()
  // TODO: post('/api/user/face-scan', { image: imageBase64 })
}

// 提交可穿戴设备数据
export async function submitDeviceData(deviceData) {
  if (isMock()) return mock({ ok: true })()
  // TODO: post('/api/user/device-data', deviceData)
}

// ─── 状态标签 ──────────────────────────────────────

// 提交用户选择的身体/情绪/节律标签
export async function submitStateTags(tags) {
  if (isMock()) return mock({ matched_profile: '平和质' })()
  // TODO: post('/api/user/state-tags', { tags })
}
