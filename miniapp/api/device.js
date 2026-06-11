/**
 * 设备 / 蓝牙 相关接口
 *
 * 当前为 mock 模式。不接真实蓝牙和可穿戴设备。
 */

import { isMock, mock } from '@/utils/request.js'

// ─── 设备管理 ──────────────────────────────────────

// 获取已绑定的设备列表
export async function getDeviceList() {
  if (isMock()) {
    return mock([
      {
        id: 'dev-001',
        name: '手臂穿戴设备',
        type: 'armband',
        serial: 'LP:2246:325667',
        connected: true,
      },
    ])()
  }
  // TODO: get('/api/devices')
}

// 绑定新设备
export async function bindDevice(deviceId) {
  if (isMock()) return mock({ ok: true })()
  // TODO: post('/api/devices/bind', { device_id: deviceId })
}

// 解绑设备
export async function unbindDevice(deviceId) {
  if (isMock()) return mock({ ok: true })()
  // TODO: post('/api/devices/unbind', { device_id: deviceId })
}

// ─── 蓝牙（占位）───────────────────────────────────

// 搜索附近蓝牙设备
export async function scanBluetoothDevices() {
  if (isMock()) {
    return mock([
      { name: 'Sancai-Band-01', id: 'BT-001' },
      { name: 'Sancai-Band-02', id: 'BT-002' },
    ])()
  }
  // TODO: 调用 wx.openBluetoothAdapter + wx.startBluetoothDevicesDiscovery
  // 实际由 device 模块处理
}
