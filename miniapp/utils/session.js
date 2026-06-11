/**
 * 会话管理 — 新一轮制作开始时重置推荐相关状态
 */

const RESET_KEYS = [
  'recommend_input',
  'recommend_result',
  'current_recipe',
  'custom_recipe_config',
  'emotion_result',
  'state_guess',
  'recognition_flow',
];

const DEFAULT_INPUT = {
  scene: [],
  body: [],
  mood: [],
  needs: [],
  limits: [],
  flavor_preference: [],
  temperature_preference: [],
};

export function resetRecommendSession() {
  for (const key of RESET_KEYS) {
    try {
      uni.removeStorageSync(key);
    } catch (e) {
      // ignore
    }
  }
  uni.setStorageSync('recommend_input', DEFAULT_INPUT);
  console.log('[session] reset recommend session');
}
