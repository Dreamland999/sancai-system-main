/**
 * POST /api/intent/parse 意图解析接口
 *
 * 优先走真实后端，失败时 fallback 到前端关键词匹配。
 */

const BASE_URL = 'http://10.197.196.246:8000'

const KEYWORD_RULES = [
  // body
  [["睡不好","困","想睡","没睡好","犯困","好困","昏昏沉沉"], "body", "困倦"],
  [["累","疲惫","没力气","没精神","好累","乏","精疲力尽"], "body", "疲劳"],
  [["状态很好","身体良好","没啥不舒服","感觉不错","我很好","精神不错","状态不错","身体不错"], "body", "良好"],
  [["饿","饥饿","肚子饿","没吃饭","空腹"], "body", "饥饿"],
  [["饱","吃饱","吃撑","吃太饱"], "body", "饱腹"],
  [["有点热","感觉热","很热","好热","太热","出汗"], "body", "感觉有点热"],
  [["有点冷","感觉冷","很冷","好冷","太冷","冻"], "body", "感觉有点冷"],
  [["渴","口干","想喝水","口渴","缺水"], "body", "口渴"],
  // mood
  [["开心","高兴","愉快","快乐","挺好的","挺好的呀","哈哈"], "mood", "开心"],
  [["平静","还行","还可以","一般般","不好不坏","没啥情绪"], "mood", "平静"],
  [["兴奋","激动","期待","太好","哇","燃"], "mood", "兴奋"],
  [["低落","不开心","沮丧","难过","抑郁","emo"], "mood", "低落"],
  [["烦","烦躁","烦死了","烦闷","心浮气躁","毛躁"], "mood", "烦躁"],
  [["紧张","焦虑","慌","不安","压力","担心"], "mood", "紧张"],
  [["无聊","没什么意思","没事干","闷","闲"], "mood", "无聊"],
  [["孤单","孤独","寂寞","一个人"], "mood", "孤单"],
  // scene
  [["家","家里","在家","宿舍","寝室","房间"], "scene", "家/宿舍"],
  [["学校","教学楼","上课","教室","课堂"], "scene", "学校/教学楼"],
  [["图书馆","自习室","自习","看书","学习区"], "scene", "图书馆/自习室"],
  [["办公室","公司","上班","工位","开会"], "scene", "办公室/公司"],
  [["餐厅","食堂","吃饭","就餐","饭堂"], "scene", "餐厅/食堂"],
  [["健身房","运动场","操场","锻炼","健身"], "scene", "健身房/运动场"],
  [["咖啡店","奶茶店","喝咖啡","喝奶茶"], "scene", "咖啡店/奶茶店"],
  [["商场","逛街","购物","商业区","mall"], "scene", "商场/商业街"],
  [["地铁","公交","车站","通勤","路上","坐车"], "scene", "地铁/公交/车站"],
  [["公园","户外","外面","野餐","散步"], "scene", "公园/户外"],
  // needs
  [["放松","安神","助眠","休息","静一静"], "needs", "安神"],
  [["提神","精神","清醒","醒脑","醒了"], "needs", "提神"],
  [["解暑","清凉","降温","消暑"], "needs", "解暑"],
  [["暖身","暖一点","暖和","驱寒"], "needs", "暖身"],
  // flavor
  [["清爽","清淡"], "flavor_preference", "清爽"],
  [["奶香","奶味","牛奶","奶盖"], "flavor_preference", "奶香"],
  [["茶香","茶味","茶底"], "flavor_preference", "茶香"],
  [["果香","果味","水果"], "flavor_preference", "果香"],
  [["花香","花的味道","花味","花茶"], "flavor_preference", "花香"],
  [["咖啡香","咖啡"], "flavor_preference", "咖啡香"],
  [["酸感","酸","柠檬","青柠","微酸"], "flavor_preference", "酸感"],
  [["甜感","甜","蜂蜜","甜食"], "flavor_preference", "甜感"],
  [["苦感","苦","微苦"], "flavor_preference", "苦感"],
  [["气泡感","气泡","汽水","碳酸"], "flavor_preference", "气泡感"],
  // temperature (互斥，覆盖)
  [["热","热一点","温热","暖的","想喝热的"], "temperature_preference", "热饮"],
  [["冷","冰","凉","加冰","想喝冷的","想喝冰"], "temperature_preference", "冷饮"],
  [["常温","不冰不热","温的就行"], "temperature_preference", "常温"],
  // limits
  [["低糖","控糖","少糖","不甜","不要太甜","少甜"], "limits", "低糖"],
  [["低刺激","不刺激","温和","不要太刺激"], "limits", "低刺激"],
  [["咖啡因敏感","咖啡因过敏","不喝咖啡","不要咖啡因","无咖啡因"], "limits", "咖啡因敏感慎用"],
  [["乳糖不耐","不喝奶","不要奶","不含乳"], "limits", "乳糖不耐慎用"],
  [["过敏","过敏原","坚果过敏"], "limits", "过敏风险"],
]

function emptyResult() {
  return { scene: [], body: [], mood: [], needs: [], limits: [], flavor_preference: [], temperature_preference: [] }
}

function keywordParse(message) {
  const result = emptyResult()
  const text = (message || '').toLowerCase()
  for (const [keywords, field, value] of KEYWORD_RULES) {
    for (const kw of keywords) {
      if (text.includes(kw.toLowerCase())) {
        if (!result[field].includes(value)) result[field].push(value)
        break
      }
    }
  }
  return result
}

/**
 * 解析用户聊天消息，提取推荐标签
 * @param {string} message 用户消息
 * @param {object} context 上下文
 * @param {number} timeout 超时 ms
 */
export async function parseIntent(message, context = {}, timeout = 8000) {
  console.log('[intent] request', { message })
  try {
    const result = await new Promise((resolve, reject) => {
      const timer = setTimeout(() => reject(new Error('timeout')), timeout)
      uni.request({
        url: BASE_URL + '/api/intent/parse',
        method: 'POST',
        data: { message, context },
        header: { 'Content-Type': 'application/json' },
        success(res) {
          clearTimeout(timer)
          if (res.statusCode === 200 && res.data) {
            console.log('[intent] result', res.data)
            resolve(res.data)
          } else {
            reject(new Error('status ' + res.statusCode))
          }
        },
        fail(err) {
          clearTimeout(timer)
          reject(err)
        },
      })
    })
    return result
  } catch (err) {
    console.error('[intent failed]', err)
    const fallback = keywordParse(message)
    console.log('[intent] using frontend keyword fallback:', fallback)
    return fallback
  }
}
