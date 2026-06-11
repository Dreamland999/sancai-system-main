/**
 * 门店 / 售货机 相关接口
 *
 * 当前为 mock 模式。不接真实地图和定位。
 */

import { isMock, mock } from '@/utils/request.js'

// ─── 门店列表 ──────────────────────────────────────

// 获取附近门店/售货机列表
export async function getStoreList(location) {
  if (isMock()) {
    return mock([
      {
        id: 'store-001',
        name: '华南理工大学售货机',
        distance: '256m',
        address: '华南理工大学大学城校区C10楼下',
        image: '/static/figma-frame387/rectangle-13030.png',
      },
      {
        id: 'store-002',
        name: '广州工业大学售货机',
        distance: '1.2km',
        address: '广州工业大学大学城校区E13楼下',
        image: '/static/figma-frame387/rectangle-13031.png',
      },
      {
        id: 'store-003',
        name: '万胜围广场售货机',
        distance: '6.8km',
        address: '万胜围地铁站D口出口处',
        image: '/static/figma-frame387/rectangle-13032.png',
      },
    ])()
  }
  // TODO: get('/api/stores', location)
}

// 选择门店（设为取货门店）
export async function selectStore(storeId) {
  if (isMock()) return mock({ ok: true, store_id: storeId })()
  // TODO: post('/api/stores/select', { store_id: storeId })
}
