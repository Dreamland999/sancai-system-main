/**
 * AI 状态推理 API — 综合 emotion_result + recommend_input + 消息 + 偏好
 */
const BASE_URL = 'http://10.191.133.249:8000';

const DEFAULT_PROFILE = {
  flavor_preference: [],
  temperature_preference: [],
  limits: [],
  profile_initialized: false
};

const EMOTION_MOOD = { '开心': '开心', '平静': '平静', '低落': '低落', '生气': '烦躁', '害怕': '紧张' };

function getTimeOfDay() {
  const h = new Date().getHours();
  if (h >= 5 && h < 12) return 'morning';
  if (h >= 12 && h < 17) return 'afternoon';
  if (h >= 17 && h < 22) return 'evening';
  return 'night';
}

function buildPayload(message) {
  const emotion = uni.getStorageSync('emotion_result') || {};
  const input = uni.getStorageSync('recommend_input') || {};
  const profile = uni.getStorageSync('user_profile') || DEFAULT_PROFILE;
  const initialized = profile.profile_initialized === true;
  return {
    message,
    emotion_result: { emotion: emotion.emotion || '', emotion_cn: emotion.emotion_cn || '', confidence: emotion.confidence || 0 },
    recommend_input: {
      scene: input.scene || [], body: input.body || [], mood: input.mood || [], needs: input.needs || [],
      limits: input.limits || [], flavor_preference: input.flavor_preference || [], temperature_preference: input.temperature_preference || []
    },
    user_profile: {
      flavor_preference: initialized ? (profile.flavor_preference || []) : [],
      temperature_preference: initialized ? (profile.temperature_preference || []) : [],
      limits: initialized ? (profile.limits || []) : []
    },
    context: { time_of_day: getTimeOfDay() }
  };
}

function fallbackStateInfer(message) {
  const emotion = uni.getStorageSync('emotion_result') || {};
  const input = uni.getStorageSync('recommend_input') || {};
  const state = {
    scene: [...(input.scene || [])], body: [...(input.body || [])], mood: [...(input.mood || [])],
    needs: [...(input.needs || [])], limits: [...(input.limits || [])],
    flavor_preference: [...(input.flavor_preference || [])], temperature_preference: [...(input.temperature_preference || [])]
  };
  const text = message.toLowerCase();

  // body
  if (['睡不好','困','想睡','没睡好','犯困','好困'].some(k => text.includes(k)) && state.body.indexOf('困倦') === -1) state.body.push('困倦');
  if (['累','疲惫','没力气','没精神','好累'].some(k => text.includes(k)) && state.body.indexOf('疲劳') === -1) state.body.push('疲劳');
  if (['状态很好','身体良好','没啥不舒服','感觉不错','我很好'].some(k => text.includes(k))) state.body = ['良好'];
  if (['饿','饥饿','肚子饿','没吃饭'].some(k => text.includes(k)) && state.body.indexOf('饥饿') === -1) state.body.push('饥饿');
  if (['饱','吃饱','吃撑'].some(k => text.includes(k)) && state.body.indexOf('饱腹') === -1) state.body.push('饱腹');
  if (['有点热','感觉热','很热'].some(k => text.includes(k)) && state.body.indexOf('感觉有点热') === -1) state.body.push('感觉有点热');
  if (['有点冷','感觉冷','很冷'].some(k => text.includes(k)) && state.body.indexOf('感觉有点冷') === -1) state.body.push('感觉有点冷');
  if (['渴','口干','想喝水','口渴'].some(k => text.includes(k)) && state.body.indexOf('口渴') === -1) state.body.push('口渴');
  // mood
  if (['开心','高兴','愉快','快乐'].some(k => text.includes(k)) && state.mood.indexOf('开心') === -1) state.mood.push('开心');
  if (['平静','还行','还可以','一般般'].some(k => text.includes(k)) && state.mood.indexOf('平静') === -1) state.mood.push('平静');
  if (['兴奋','激动','期待'].some(k => text.includes(k)) && state.mood.indexOf('兴奋') === -1) state.mood.push('兴奋');
  if (['低落','不开心','沮丧','难过'].some(k => text.includes(k)) && state.mood.indexOf('低落') === -1) state.mood.push('低落');
  if (['烦','烦躁','心浮气躁'].some(k => text.includes(k)) && state.mood.indexOf('烦躁') === -1) state.mood.push('烦躁');
  if (['紧张','心慌','不安'].some(k => text.includes(k)) && state.mood.indexOf('紧张') === -1) state.mood.push('紧张');
  if (['无聊','没什么意思'].some(k => text.includes(k)) && state.mood.indexOf('无聊') === -1) state.mood.push('无聊');
  if (['孤单','孤独','寂寞'].some(k => text.includes(k)) && state.mood.indexOf('孤单') === -1) state.mood.push('孤单');
  // scene
  if (['家','家里','在家','宿舍','寝室'].some(k => text.includes(k))) state.scene = ['家/宿舍'];
  if (['学校','教学楼','上课','教室'].some(k => text.includes(k))) state.scene = ['学校/教学楼'];
  if (['图书馆','自习室','自习'].some(k => text.includes(k))) state.scene = ['图书馆/自习室'];
  if (['办公室','公司','上班','工位'].some(k => text.includes(k))) state.scene = ['办公室/公司'];
  if (['餐厅','食堂','吃饭'].some(k => text.includes(k))) state.scene = ['餐厅/食堂'];
  if (['健身房','运动场','锻炼','健身'].some(k => text.includes(k))) state.scene = ['健身房/运动场'];
  if (['咖啡店','奶茶店'].some(k => text.includes(k))) state.scene = ['咖啡店/奶茶店'];
  if (['商场','逛街','购物','商业区'].some(k => text.includes(k))) state.scene = ['商场/商业街'];
  if (['地铁','公交','车站','通勤','路上'].some(k => text.includes(k))) state.scene = ['地铁/公交/车站'];
  if (['公园','户外','外面','野餐'].some(k => text.includes(k))) state.scene = ['公园/户外'];
  // flavor
  if (['清爽','清淡'].some(k => text.includes(k)) && state.flavor_preference.indexOf('清爽') === -1) state.flavor_preference.push('清爽');
  if (['奶香','奶味','牛奶','奶盖'].some(k => text.includes(k)) && state.flavor_preference.indexOf('奶香') === -1) state.flavor_preference.push('奶香');
  if (['茶香','茶味','茶底'].some(k => text.includes(k)) && state.flavor_preference.indexOf('茶香') === -1) state.flavor_preference.push('茶香');
  if (['果香','果味','水果'].some(k => text.includes(k)) && state.flavor_preference.indexOf('果香') === -1) state.flavor_preference.push('果香');
  if (['花香','花的味道'].some(k => text.includes(k)) && state.flavor_preference.indexOf('花香') === -1) state.flavor_preference.push('花香');
  if (['咖啡香','咖啡'].some(k => text.includes(k)) && state.flavor_preference.indexOf('咖啡香') === -1) state.flavor_preference.push('咖啡香');
  if (['酸','酸感','柠檬','青柠'].some(k => text.includes(k)) && state.flavor_preference.indexOf('酸感') === -1) state.flavor_preference.push('酸感');
  if (['甜','甜感','蜂蜜'].some(k => text.includes(k)) && state.flavor_preference.indexOf('甜感') === -1) state.flavor_preference.push('甜感');
  if (['苦','苦感','微苦'].some(k => text.includes(k)) && state.flavor_preference.indexOf('苦感') === -1) state.flavor_preference.push('苦感');
  if (['气泡','气泡感','汽水','碳酸'].some(k => text.includes(k)) && state.flavor_preference.indexOf('气泡感') === -1) state.flavor_preference.push('气泡感');
  // temperature — 互斥
  if (['热','热一点','温热','暖的','想喝热的'].some(k => text.includes(k))) state.temperature_preference = ['热饮'];
  else if (['冷','冰','凉','加冰','想喝冷的','想喝冰'].some(k => text.includes(k))) state.temperature_preference = ['冷饮'];
  else if (['常温','不冰不热'].some(k => text.includes(k))) state.temperature_preference = ['常温'];
  // limits
  if (['低糖','控糖','少糖','不要太甜'].some(k => text.includes(k)) && state.limits.indexOf('低糖') === -1) state.limits.push('低糖');
  if (['低刺激','不刺激','温和'].some(k => text.includes(k)) && state.limits.indexOf('低刺激') === -1) state.limits.push('低刺激');
  if (['咖啡因敏感','不喝咖啡','咖啡因过敏','咖啡因'].some(k => text.includes(k)) && state.limits.indexOf('咖啡因敏感慎用') === -1) state.limits.push('咖啡因敏感慎用');
  if (['乳糖不耐','不喝奶','不要奶','不含乳'].some(k => text.includes(k)) && state.limits.indexOf('乳糖不耐慎用') === -1) state.limits.push('乳糖不耐慎用');
  if (['过敏','过敏原','坚果过敏'].some(k => text.includes(k)) && state.limits.indexOf('过敏风险') === -1) state.limits.push('过敏风险');
  // mood from camera
  if ((!state.mood || !state.mood.length) && emotion.emotion_cn && emotion.emotion !== 'unknown') {
    const m = EMOTION_MOOD[emotion.emotion_cn]; if (m) state.mood = [m];
  }
  // long-term profile
  const profile = uni.getStorageSync('user_profile') || DEFAULT_PROFILE;
  if (profile.flavor_preference) for (const v of profile.flavor_preference) { if (state.flavor_preference.indexOf(v) === -1) state.flavor_preference.push(v); }
  if (profile.limits) for (const v of profile.limits) { if (state.limits.indexOf(v) === -1) state.limits.push(v); }
  if (profile.temperature_preference && profile.temperature_preference.length && !state.temperature_preference.length) {
    state.temperature_preference = [...profile.temperature_preference];
  }

  const parts = [];
  if (state.mood.length) parts.push('心境' + state.mood.join('、'));
  if (state.body.length) parts.push(state.body.join('、'));
  let summary = parts.length ? `小才看到你${parts.join('，')}。是否确认推荐？` : '小才已收到你的信息。是否推荐？';
  return { summary, state_guess: state, confidence: parts.length ? 0.75 : 0.5, need_confirm: true };
}

export async function inferState(message, timeout = 15000) {
  const payload = buildPayload(message);
  console.log('[state] infer request', JSON.stringify(payload));
  try {
    const [err, res] = await new Promise(resolve => {
      uni.request({ url: `${BASE_URL}/api/state/infer`, method: 'POST', data: payload, timeout,
        success(r) { resolve([null, r]); }, fail(e) { resolve([e, null]); } });
    });
    if (err || !res || res.statusCode < 200 || res.statusCode >= 300) throw new Error(err ? err.errMsg : `HTTP ${res ? res.statusCode : '?'}`);
    const result = res.data;
    console.log('[state] infer result', JSON.stringify(result));
    return result;
  } catch (e) {
    console.error('[state] infer failed, using fallback:', e);
    const fb = fallbackStateInfer(message);
    console.log('[state] fallback result', JSON.stringify(fb));
    return fb;
  }
}
