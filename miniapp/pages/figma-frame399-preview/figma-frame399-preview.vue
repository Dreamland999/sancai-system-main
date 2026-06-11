<template>
  <view class="frame-399">
    <!-- 顶部白色底色 -->
    <view class="top-bar"></view>

    <!-- 假状态栏已移除（真机系统自带） -->

    <!-- 假底部 Home Indicator 已移除（真机系统自带） -->

    <!-- 返回箭头 -->
    <view class="back-hit" @tap="onBack">
      <image class="ico-back" src="/static/figma-frame399/right0.svg" mode="aspectFit" />
    </view>
    <!-- 标题 -->
    <view class="txt-title">AI定制</view>
    <!-- 历史（使用 right 定位避开微信胶囊按钮） -->
    <view class="txt-history" @tap="onHistory">历史</view>

    <!-- 内容区：AI 头像 + 消息列表 -->
    <view class="content-area">
      <!-- AI 头像圆形背景 -->
      <view class="avatar-circle"></view>
      <!-- 头像图片 -->
      <image
        class="avatar-img"
        src="/static/figma-frame399/b-8-b-9-a-543-d-10-f-48-fafb-88-aa-0-fb-39-d-4987-10.png"
        mode="aspectFill"
      />

      <!-- 消息列表 -->
      <view class="msg-list">
        <view
          v-for="(msg, i) in messages"
          :key="i"
          :class="msg.role === 'user' ? 'msg-user' : 'msg-ai'"
        >
          <text class="msg-text">{{ msg.text }}</text>
        </view>
        <!-- AI 确认卡 -->
        <view v-if="showConfirmRecommend" class="confirm-card">

          <!-- A. 小才推测（body/mood/scene） -->
          <view class="confirm-section">
            <view class="confirm-section-title">
              小才推测
              <text v-if="panelStatus === 'analyzing'" class="guess-status-text">分析中...</text>
            </view>
            <view v-if="guessStateTags.length" class="confirm-card-tags">
              <view v-for="tag in guessStateTags" :key="'gs'+tag"
                class="confirm-tag" :class="tag.c">{{ tag.text }}</view>
            </view>
            <view v-else class="confirm-tag confirm-tag-empty">{{ guessPanelHint }}</view>
          </view>

          <!-- B. 此次偏好（flavor/temperature/limits，仅当有值时显示） -->
          <view v-if="tempPrefTags.length" class="confirm-section">
            <view class="confirm-section-title">此次偏好</view>
            <view class="confirm-card-tags">
              <view v-for="tag in tempPrefTags" :key="'tp'+tag"
                class="confirm-tag" :class="tag.c">{{ tag.text }}</view>
            </view>
          </view>

          <!-- C. 长期偏好 -->
          <view class="confirm-section">
            <view class="confirm-section-title">长期偏好</view>
            <view v-if="showProfileSetup">
              <view class="profile-setup">
                <view class="profile-setup-label">风味偏好</view>
                <view class="profile-setup-tags">
                  <view v-for="t in flavorOptions" :key="'pf'+t"
                    class="profile-tag" :class="{ 'profile-tag-sel': prefFlavor.indexOf(t) !== -1 }"
                    @tap="onToggleFlavor(t)">{{ t }}</view>
                </view>
                <view class="profile-setup-label">冷热偏好</view>
                <view class="profile-setup-tags">
                  <view v-for="t in tempOptions" :key="'pt'+t"
                    class="profile-tag" :class="{ 'profile-tag-sel': prefTemp.indexOf(t) !== -1 }"
                    @tap="onToggleTemp(t)">{{ t }}</view>
                </view>
                <view class="profile-setup-label">健康约束</view>
                <view class="profile-setup-tags">
                  <view v-for="t in limitOptions" :key="'pl'+t"
                    class="profile-tag" :class="{ 'profile-tag-sel': prefLimits.indexOf(t) !== -1 }"
                    @tap="onToggleLimit(t)">{{ t }}</view>
                </view>
                <view class="profile-setup-btns">
                  <view class="profile-setup-btn-save" @tap="onSaveProfile">保存偏好</view>
                  <view class="profile-setup-btn-skip" @tap="onSkipProfile">跳过</view>
                </view>
              </view>
            </view>
            <view v-else>
              <view v-if="!showEditProfile">
                <view v-if="profileTagList.length" class="confirm-card-tags">
                  <view v-for="tag in profileTagList" :key="'lt'+tag"
                    class="confirm-tag" :class="tag.c">{{ tag.text }}</view>
                </view>
                <view v-else class="confirm-tag confirm-tag-empty">暂无长期偏好</view>
                <view class="profile-actions">
                  <view class="profile-action-edit" @tap="onStartEditProfile">修改偏好</view>
                  <view class="profile-action-reset" @tap="onResetProfile">重设偏好</view>
                </view>
              </view>
              <view v-else class="profile-setup">
                <view class="profile-setup-label">风味偏好</view>
                <view class="profile-setup-tags">
                  <view v-for="t in flavorOptions" :key="'ef'+t"
                    class="profile-tag" :class="{ 'profile-tag-sel': editFlavor.indexOf(t) !== -1 }"
                    @tap="onEditToggleFlavor(t)">{{ t }}</view>
                </view>
                <view class="profile-setup-label">冷热偏好</view>
                <view class="profile-setup-tags">
                  <view v-for="t in tempOptions" :key="'et'+t"
                    class="profile-tag" :class="{ 'profile-tag-sel': editTemp.indexOf(t) !== -1 }"
                    @tap="onEditToggleTemp(t)">{{ t }}</view>
                </view>
                <view class="profile-setup-label">健康约束</view>
                <view class="profile-setup-tags">
                  <view v-for="t in limitOptions" :key="'el'+t"
                    class="profile-tag" :class="{ 'profile-tag-sel': editLimits.indexOf(t) !== -1 }"
                    @tap="onEditToggleLimit(t)">{{ t }}</view>
                </view>
                <view class="profile-setup-btns">
                  <view class="profile-setup-btn-save" @tap="onSaveEditProfile">保存修改</view>
                  <view class="profile-setup-btn-skip" @tap="onCancelEditProfile">取消</view>
                </view>
              </view>
            </view>
          </view>

          <view v-if="confirmationSummary.text" class="confirm-card-footer">
            {{ confirmationSummary.text }}
          </view>

          <view class="confirm-card-btns">
            <view
              class="confirm-card-btn"
              :class="{ 'btn-disabled': panelStatus !== 'ready' }"
              @tap="onConfirmRecommend"
            >确认推荐</view>
            <view
              class="confirm-card-btn-alt"
              :class="{ 'btn-disabled': panelStatus === 'analyzing' || panelStatus === 'idle' }"
              @tap="onGoAdjust"
            >调整状态</view>
          </view>
        </view>
      </view>
    </view>

    <!-- 底部输入区 -->
    <view class="input-area">
      <input
        class="input-real"
        v-model="chatText"
        placeholder="请输入你的思绪…"
        :disabled="sending"
        confirm-type="send"
        @confirm="onSend"
      />
      <!-- 发送文字按钮 -->
      <view class="btn-send" @tap="onSend">发送</view>
      <!-- 相机图标 -->
      <image class="ico-camera" src="/static/figma-frame399/camera0.svg" mode="aspectFit" @tap="onCamera" />
      <!-- 语音图标 -->
      <image
        class="ico-voice"
        :class="{ 'ico-voice-recording': isVoiceRecording }"
        src="/static/figma-frame399/voice0.svg"
        mode="aspectFit"
        @tap="onVoice"
      />
      <!-- 绿色按钮（进入推荐） -->
      <view class="mic-circle" @tap="onGoRecommend">
        <text class="mic-label">推荐</text>
      </view>
    </view>
  </view>
</template>

<script>
import { goBack } from '@/utils/nav.js';
import { sendMessage } from '@/api/ai.js';
import { parseIntent } from '@/api/intent.js';
import { inferState } from '@/api/state.js';
import { recommend } from '@/api/recommend.js';

function mergeTags(existing, parsed) {
  const fields = ['scene', 'body', 'mood', 'needs', 'limits', 'flavor_preference', 'temperature_preference'];
  const merged = {};
  for (const f of fields) {
    const set = new Set([...(existing[f] || []), ...(parsed[f] || [])]);
    merged[f] = [...set];
  }
  return merged;
}

export default {
  name: "FigmaFrame399Preview",
  data() {
    return {
      chatText: '',
      messages: [
        { role: 'ai', text: '今天感觉怎么样？外面高温酷暑，进入空调房前要小心冷热交替着凉' },
      ],
      sending: false,
      hasChatted: false,
      showConfirmRecommend: true,
      panelStatus: 'idle',  // idle | analyzing | ready | error
      pendingStateGuess: null,
      confirmedInput: { scene:[], body:[], mood:[], needs:[], limits:[], flavor_preference:[], temperature_preference:[] },
      isVoiceRecording: false,
      voiceRecognizing: false,
      showEditProfile: false,
      editFlavor: [],
      editTemp: [],
      editLimits: [],
      prefFlavor: [],
      prefTemp: [],
      prefLimits: [],
      flavorOptions: ['清爽', '奶香', '茶香', '果香', '花香', '咖啡香', '酸感', '甜感', '苦感', '气泡感'],
      tempOptions: ['热饮', '冷饮', '常温'],
      limitOptions: ['低糖', '低刺激', '咖啡因敏感慎用', '乳糖不耐慎用', '过敏风险'],
      confirmationSummary: {
        emotion: null,
        body: [],
        mood: [],
        scene: [],
        needs: [],
        flavor: [],
        temperature: [],
        limits: [],
        isEmpty: true,
        text: '你可以先输入一些感受，小才帮你整理~'
      },
    };
  },
  computed: {
    /** A. 小才推测 — 仅 body/mood/scene */
    guessStateTags() {
      const ci = this.confirmedInput;
      const tags = [];
      const arr = (v) => v || [];
      arr(ci.body).forEach(t => tags.push({ text: t, c: 'confirm-tag-body' }));
      arr(ci.mood).forEach(t => tags.push({ text: t, c: 'confirm-tag-mood' }));
      arr(ci.scene).forEach(t => tags.push({ text: t, c: 'confirm-tag-scene' }));
      return tags;
    },
    /** 面板底部提示 — 根据 panelStatus 切换 */
    guessPanelHint() {
      switch (this.panelStatus) {
        case 'analyzing': return '正在分析你的身体和心情...';
        case 'error': return '暂时没分析出来，可以继续和我聊聊～';
        case 'ready': return '等待你的状态';
        default: return '告诉我今天的身体和心情，我会帮你匹配饮品';
      }
    },
    /** B. 此次偏好 — flavor/temp/limits（仅当有值时显示） */
    tempPrefTags() {
      const ci = this.confirmedInput;
      const tags = [];
      const arr = (v) => v || [];
      arr(ci.flavor_preference).forEach(t => tags.push({ text: t, c: 'confirm-tag-flavor' }));
      arr(ci.temperature_preference).forEach(t => tags.push({ text: t, c: 'confirm-tag-temp' }));
      arr(ci.limits).forEach(t => tags.push({ text: t, c: 'confirm-tag-limits' }));
      return tags;
    },
    /** C. 长期偏好标签 */
    profileTagList() {
      const p = uni.getStorageSync('user_profile') || {};
      const tags = [];
      const arr = (v) => v || [];
      arr(p.flavor_preference).forEach(t => tags.push({ text: t, c: 'confirm-tag-flavor' }));
      arr(p.temperature_preference).forEach(t => tags.push({ text: t, c: 'confirm-tag-temp' }));
      arr(p.limits).forEach(t => tags.push({ text: t, c: 'confirm-tag-limits' }));
      return tags;
    },
    showProfileSetup() {
      const p = uni.getStorageSync('user_profile') || {};
      return !p.profile_initialized && this.showConfirmRecommend;
    },
    hasPrefSelection() {
      return this.prefFlavor.length || this.prefTemp.length || this.prefLimits.length;
    },
    hasUserProfile() {
      const p = uni.getStorageSync('user_profile') || {};
      return p.profile_initialized === true;
    },
    userProfileFlavor() {
      return ((uni.getStorageSync('user_profile') || {}).flavor_preference) || [];
    },
    userProfileTemp() {
      return ((uni.getStorageSync('user_profile') || {}).temperature_preference) || [];
    },
    userProfileLimits() {
      return ((uni.getStorageSync('user_profile') || {}).limits) || [];
    }
  },
  mounted() {
    const profile = uni.getStorageSync('user_profile') || {};
    console.log('[Frame399] user_profile loaded', JSON.stringify(profile));
    console.log('[Frame399] profile_initialized', profile.profile_initialized === true);
    if (!profile.profile_initialized) {
      console.log('[Frame399] 测试首次用户：控制台执行 uni.removeStorageSync("user_profile") 后重进');
    }
    this._autoInferOnEntry();
  },
  methods: {
    /** 同步 storage 到 reactive confirmedInput，保证 UI 响应更新 */
    syncConfirmedInput() {
      const ri = uni.getStorageSync('recommend_input') || {};
      // normalize old tags
      const tempNorm = (t) => t === '热' ? '热饮' : t === '冷' ? '冷饮' : t;
      const limitNorm = (t) => t === '不含乳' ? '乳糖不耐慎用' : t === '不含咖啡因' ? '咖啡因敏感慎用' : t === '无过敏原' ? '过敏风险' : t;
      this.confirmedInput = {
        scene: (ri.scene || []).map(s => s === '商场/商业区' ? '商场/商业街' : s === '地铁/公交' ? '地铁/公交/车站' : s),
        body: ri.body || [],
        mood: ri.mood || [],
        needs: ri.needs || [],
        limits: (ri.limits || []).map(limitNorm),
        flavor_preference: ri.flavor_preference || [],
        temperature_preference: (ri.temperature_preference || []).map(tempNorm)
      };
      console.log('[Frame399] confirmedInput synced', JSON.stringify(this.confirmedInput));
    },
    async _autoInferOnEntry() {
      this.syncConfirmedInput();
      const emotion = uni.getStorageSync('emotion_result');
      const input = uni.getStorageSync('recommend_input') || {};
      // 只自动展示情绪识别结果 + 偏好区，不自动生成完整 state_guess
      const hasBodyOrScene = (input.body && input.body.length) || (input.scene && input.scene.length);
      const hasMoodOnly = !hasBodyOrScene && (input.mood && input.mood.length);

      // 构建轻量确认卡
      const summary = {
        emotion: (emotion && emotion.emotion_cn) ? emotion.emotion_cn : null,
        body: input.body || [],
        mood: input.mood || [],
        scene: input.scene || [],
        needs: [],
        flavor: input.flavor_preference || [],
        temperature: input.temperature_preference || [],
        limits: input.limits || [],
        isEmpty: !emotion && !hasBodyOrScene && !(input.mood && input.mood.length),
        text: ''
      };

      const profile = uni.getStorageSync('user_profile') || {};
      const isFirstTime = !profile.profile_initialized;
      let hasExistingData = false;

      if (emotion && emotion.emotion_cn && emotion.emotion !== 'unknown') {
        hasExistingData = true;
        if (isFirstTime) {
          const ecn = emotion.emotion_cn;
          summary.text = `小才识别到你当前心境偏${ecn}。第一次使用前，想了解你的长期偏好：你平时喜欢清爽、花香还是低甜？常喝热饮、冷饮还是常温？有没有不含乳、不含咖啡因等限制？`;
        } else if (hasBodyOrScene) {
          summary.text = `小才识别到你当前心境偏${emotion.emotion_cn}。确认这些状态后为你推荐饮品？`;
        } else {
          summary.text = `小才识别到你当前心境偏${emotion.emotion_cn}，可以继续告诉我你的身体状态或饮用偏好。`;
        }
      } else if (isFirstTime) {
        hasExistingData = true;
        summary.text = '第一次使用前，想了解你的长期偏好：你平时喜欢什么口味？常喝热饮还是冷饮？有没有饮食限制？可以在下方偏好区选择。';
      } else if (hasBodyOrScene) {
        hasExistingData = true;
        summary.text = '确认这些状态后为你推荐饮品？';
      }

      this.confirmationSummary = summary;
      this.panelStatus = hasExistingData ? 'ready' : 'idle';
      this.showConfirmRecommend = true;
    },
    onBack() {
      goBack();
    },
    onHistory() {
      uni.showToast({ title: "历史", icon: "none" });
    },
    onSaveProfile() {
      const profile = {
        flavor_preference: [...this.prefFlavor],
        temperature_preference: [...this.prefTemp],
        limits: [...this.prefLimits],
        profile_initialized: true
      };
      uni.setStorageSync('user_profile', profile);
      console.log('[Frame399] user_profile saved', JSON.stringify(profile));
      uni.showToast({ title: '已保存偏好', icon: 'none' });
    },
    onSkipProfile() {
      const profile = {
        flavor_preference: [],
        temperature_preference: [],
        limits: [],
        profile_initialized: true
      };
      uni.setStorageSync('user_profile', profile);
      console.log('[Frame399] user_profile skipped (empty)');
      uni.showToast({ title: '已跳过', icon: 'none' });
    },
    // ── 修改偏好 ──
    onStartEditProfile() {
      const p = uni.getStorageSync('user_profile') || {};
      this.editFlavor = [...(p.flavor_preference || [])];
      this.editTemp = [...(p.temperature_preference || [])];
      this.editLimits = [...(p.limits || [])];
      this.showEditProfile = true;
    },
    onSaveEditProfile() {
      const p = uni.getStorageSync('user_profile') || {};
      p.flavor_preference = [...this.editFlavor];
      p.temperature_preference = [...this.editTemp];
      p.limits = [...this.editLimits];
      p.profile_initialized = true;
      uni.setStorageSync('user_profile', p);
      this.showEditProfile = false;
      console.log('[Frame399] user_profile updated', JSON.stringify(p));
      uni.showToast({ title: '偏好已更新', icon: 'none' });
    },
    onCancelEditProfile() {
      this.showEditProfile = false;
    },
    onEditToggleFlavor(t) {
      const idx = this.editFlavor.indexOf(t);
      idx === -1 ? this.editFlavor.push(t) : this.editFlavor.splice(idx, 1);
    },
    onEditToggleTemp(t) {
      this.editTemp = [t];
    },
    onEditToggleLimit(t) {
      const idx = this.editLimits.indexOf(t);
      idx === -1 ? this.editLimits.push(t) : this.editLimits.splice(idx, 1);
    },
    // ── 聊天中提取长期偏好预填标签 ──
    _prefillProfileFromChat(text) {
      const profile = uni.getStorageSync('user_profile') || {};
      if (profile.profile_initialized) return; // 已初始化不预填
      const t = text.toLowerCase();
      // 口味
      this.flavorOptions.forEach(f => {
        const kw = f.toLowerCase();
        if (t.includes(kw) && this.prefFlavor.indexOf(f) === -1) {
          this.prefFlavor.push(f);
        }
      });
      // 冷热
      if (['热','热的','温热','暖的'].some(kw => t.includes(kw))) { this.prefTemp = ['热饮']; }
      else if (['冷','冰的','冰','冷的','凉'].some(kw => t.includes(kw))) { this.prefTemp = ['冷饮']; }
      else if (t.includes('常温')) { this.prefTemp = ['常温']; }
    },
    // ── 测试重设 ──
    onResetProfile() {
      uni.removeStorageSync('user_profile');
      this.showEditProfile = false;
      console.log('[Frame399] user_profile cleared for testing');
      uni.showToast({ title: '偏好已重设，刷新确认卡', icon: 'none' });
    },
    onToggleFlavor(t) {
      const idx = this.prefFlavor.indexOf(t);
      idx === -1 ? this.prefFlavor.push(t) : this.prefFlavor.splice(idx, 1);
    },
    onToggleTemp(t) {
      this.prefTemp = [t]; // 单选覆盖
    },
    onToggleLimit(t) {
      const idx = this.prefLimits.indexOf(t);
      idx === -1 ? this.prefLimits.push(t) : this.prefLimits.splice(idx, 1);
    },
    onCamera() {
      uni.showToast({ title: '相机暂未接入', icon: 'none' });
    },
    onVoice() {
      // #ifdef MP-WEIXIN
      if (this.isVoiceRecording) {
        this._stopVoice();
      } else if (!this.voiceRecognizing) {
        this._startVoice();
      }
      // #endif
      // #ifndef MP-WEIXIN
      uni.showToast({ title: '语音识别暂不可用，请手动输入', icon: 'none' });
      // #endif
    },
    _startVoice() {
      this.isVoiceRecording = true;
      uni.showToast({ title: '正在聆听...', icon: 'none', duration: 1500 });
      // #ifdef MP-WEIXIN
      let plugin;
      try {
        plugin = requirePlugin && requirePlugin('WechatSI');
      } catch (e) {
        plugin = null;
      }
      if (!plugin) {
        this.isVoiceRecording = false;
        uni.showToast({ title: '语音识别暂不可用，请手动输入', icon: 'none' });
        return;
      }
      const manager = plugin.getRecordRecognitionManager();
      manager.onStart = () => {
        console.log('[voice] recording started');
      };
      manager.onRecognize = (res) => {
        console.log('[voice] recognizing:', res.result);
      };
      manager.onStop = (res) => {
        this.isVoiceRecording = false;
        this.voiceRecognizing = false;
        const text = res && res.result ? res.result : '';
        console.log('[voice] recognized text:', text);
        if (text) {
          this.chatText = text;
          this.onSend();
        } else {
          uni.showToast({ title: '没有听清，请再说一次', icon: 'none' });
        }
      };
      manager.onError = (err) => {
        console.error('[voice] recognize failed', err);
        this.isVoiceRecording = false;
        this.voiceRecognizing = false;
        uni.showToast({ title: '语音识别失败，请手动输入', icon: 'none' });
      };
      manager.start({ lang: 'zh_CN' });
      // #endif
    },
    _stopVoice() {
      this.isVoiceRecording = false;
      this.voiceRecognizing = true;
      // #ifdef MP-WEIXIN
      try {
        const plugin = requirePlugin && requirePlugin('WechatSI');
        if (plugin) {
          const manager = plugin.getRecordRecognitionManager();
          manager.stop();
        }
      } catch (e) { /* ignore */ }
      // #endif
    },
    buildConfirmationSummary(stateResult, latestInput) {
      const ci = latestInput || this.confirmedInput;
      const emotion = uni.getStorageSync('emotion_result');

      const summary = {
        emotion: (emotion && emotion.emotion_cn) ? emotion.emotion_cn : null,
        body: ci.body || [],
        mood: ci.mood || [],
        scene: ci.scene || [],
        needs: [],
        flavor: ci.flavor_preference || [],
        temperature: ci.temperature_preference || [],
        limits: ci.limits || []
      };

      summary.isEmpty = !summary.emotion && !summary.body.length && !summary.mood.length && !summary.scene.length
        && !summary.flavor.length && !summary.temperature.length && !summary.limits.length;

      if (stateResult && stateResult.summary) {
        summary.text = stateResult.summary;
      } else if (summary.isEmpty) {
        summary.text = '你可以先输入一些感受，小才帮你整理~';
      } else {
        summary.text = '确认这些信息为你推荐饮品？';
      }

      this.confirmationSummary = summary;
      this.pendingStateGuess = stateResult || null;
      console.log('[Frame399] summary confirmed mood', JSON.stringify(summary.mood));
      console.log('[Frame399] summary confirmed body', JSON.stringify(summary.body));
      console.log('[Frame399] summary confirmed scene', JSON.stringify(summary.scene));
    },
    async onSend() {
      const userMsg = this.chatText.trim();
      if (!userMsg) {
        uni.showToast({ title: '请输入内容', icon: 'none' });
        return;
      }
      console.log('[Frame399] user input:', userMsg);
      if (this.sending) return;
      this.sending = true;
      this.panelStatus = 'analyzing';
      this.chatText = '';
      this.messages.push({ role: 'user', text: userMsg });
      this.messages.push({ role: 'ai', text: '...' });

      // 并行：chat 回复 + intent 解析
      const context = { recommend_input: uni.getStorageSync('recommend_input') || {} };
      let reply;
      let intentRes = null;
      try {
        const [chatRes, parsedIntent] = await Promise.all([
          sendMessage(userMsg, context).catch(e => {
            console.error('[Frame399] chat error:', e);
            return null;
          }),
          parseIntent(userMsg, context).catch(e => {
            console.error('[Frame399] intent parse error:', e);
            return null;
          }),
        ]);
        intentRes = parsedIntent;
        console.log('[Frame399] sendMessage result:', chatRes);
        console.log('[Frame399] parseIntent result:', intentRes);
        reply = (chatRes && chatRes.reply) ? chatRes.reply : '今天高温，建议来一杯清热解暑的茉莉薄荷茶~';

        // Step 1: 用户明确表达 → 合并到 recommend_input（已确认状态）
        if (intentRes) {
          const existing = uni.getStorageSync('recommend_input') || {};
          const confirmed = this.mergeConfirmedInput(existing, intentRes);
          uni.setStorageSync('recommend_input', confirmed);
          this.syncConfirmedInput();
          console.log('[Frame399] input after intent merge (confirmed)', JSON.stringify(confirmed));
        }
      } catch (e) {
        console.error('[Frame399] unexpected error:', e);
        reply = '今天高温，建议来一杯清热解暑的茉莉薄荷茶~';
        this.panelStatus = 'error';
      }

      this.messages[this.messages.length - 1] = { role: 'ai', text: reply };
      this.sending = false;
      this.hasChatted = true;

      const input = uni.getStorageSync('recommend_input') || {};
      console.log('[Frame399] recommend_input before state infer', JSON.stringify(input));

      // 调用 AI 状态推理
      let stateResult = null;
      try {
        stateResult = await inferState(userMsg);
        console.log('[Frame399] state_guess received', JSON.stringify(stateResult));
      } catch (e) {
        console.error('[Frame399] inferState error:', e);
      }

      // 如果未初始化，尝试从聊天中提取长期偏好预填标签
      this._prefillProfileFromChat(userMsg);
      this.buildConfirmationSummary(stateResult, this.confirmedInput);
      this.panelStatus = (intentRes || stateResult) ? 'ready' : 'error';
      this.showConfirmRecommend = true;
    },
    /** 合并用户明确表达的状态到 recommend_input */
    mergeConfirmedInput(existing, incoming) {
      const result = { ...existing };

      // mood: incoming 非空则覆盖
      if (incoming.mood && incoming.mood.length) {
        result.mood = incoming.mood.slice(0, 2);
      }
      // body: 应用互斥规则
      if (incoming.body && incoming.body.length) {
        const arr = [...existing.body || []];
        for (const t of incoming.body) {
          if (t === '良好') {
            result.body = ['良好']; return result;
          }
          if (arr.indexOf(t) !== -1) continue;
          // 清除互斥值
          if (t === '饥饿' && arr.indexOf('饱腹') !== -1) arr.splice(arr.indexOf('饱腹'), 1);
          if (t === '饱腹' && arr.indexOf('饥饿') !== -1) arr.splice(arr.indexOf('饥饿'), 1);
          if (t === '感觉有点冷' && arr.indexOf('感觉有点热') !== -1) arr.splice(arr.indexOf('感觉有点热'), 1);
          if (t === '感觉有点热' && arr.indexOf('感觉有点冷') !== -1) arr.splice(arr.indexOf('感觉有点冷'), 1);
          // 清除"良好"当有不适标签
          const gIdx = arr.indexOf('良好');
          if (gIdx !== -1) arr.splice(gIdx, 1);
          arr.push(t);
        }
        result.body = arr;
      }
      // scene: 覆盖
      if (incoming.scene && incoming.scene.length) {
        result.scene = incoming.scene.slice(0, 1);
      }
      // needs: 合并去重
      if (incoming.needs && incoming.needs.length) {
        result.needs = [...new Set([...(result.needs || []), ...incoming.needs])];
      }
      // temperature: 覆盖
      if (incoming.temperature_preference && incoming.temperature_preference.length) {
        result.temperature_preference = [...incoming.temperature_preference];
      }
      // flavor: 合并去重
      if (incoming.flavor_preference && incoming.flavor_preference.length) {
        result.flavor_preference = [...new Set([...(result.flavor_preference || []), ...incoming.flavor_preference])];
      }
      // limits: 合并去重
      if (incoming.limits && incoming.limits.length) {
        result.limits = [...new Set([...(result.limits || []), ...incoming.limits])];
      }
      return result;
    },
    mergeStateGuess(existing, sg) {
      // body / needs / limits: 合并去重
      const mergeFields = ['body', 'needs', 'limits'];
      for (const k of mergeFields) {
        if (sg[k] && sg[k].length) {
          existing[k] = [...new Set([...(existing[k] || []), ...sg[k]])];
        }
      }
      // mood: 已确认过就不覆盖，只有 existing 为空时才用 state_guess
      if ((!existing.mood || existing.mood.length === 0) && sg.mood && sg.mood.length) {
        existing.mood = sg.mood.slice(0, 2);
      }
      // scene: stateGuess 非空则优先使用
      if (sg.scene && sg.scene.length) {
        existing.scene = [...sg.scene];
      }
      // flavor_preference: 非空则合并去重
      if (sg.flavor_preference && sg.flavor_preference.length) {
        existing.flavor_preference = [...new Set([...(existing.flavor_preference || []), ...sg.flavor_preference])];
      }
      // temperature_preference: 非空则覆盖（避免热饮/冷饮冲突）
      if (sg.temperature_preference && sg.temperature_preference.length) {
        existing.temperature_preference = [...sg.temperature_preference];
      }
      return existing;
    },
    async onConfirmRecommend() {
      if (this.panelStatus !== 'ready') return;
      const input = uni.getStorageSync('recommend_input') || {};

      // 1. 合并 state_guess
      if (this.pendingStateGuess && this.pendingStateGuess.state_guess) {
        this.mergeStateGuess(input, this.pendingStateGuess.state_guess);
      }

      // 2. 保存长期偏好
      const existingProfile = uni.getStorageSync('user_profile') || {};
      const profile = existingProfile.profile_initialized
        ? existingProfile  // 已有偏好，保持不变
        : {                // 首次：保存当前选择或空
            flavor_preference: [...this.prefFlavor],
            temperature_preference: [...this.prefTemp],
            limits: [...this.prefLimits],
            profile_initialized: true
          };
      if (!existingProfile.profile_initialized) {
        uni.setStorageSync('user_profile', profile);
        console.log('[Frame399] user_profile saved', JSON.stringify(profile));
      }

      // 3. 合并长期偏好到 recommend_input（不覆盖本次状态温度）
      if (profile.flavor_preference.length) {
        input.flavor_preference = [...new Set([...(input.flavor_preference || []), ...profile.flavor_preference])];
      }
      if (profile.limits.length) {
        input.limits = [...new Set([...(input.limits || []), ...profile.limits])];
      }
      // 温度：本次状态优先，无本次状态才用长期偏好
      if (!input.temperature_preference || !input.temperature_preference.length) {
        if (profile.temperature_preference.length) {
          input.temperature_preference = [...profile.temperature_preference];
        }
      }

      // 4. normalize 旧标签
      if (input.temperature_preference) {
        input.temperature_preference = input.temperature_preference.map(t => t === '热' ? '热饮' : t === '冷' ? '冷饮' : t);
      }
      if (input.limits) input.limits = input.limits.map(t => t === '不含乳' ? '乳糖不耐慎用' : t === '不含咖啡因' ? '咖啡因敏感慎用' : t === '无过敏原' ? '过敏风险' : t);

      uni.setStorageSync('recommend_input', input);
      console.log('[Frame399] final recommend_input after state confirm', JSON.stringify(input));
      console.log('[Frame399] user_profile saved', JSON.stringify(profile));
      // 5. 调用 /api/recommend 获取真实推荐结果
      uni.removeStorageSync('recommend_result');
      uni.showLoading({ title: '正在生成推荐...' });
      try {
        const result = await recommend(input);
        console.log('[Frame399] recommend result model_mode:', result.model_mode);
        uni.setStorageSync('recommend_result', result);
        uni.hideLoading();
        uni.redirectTo({ url: '/pages/figma-frame391-animation/figma-frame391-animation?type=recommend' });
      } catch (e) {
        console.error('[Frame399] recommend failed:', e);
        uni.hideLoading();
        uni.showToast({ title: '推荐生成失败，请稍后重试', icon: 'none' });
      }
    },
    onGoAdjust() {
      console.log('[Frame399] adjust state -> Frame394');
      uni.navigateTo({ url: '/pages/figma-frame394-preview/figma-frame394-preview' });
    },
    onGoRecommend() {
      console.log('[Frame399] go -> animation -> Frame389');
      uni.redirectTo({ url: '/pages/figma-frame391-animation/figma-frame391-animation?type=recommend' });
    },
  },
};
</script>

<style scoped>
.frame-399 {
  width: 750rpx;
  height: 100vh;
  background: linear-gradient(180deg, rgba(236, 253, 255, 1) 0%, rgba(255, 255, 255, 1) 100%);
  position: relative;
  overflow: hidden;
  padding-bottom: env(safe-area-inset-bottom);
  box-sizing: border-box;
}

/* 顶部白色底色 */
.top-bar {
  background: #ffffff;
  width: 750rpx;
  height: 176rpx;
  position: absolute;
  left: 0;
  top: 0;
}

/* 状态栏 */
.status-bar {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  width: 780rpx;
  position: absolute;
  left: -14rpx;
  top: 0;
  padding: 36rpx 52rpx 28rpx 54rpx;
  box-sizing: border-box;
}
.time-wrap {
  flex-shrink: 0;
  width: 108rpx;
  height: 42rpx;
  position: relative;
}
.time {
  color: #000000;
  text-align: center;
  font-family: "SfProText-Semibold", sans-serif;
  font-size: 34rpx;
  line-height: 44rpx;
  letter-spacing: -0.82rpx;
  font-weight: 600;
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 108rpx;
}
.icons-wrap {
  flex-shrink: 0;
  width: 156rpx;
  height: 26rpx;
  position: relative;
}
.icon-battery {
  width: 54rpx;
  height: 26rpx;
  position: absolute;
  right: 0;
  top: 0;
}
.icon-wifi {
  width: 34rpx;
  height: 24rpx;
  position: absolute;
  left: 53rpx;
  top: 1rpx;
}
.icon-cellular {
  width: 38rpx;
  height: 24rpx;
  position: absolute;
  left: 0;
  top: 1rpx;
}

/* Home Indicator — 锚定底部 */
.home-bar {
  width: 780rpx;
  height: 38rpx;
  position: absolute;
  left: -14rpx;
  top: 1586rpx;
}
.home-bar-inner {
  background: #000000;
  border-radius: 200rpx;
  width: 268rpx;
  height: 10rpx;
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  bottom: 16rpx;
}

/* 返回箭头热区 */
.back-hit {
  position: absolute;
  left: 72rpx;
  top: 90rpx;
  width: 80rpx;
  height: 80rpx;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: center;
}
.ico-back {
  width: 48rpx;
  height: 48rpx;
}

/* 标题 AI定制 */
.txt-title {
  color: #333333;
  text-align: center;
  font-family: "PingFangSc-Medium", sans-serif;
  font-size: 32rpx;
  font-weight: 500;
  position: absolute;
  left: 330rpx;
  top: 108rpx;
}

/* 历史 — right:120rpx 避开微信胶囊按钮 */
.txt-history {
  color: #333333;
  text-align: right;
  font-family: "PingFangSc-Medium", sans-serif;
  font-size: 32rpx;
  font-weight: 500;
  position: absolute;
  right: 120rpx;
  top: 108rpx;
}

/* ===== 内容区 ===== */
.content-area {
  position: absolute;
  left: 40rpx;
  top: 230rpx;
  width: 622rpx;
  height: 1140rpx;
  overflow-y: auto;
}

/* AI 头像圆形渐变背景 */
.avatar-circle {
  background: linear-gradient(205.26deg, rgba(255, 206, 206, 1) 0%, rgba(133, 210, 199, 1) 63.37%, rgba(255, 255, 255, 1) 100%);
  border-radius: 50%;
  width: 80rpx;
  height: 80rpx;
  position: absolute;
  left: 0;
  top: 0;
}

/* 头像图片 */
.avatar-img {
  width: 62rpx;
  height: 62rpx;
  position: absolute;
  left: 8rpx;
  top: 8rpx;
  border-radius: 50%;
}

/* 消息列表 */
.msg-list {
  position: absolute;
  left: 0;
  top: 100rpx;
  width: 622rpx;
  padding-bottom: 40rpx;
}

.msg-user {
  text-align: right;
  margin-bottom: 20rpx;
}

.msg-user .msg-text {
  display: inline-block;
  background: #85d2c7;
  color: #fff;
  border-radius: 16rpx 0 16rpx 16rpx;
  padding: 16rpx 20rpx;
  font-size: 28rpx;
  max-width: 460rpx;
  word-break: break-all;
}

.msg-ai {
  text-align: left;
  margin-bottom: 20rpx;
  padding-left: 40rpx;
}

.msg-ai .msg-text {
  display: inline-block;
  background: rgba(133, 210, 199, 0.2);
  color: #666;
  border-radius: 0 16rpx 16rpx 16rpx;
  padding: 16rpx 20rpx;
  font-size: 28rpx;
  max-width: 460rpx;
  word-break: break-all;
}

/* AI 确认卡 */
.confirm-card {
  margin: 12rpx 0 20rpx 40rpx;
  background: rgba(133, 210, 199, 0.08);
  border: 2rpx solid rgba(133, 210, 199, 0.3);
  border-radius: 16rpx;
  padding: 20rpx 24rpx;
  max-width: 520rpx;
}
.confirm-section {
  margin-bottom: 16rpx;
}
.confirm-section:last-child {
  margin-bottom: 0;
}
.confirm-section-title {
  color: #999;
  font-family: "PingFangSc-Regular", sans-serif;
  font-size: 20rpx;
  margin-bottom: 6rpx;
}
.confirm-tag-guess {
  background: rgba(180, 160, 255, 0.1);
  color: #9b8fd4;
  border: 1rpx dashed rgba(180, 160, 255, 0.5);
  border-radius: 40rpx;
  padding: 6rpx 16rpx;
  font-size: 22rpx;
}

.confirm-card-header {
  color: #333;
  font-family: "PingFangSc-Medium", sans-serif;
  font-size: 26rpx;
  font-weight: 500;
  margin-bottom: 16rpx;
}
.confirm-card-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10rpx 12rpx;
  margin-bottom: 16rpx;
}
.confirm-tag {
  border-radius: 40rpx;
  padding: 6rpx 16rpx;
  font-family: "PingFangSc-Regular", sans-serif;
  font-size: 22rpx;
}
.confirm-tag-emotion {
  background: rgba(255, 158, 190, 0.15);
  color: #e07a9e;
  border: 1rpx solid rgba(255, 158, 190, 0.4);
}
.confirm-tag-body {
  background: rgba(119, 227, 212, 0.12);
  color: #3b9483;
  border: 1rpx solid rgba(119, 227, 212, 0.4);
}
.confirm-tag-mood {
  background: rgba(255, 158, 190, 0.12);
  color: #c47a90;
  border: 1rpx solid rgba(255, 158, 190, 0.4);
}
.confirm-tag-scene {
  background: rgba(255, 165, 165, 0.12);
  color: #c47a6e;
  border: 1rpx solid rgba(255, 165, 165, 0.4);
}
.confirm-tag-needs {
  background: rgba(180, 160, 255, 0.12);
  color: #7a6ec4;
  border: 1rpx solid rgba(180, 160, 255, 0.4);
}
.confirm-tag-flavor {
  background: rgba(135, 190, 255, 0.12);
  color: #5a8ec4;
  border: 1rpx solid rgba(135, 190, 255, 0.4);
}
.confirm-tag-temp {
  background: rgba(255, 220, 130, 0.12);
  color: #c49a3b;
  border: 1rpx solid rgba(255, 220, 130, 0.4);
}
.confirm-tag-limits {
  background: rgba(200, 200, 200, 0.15);
  color: #888;
  border: 1rpx solid rgba(200, 200, 200, 0.4);
}
.confirm-tag-empty {
  background: rgba(200, 200, 200, 0.1);
  color: #aaa;
  border: 1rpx solid rgba(200, 200, 200, 0.3);
}
.confirm-card-footer {
  color: #666;
  font-family: "PingFangSc-Regular", sans-serif;
  font-size: 24rpx;
  margin-bottom: 16rpx;
}
.confirm-card-btns {
  display: flex;
  flex-direction: row;
  gap: 16rpx;
  align-items: center;
}
.confirm-card-btn {
  display: inline-block;
  background: #85d2c7;
  color: #fff;
  border-radius: 60rpx;
  padding: 12rpx 32rpx;
  font-family: "PingFangSc-Medium", sans-serif;
  font-size: 26rpx;
  font-weight: 500;
}
.confirm-card-btn-alt {
  display: inline-block;
  background: transparent;
  color: #85d2c7;
  border: 2rpx solid #85d2c7;
  border-radius: 60rpx;
  padding: 10rpx 30rpx;
  font-family: "PingFangSc-Medium", sans-serif;
  font-size: 26rpx;
  font-weight: 500;
}

/* 首次偏好确认 */
.profile-setup {
  margin: 12rpx 0;
  padding: 16rpx;
  background: rgba(133, 210, 199, 0.05);
  border-radius: 12rpx;
}
.profile-setup-title {
  color: #666;
  font-size: 22rpx;
  margin-bottom: 12rpx;
}
.profile-setup-row {
  margin-bottom: 10rpx;
}
.profile-setup-label {
  color: #999;
  font-size: 20rpx;
  margin-bottom: 4rpx;
}
.profile-setup-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8rpx;
}
.profile-tag {
  border: 1rpx solid #ccc;
  border-radius: 30rpx;
  padding: 4rpx 14rpx;
  color: #999;
  font-size: 20rpx;
}
.profile-tag-sel {
  border-color: #85d2c7;
  color: #85d2c7;
  background: rgba(133, 210, 199, 0.08);
}
.profile-setup-btns {
  display: flex;
  flex-direction: row;
  gap: 16rpx;
  margin-top: 12rpx;
}
.profile-setup-btn-save {
  background: #85d2c7;
  color: #fff;
  border-radius: 40rpx;
  padding: 8rpx 24rpx;
  font-size: 22rpx;
}
.profile-setup-btn-skip {
  color: #999;
  border: 1rpx solid #ccc;
  border-radius: 40rpx;
  padding: 8rpx 24rpx;
  font-size: 22rpx;
}
.profile-actions {
  display: flex;
  gap: 12rpx;
  margin-top: 6rpx;
}
.profile-action-edit {
  color: #85d2c7;
  font-size: 22rpx;
  padding: 4rpx 0;
}
.profile-action-reset {
  color: #ccc;
  font-size: 20rpx;
  padding: 4rpx 0;
}

/* 已确认长期偏好展示 */
.profile-display {
  margin: 12rpx 0 0 0;
}
.profile-display-label {
  color: #999;
  font-size: 20rpx;
  margin-bottom: 4rpx;
}
.profile-display-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8rpx;
}

/* ===== 底部输入区 ===== */
.input-area {
  position: absolute;
  left: 0;
  top: 1446rpx;
  width: 750rpx;
  height: 72rpx;
  z-index: 10;
}

/* 真实输入框 */
.input-real {
  background: rgba(133, 210, 199, 0.1);
  border-radius: 60rpx;
  border: 2rpx solid #85d2c7;
  width: 400rpx;
  height: 72rpx;
  position: absolute;
  left: 24rpx;
  top: 0;
  padding-left: 28rpx;
  padding-right: 16rpx;
  box-sizing: border-box;
  color: #333;
  font-family: "PingFangSc-Regular", sans-serif;
  font-size: 28rpx;
  z-index: 5;
}

/* 发送文字按钮 */
.btn-send {
  position: absolute;
  left: 434rpx;
  top: 0;
  width: 64rpx;
  height: 72rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #85d2c7;
  font-family: "PingFangSc-Medium", sans-serif;
  font-size: 24rpx;
  z-index: 15;
}

/* 相机图标 */
.ico-camera {
  width: 44rpx;
  height: 44rpx;
  position: absolute;
  left: 508rpx;
  top: 14rpx;
  z-index: 15;
}

/* 语音图标 */
.ico-voice {
  width: 44rpx;
  height: 44rpx;
  position: absolute;
  left: 560rpx;
  top: 14rpx;
  z-index: 15;
}
.ico-voice-recording {
  opacity: 0.5;
  transform: scale(1.15);
}

/* 绿色按钮（进入推荐） */
.mic-circle {
  background: #85d2c7;
  border-radius: 50%;
  width: 72rpx;
  height: 72rpx;
  position: absolute;
  left: 640rpx;
  top: 0;
  z-index: 15;
  display: flex;
  align-items: center;
  justify-content: center;
}
.mic-label {
  color: #fff;
  font-family: "PingFangSc-Medium", sans-serif;
  font-size: 20rpx;
}

/* 面板状态 */
.guess-status-text {
  color: #85d2c7;
  font-size: 20rpx;
  margin-left: 12rpx;
}

/* 按钮禁用态 */
.btn-disabled {
  opacity: 0.4;
  pointer-events: none;
}
</style>
