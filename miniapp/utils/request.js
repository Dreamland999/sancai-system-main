/**
 * HTTP 请求封装
 *
 * 当前为 MOCK 模式（USE_MOCK = true），所有接口返回 mock 数据。
 * 接后端时将 USE_MOCK 改为 false 并填入真实 baseURL。
 */

export const BASE_URL = 'http://10.197.196.246:8000'
const USE_MOCK = true

/**
 * 统一请求方法
 * @param {string}  method  - GET / POST
 * @param {string}  path    - 接口路径，如 /api/health
 * @param {object}  data    - POST 请求体（GET 时自动拼到 query）
 * @param {object}  options - { showLoading, showError }
 * @returns {Promise<any>}
 */
function request(method, path, data = {}, options = {}) {
  const { showLoading = false, showError = true } = options

  if (showLoading) {
    uni.showLoading({ title: '加载中...', mask: true })
  }

  return new Promise((resolve, reject) => {
    uni.request({
      url: BASE_URL + path,
      method,
      data,
      header: {
        'Content-Type': 'application/json',
      },
      success(res) {
        if (showLoading) uni.hideLoading()
        const { statusCode, data: body } = res
        if (statusCode === 200) {
          resolve(body)
        } else {
          const msg = body?.detail || body?.message || '请求失败'
          if (showError) {
            uni.showToast({ title: msg, icon: 'none' })
          }
          reject(new Error(msg))
        }
      },
      fail(err) {
        if (showLoading) uni.hideLoading()
        if (showError) {
          uni.showToast({ title: '网络异常', icon: 'none' })
        }
        console.error('[request failed]', path, err)
        reject(err)
      },
    })
  })
}

export function get(path, params = {}, options) {
  const query = Object.keys(params)
    .filter(k => params[k] != null)
    .map(k => encodeURIComponent(k) + '=' + encodeURIComponent(params[k]))
    .join('&')
  const fullPath = query ? path + '?' + query : path
  return request('GET', fullPath, {}, options)
}

export function post(path, data = {}, options) {
  return request('POST', path, data, options)
}

/**
 * 创建 mock API 函数
 * @param {any} mockData - mock 返回数据
 * @param {number} delay - 模拟网络延迟 (ms)
 * @returns {Function}
 */
export function mock(mockData, delay = 200) {
  return () => {
    if (!USE_MOCK) {
      throw new Error('mock() called but USE_MOCK is false')
    }
    return new Promise(resolve => {
      setTimeout(() => resolve(mockData), delay)
    })
  }
}

/** 当前是否为 mock 模式 */
export function isMock() { return USE_MOCK }
