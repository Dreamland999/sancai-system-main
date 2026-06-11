/**
 * 返回上一页，如果无法返回则跳转到首页
 * @param {string} homeUrl 首页路径
 */
export function goBack(homeUrl = '/pages/figma-frame400-preview/figma-frame400-preview') {
  const pages = getCurrentPages()
  if (pages.length > 1) {
    uni.navigateBack()
  } else {
    uni.redirectTo({ url: homeUrl })
  }
}

/**
 * 安全 navigateTo，失败时输出日志
 * @param {string} url 目标路径
 */
export function safeNavigateTo(url) {
  uni.navigateTo({
    url,
    fail(err) {
      console.error('[navigateTo failed]', url, err)
    }
  })
}

/**
 * 智能跳转：页面栈 >= 8 时用 redirectTo，否则用 navigateTo
 * @param {string} url 目标路径
 */
export function safeGo(url) {
  const pages = getCurrentPages()
  if (pages.length >= 8) {
    uni.redirectTo({
      url,
      fail(err) {
        console.error('[safeGo redirectTo failed]', url, err)
      }
    })
  } else {
    uni.navigateTo({
      url,
      fail(err) {
        console.error('[safeGo navigateTo failed]', url, err)
      }
    })
  }
}
