<template>
  <view class="page" :style="{ paddingTop: statusBarHeight + 'px' }">
    <!-- ===== 顶部导航栏 ===== -->
    <view class="nav-bar">
      <view class="nav-back" @tap="onBack">
        <image class="nav-back-icon" src="/static/figma-frame394-new/back-arrow.png" mode="aspectFit" />
      </view>
      <text class="nav-title">状态显化</text>
      <text class="nav-history" @tap="onHistory">历史</text>
    </view>

    <!-- ===== 中间可滚动内容 ===== -->
    <scroll-view
      class="content-scroll"
      scroll-y="true"
      :style="{ height: scrollHeight + 'px' }"
      :show-scrollbar="false"
      :enhanced="true"
    >
      <!-- 主标题区 -->
      <view class="title-section">
        <view class="main-title-row">
          <view class="hero-title-wrap">
            <text class="main-title">选择此刻的状态</text>
            <image class="title-leaf" src="/static/figma-frame394-new/decor-leaf.png" mode="aspectFit" />
          </view>
        </view>
        <view class="subtitle-row">
          <text class="subtitle-text">观照当下，三才调和，食养身心</text>
        </view>
      </view>

      <!-- ===== 三才卡片：形 · 躯体状态 ===== -->
      <view
        class="sancai-card"
        :class="{ 'card-active': selectedCategory === 'body' }"
        @tap="onTapCategory('body')"
      >
        <view class="card-bg card-bg-body">
          <!-- 左侧图标 -->
          <image class="card-badge-img" src="/static/figma-frame394-new/sancai-body-symbol.png" mode="aspectFit" />
          <!-- 中间信息区 -->
          <view class="card-info">
            <text class="card-label">形·躯体状态</text>
            <text class="card-desc-1">身体的感受与能量</text>
            <text class="card-desc-2">气血、脏腑、体能状态</text>
            <view v-if="selectedByField.body.length > 0" class="card-tags-preview">
              <text v-for="t in selectedByField.body" :key="t" class="card-tag-chip">{{ t }}</text>
            </view>
          </view>
          <!-- 右侧装饰图 -->
          <image class="card-illust" src="/static/figma-frame394-new/card-body-illustration.png" mode="aspectFit" />
          <!-- 展开提示 -->
          <image class="card-expand-arrow" :class="{ 'card-expand-arrow-open': selectedCategory === 'body' }" src="/static/figma-frame394-new/card-body-arrow.png" mode="aspectFit" />
        </view>
      </view>

      <!-- ===== 三才卡片：心 · 情志状态 ===== -->
      <view
        class="sancai-card"
        :class="{ 'card-active': selectedCategory === 'mood' }"
        @tap="onTapCategory('mood')"
      >
        <view class="card-bg card-bg-mood">
          <!-- 左侧图标 -->
          <image class="card-badge-img" src="/static/figma-frame394-new/sancai-mood-symbol.png" mode="aspectFit" />
          <view class="card-info">
            <text class="card-label">心·情志状态</text>
            <text class="card-desc-1">情绪与心理的感受</text>
            <text class="card-desc-2">喜怒、思虑、情绪状态</text>
            <view v-if="selectedByField.mood.length > 0" class="card-tags-preview">
              <text v-for="t in selectedByField.mood" :key="t" class="card-tag-chip">{{ t }}</text>
            </view>
          </view>
          <image class="card-illust" src="/static/figma-frame394-new/card-mood-illustration.png" mode="aspectFit" />
          <image class="card-expand-arrow" :class="{ 'card-expand-arrow-open': selectedCategory === 'mood' }" src="/static/figma-frame394-new/card-mood-arrow.png" mode="aspectFit" />
        </view>
      </view>

      <!-- ===== 三才卡片：境 · 环境状态 ===== -->
      <view
        class="sancai-card"
        :class="{ 'card-active': selectedCategory === 'scene' }"
        @tap="onTapCategory('scene')"
      >
        <view class="card-bg card-bg-scene">
          <!-- 左侧图标 -->
          <image class="card-badge-img" src="/static/figma-frame394-new/sancai-scene-symbol.png" mode="aspectFit" />
          <view class="card-info">
            <text class="card-label">境·环境状态</text>
            <text class="card-desc-1">所处环境的影响</text>
            <text class="card-desc-2">季节、气候、生活环境</text>
            <view v-if="selectedByField.scene.length > 0" class="card-tags-preview">
              <text v-for="t in selectedByField.scene" :key="t" class="card-tag-chip">{{ t }}</text>
            </view>
          </view>
          <image class="card-illust" src="/static/figma-frame394-new/card-scene-illustration.png" mode="aspectFit" />
          <image class="card-expand-arrow" :class="{ 'card-expand-arrow-open': selectedCategory === 'scene' }" src="/static/figma-frame394-new/card-scene-arrow.png" mode="aspectFit" />
        </view>
      </view>

      <!-- ===== 标签选择面板 ===== -->
      <view v-if="selectedCategory && currentCategoryCfg" class="tag-panel">
        <view class="tag-panel-head">
          <text class="tag-panel-title">{{ currentCategoryCfg.label }}</text>
          <view class="tag-panel-collapse" @tap.stop="closeCard">
            <image class="collapse-ico" src="/static/figma-frame394-new/icon-collapse.png" mode="aspectFit" />
            <text class="collapse-txt">收起</text>
          </view>
        </view>
        <view class="tag-panel-grid">
          <view
            v-for="tag in currentCategoryCfg.tags"
            :key="tag"
            class="tag-btn"
            :class="{ 'tag-btn-on': selectedByField[selectedCategory].indexOf(tag) !== -1 }"
            @tap.stop="onToggleTag(tag)"
          >
            <image
              v-if="getTagIcon(tag)"
              class="tag-btn-icon"
              :src="getTagIcon(tag)"
              mode="aspectFit"
            />
            <text class="tag-btn-text">{{ tag }}</text>
          </view>
        </view>
      </view>

      <!-- 三才状态 / 了解三才 —— 始终显示 -->
      <view class="sancai-link">
        <image class="sancai-link-icon" src="/static/figma-frame394-new/icon-sancai.png" mode="aspectFit" />
        <text class="sancai-link-label">三才状态</text>
        <text class="sancai-link-text">了解三才</text>
      </view>

      <view class="bottom-spacer"></view>
    </scroll-view>

    <!-- ===== 底部固定区 ===== -->
    <view class="bottom-bar" :style="{ paddingBottom: bottomBarPadding + 'px' }">
      <view class="footer-tip">
        <image class="footer-tip-icon" src="/static/figma-frame394-new/decor-leaf.png" mode="aspectFit" />
        <text class="footer-tip-text">从内观照，由食养调，回归平衡</text>
      </view>
      <view
        class="btn-next"
        :class="{ 'btn-next-active': hasAnySelection }"
        @tap="onNext"
      >
        <text class="btn-next-text">下一步</text>
      </view>
    </view>
  </view>
</template>

<script>
import { goBack } from '@/utils/nav.js';

const CATEGORY_OPTIONS = {
  body: {
    label: '身体状态',
    tags: ['良好', '饥饿', '饱腹', '口渴', '疲劳', '感觉有点冷', '感觉有点热', '困倦']
  },
  mood: {
    label: '情绪心境',
    tags: ['开心', '平静', '兴奋', '低落', '烦躁', '紧张', '无聊', '孤单']
  },
  scene: {
    label: '所处环境',
    tags: ['家/宿舍', '学校/教学楼', '图书馆/自习室', '办公室/公司', '餐厅/食堂', '健身房/运动场', '咖啡店/奶茶店', '商场/商业街', '地铁/公交/车站', '公园/户外']
  }
};

const DEFAULT_INPUT = {
  scene: [],
  body: [],
  mood: [],
  needs: [],
  limits: [],
  flavor_preference: [],
  temperature_preference: []
};
const EDITABLE_FIELDS = ['body', 'mood', 'scene'];

const MOOD_ICON_MAP = {
  '开心': '/static/figma-frame394-new/mood-kaixin.png',
  '平静': '/static/figma-frame394-new/mood-pingjing.png',
  '兴奋': '/static/figma-frame394-new/mood-xingfen.png',
  '低落': '/static/figma-frame394-new/mood-diluo.png',
  '烦躁': '/static/figma-frame394-new/mood-fanzao.png',
  '紧张': '/static/figma-frame394-new/mood-jinzhang.png',
  '无聊': '/static/figma-frame394-new/mood-wuliao.png',
  '孤单': '/static/figma-frame394-new/mood-gudan.png'
};

function loadExistingInput() {
  try {
    const input = uni.getStorageSync('recommend_input');
    if (input && typeof input === 'object') return input;
  } catch (e) { /* ignore */ }
  return null;
}

export default {
  name: "FigmaFrame394Preview",
  data() {
    const existing = loadExistingInput();
    return {
      selectedCategory: null,
      existingInput: existing || DEFAULT_INPUT,
      selectedByField: {
        body: existing ? [...(existing.body || [])] : [],
        mood: existing ? [...(existing.mood || [])] : [],
        scene: existing ? [...(existing.scene || [])] : []
      },
      touchedFields: {
        body: false,
        mood: false,
        scene: false
      },
      statusBarHeight: 0,
      scrollHeight: 0,
      bottomSafe: 0,
      bottomBarPadding: 0
    };
  },
  computed: {
    currentCategoryCfg() {
      return this.selectedCategory ? CATEGORY_OPTIONS[this.selectedCategory] : null;
    },
    hasAnySelection() {
      const allFields = { ...this.existingInput, ...this.selectedByField };
      return EDITABLE_FIELDS.some(k => {
        const v = this.touchedFields[k] ? this.selectedByField[k] : allFields[k];
        return v && v.length > 0;
      });
    }
  },
  created() {
    this.calcLayout();
  },
  methods: {
    onBack() {
      goBack();
    },
    onHistory() {
      uni.showToast({ title: "历史", icon: "none" });
    },
    onTapCategory(category) {
      if (this.selectedCategory === category) {
        this.selectedCategory = null;
      } else {
        this.selectedCategory = category;
      }
    },
    closeCard() {
      this.selectedCategory = null;
    },
    onToggleTag(tag) {
      if (!this.selectedCategory) return;
      this.touchedFields[this.selectedCategory] = true;
      const arr = this.selectedByField[this.selectedCategory];
      const idx = arr.indexOf(tag);

      if (this.selectedCategory === 'scene') {
        this.selectedByField.scene = [tag];
        return;
      }

      if (idx === -1) {
        if (this.selectedCategory === 'body' && tag === '良好') {
          this.selectedByField.body = ['良好'];
          return;
        }
        if (this.selectedCategory === 'body') {
          const gIdx = arr.indexOf('良好');
          if (gIdx !== -1) arr.splice(gIdx, 1);
        }
        if (tag === '饥饿' && arr.indexOf('饱腹') !== -1) arr.splice(arr.indexOf('饱腹'), 1);
        if (tag === '饱腹' && arr.indexOf('饥饿') !== -1) arr.splice(arr.indexOf('饥饿'), 1);
        if (tag === '感觉有点冷' && arr.indexOf('感觉有点热') !== -1) arr.splice(arr.indexOf('感觉有点热'), 1);
        if (tag === '感觉有点热' && arr.indexOf('感觉有点冷') !== -1) arr.splice(arr.indexOf('感觉有点冷'), 1);

        arr.push(tag);
      } else {
        arr.splice(idx, 1);
      }
    },
    normalizeInput() {
      const merged = {};
      const allKeys = Object.keys(DEFAULT_INPUT);
      for (const k of allKeys) {
        if (EDITABLE_FIELDS.indexOf(k) !== -1 && this.touchedFields[k]) {
          merged[k] = [...this.selectedByField[k]];
        } else {
          merged[k] = EDITABLE_FIELDS.indexOf(k) !== -1
            ? [...(this.existingInput[k] || [])]
            : [...(this.existingInput[k] || DEFAULT_INPUT[k] || [])];
        }
      }
      return merged;
    },
    onNext() {
      if (!this.hasAnySelection) {
        uni.showToast({ title: "请先选择状态或偏好", icon: "none" });
        return;
      }
      const input = this.normalizeInput();
      uni.setStorageSync('recommend_input', input);
      console.log('[Frame394] recommend_input saved', JSON.stringify(input));
      uni.redirectTo({ url: '/pages/figma-frame399-preview/figma-frame399-preview' });
    },

    getTagIcon(tag) {
      return MOOD_ICON_MAP[tag] || null;
    },

    calcLayout() {
      const info = uni.getSystemInfoSync();
      const { statusBarHeight, windowHeight, screenHeight, safeArea, screenWidth } = info;
      const rpxRatio = screenWidth / 750;

      this.statusBarHeight = statusBarHeight || 0;

      // 底部安全区（Home Indicator）
      const safeBottom = (safeArea && typeof safeArea.bottom === 'number') ? safeArea.bottom : screenHeight;
      this.bottomSafe = Math.max(0, screenHeight - safeBottom);

      // 额外视觉间距（把按钮往上推，避免贴边）: 40rpx → px
      const extraMarginPx = 40 * rpxRatio;
      this.bottomBarPadding = this.bottomSafe + extraMarginPx;

      // 导航栏内容高度 88rpx → px
      const navPx = 88 * rpxRatio;
      // 底部区可见高度: padding-top(0) + footer-tip(56rpx) + button(88rpx) + extra(40rpx) = 184rpx → px
      const bottomBarVisiblePx = 184 * rpxRatio;

      // scroll-view 占满剩余空间
      this.scrollHeight = windowHeight - this.statusBarHeight - navPx - bottomBarVisiblePx;
    }
  }
};
</script>

<style scoped>
.page {
  width: 750rpx;
  height: 100vh;
  background: #fafafa;
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

/* ===== 导航栏 ===== */
.nav-bar {
  width: 750rpx;
  height: 88rpx;
  flex-shrink: 0;
  position: relative;
  display: flex;
  align-items: center;
}
.nav-back {
  position: absolute;
  left: 20rpx;
  top: 50%;
  transform: translateY(-50%);
  width: 60rpx;
  height: 60rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2;
}
.nav-back-icon {
  width: 22rpx;
  height: 38rpx;
}
.nav-title {
  position: absolute;
  left: 0;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  text-align: center;
  pointer-events: none;
  color: #666666;
  font-family: "PingFangSC-Regular", "Microsoft YaHei", sans-serif;
  font-size: 32rpx;
  font-weight: 400;
  white-space: nowrap;
}
.nav-history {
  position: absolute;
  right: 24rpx;
  top: 50%;
  transform: translateY(-50%);
  color: #666666;
  font-family: "PingFangSC-Regular", sans-serif;
  font-size: 26rpx;
  font-weight: 400;
  padding: 8rpx 12rpx;
}

/* ===== 可滚动内容 ===== */
.content-scroll {
  width: 750rpx;
}

/* ===== 主标题区 ===== */
.title-section {
  width: 750rpx;
  padding: 24rpx 56rpx 4rpx 56rpx;
  box-sizing: border-box;
}
.main-title-row {
  display: flex;
  justify-content: center;
}
.hero-title-wrap {
  position: relative;
  display: inline-block;
}
.main-title {
  display: block;
  text-align: center;
  color: #5c5c5c;
  font-family: -apple-system, "PingFangSC-Medium", "Microsoft YaHei", sans-serif;
  font-size: 40rpx;
  font-weight: 500;
  line-height: 56rpx;
}
.title-leaf {
  position: absolute;
  right: -34rpx;
  top: 2rpx;
  width: 28rpx;
  height: 28rpx;
}
.subtitle-row {
  display: flex;
  justify-content: center;
  margin-top: 6rpx;
}
.subtitle-text {
  text-align: center;
  color: #b2b2b2;
  font-family: -apple-system, "PingFangSC-Regular", "Microsoft YaHei", sans-serif;
  font-size: 24rpx;
  font-weight: 400;
  line-height: 34rpx;
}

/* ===== 三才卡片 ===== */
.sancai-card {
  width: 750rpx;
  padding: 12rpx 40rpx;
  box-sizing: border-box;
}
.card-bg {
  width: 670rpx;
  min-height: 170rpx;
  border-radius: 20rpx;
  position: relative;
  overflow: hidden;
  box-sizing: border-box;
  display: flex;
  flex-direction: row;
  align-items: center;
  padding: 24rpx 20rpx 24rpx 16rpx;
  transition: border-color 0.2s, box-shadow 0.2s;
}
/* 卡片底色 */
.card-bg-body {
  background: #f7f9f9;
  border: 2rpx solid #eaf4f3;
}
.card-bg-mood {
  background: #fdf6f6;
  border: 2rpx solid #f9eff0;
}
.card-bg-scene {
  background: #fdf8f4;
  border: 2rpx solid #faf3ee;
}
/* 展开态高亮 */
.card-active .card-bg {
  box-shadow: 0px 4rpx 20rpx 0px rgba(88, 187, 171, 0.12);
}
.card-active .card-bg-body {
  border-color: #b8e0d9;
}
.card-active .card-bg-mood {
  border-color: #f0ccd0;
}
.card-active .card-bg-scene {
  border-color: #f0dcd0;
}

/* ---- 左侧图标 ---- */
.card-badge-img {
  width: 96rpx;
  height: 96rpx;
  flex-shrink: 0;
  margin-right: 14rpx;
}

/* ---- 中间信息区 ---- */
.card-info {
  flex: 1;
  position: relative;
  z-index: 1;
  min-width: 0;
}
.card-label {
  display: block;
  color: #6d6b6b;
  font-family: -apple-system, "PingFangSC-Regular", "Microsoft YaHei", sans-serif;
  font-size: 28rpx;
  font-weight: 400;
  line-height: 38rpx;
}
.card-desc-1 {
  display: block;
  color: #b8b6b6;
  font-family: -apple-system, "PingFangSC-Regular", "Microsoft YaHei", sans-serif;
  font-size: 22rpx;
  font-weight: 400;
  line-height: 32rpx;
  margin-top: 4rpx;
}
.card-desc-2 {
  display: block;
  color: #b8b6b6;
  font-family: -apple-system, "PingFangSC-Regular", "Microsoft YaHei", sans-serif;
  font-size: 22rpx;
  font-weight: 400;
  line-height: 30rpx;
}

/* 已选标签预览 */
.card-tags-preview {
  position: relative;
  z-index: 1;
  display: flex;
  flex-wrap: wrap;
  gap: 8rpx;
  margin-top: 10rpx;
}
.card-tag-chip {
  background: rgba(255,255,255,0.8);
  border: 1rpx solid rgba(88, 187, 171, 0.35);
  border-radius: 20rpx;
  padding: 4rpx 16rpx;
  color: #555555;
  font-size: 20rpx;
  font-family: "PingFangSC-Regular", sans-serif;
  white-space: nowrap;
}

/* ---- 右侧装饰图 ---- */
.card-illust {
  position: absolute;
  right: 6rpx;
  bottom: 4rpx;
  width: 180rpx;
  height: 140rpx;
  object-fit: contain;
  pointer-events: none;
  z-index: 0;
  opacity: 0.85;
}

/* ---- 展开箭头 ---- */
.card-expand-arrow {
  position: absolute;
  right: 16rpx;
  top: 50%;
  transform: translateY(-50%) rotate(0deg);
  width: 36rpx;
  height: 36rpx;
  z-index: 1;
  transition: transform 0.25s;
}
.card-expand-arrow-open {
  transform: translateY(-50%) rotate(90deg);
}

/* ===== 标签选择面板 ===== */
.tag-panel {
  width: 750rpx;
  padding: 0 40rpx;
  box-sizing: border-box;
  margin-top: 18rpx;
}
.tag-panel-head {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  padding: 12rpx 0 16rpx 0;
}
.tag-panel-title {
  color: #555555;
  font-family: "PingFangSC-Medium", sans-serif;
  font-size: 28rpx;
  font-weight: 500;
}
.tag-panel-collapse {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 6rpx;
  padding: 8rpx 16rpx;
}
.collapse-ico {
  width: 26rpx;
  height: 16rpx;
}
.collapse-txt {
  color: #58bbab;
  font-family: "PingFangSC-Regular", sans-serif;
  font-size: 24rpx;
  font-weight: 400;
}

/* 标签网格 */
.tag-panel-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 16rpx 16rpx;
}
.tag-btn {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  gap: 8rpx;
  background: #ffffff;
  border: 1rpx solid #e0e0e0;
  border-radius: 18rpx;
  padding: 16rpx 24rpx;
  min-width: 140rpx;
  box-sizing: border-box;
}
.tag-btn-icon {
  width: 34rpx;
  height: 34rpx;
  flex-shrink: 0;
}
.tag-btn-text {
  color: #666666;
  font-family: "PingFangSC-Regular", sans-serif;
  font-size: 26rpx;
  font-weight: 400;
  white-space: nowrap;
}
/* 选中态 */
.tag-btn-on {
  background: #58bdad;
  border-color: #98d6ce;
}
.tag-btn-on .tag-btn-text {
  color: #ffffff;
}

/* ===== 了解三才 ===== */
.sancai-link {
  display: flex;
  flex-direction: row;
  align-items: center;
  padding: 24rpx 40rpx 0 40rpx;
  gap: 10rpx;
}
.sancai-link-icon {
  width: 24rpx;
  height: 24rpx;
  flex-shrink: 0;
}
.sancai-link-label {
  color: #666666;
  font-family: "PingFangSC-Regular", sans-serif;
  font-size: 26rpx;
  font-weight: 400;
}
.sancai-link-text {
  color: #999999;
  font-family: "PingFangSC-Regular", sans-serif;
  font-size: 22rpx;
  font-weight: 400;
}

/* ===== 底部文案 ===== */
.footer-tip {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  padding: 16rpx 40rpx 20rpx 40rpx;
}
.footer-tip-icon {
  width: 26rpx;
  height: 26rpx;
  flex-shrink: 0;
  margin-right: 10rpx;
}
.footer-tip-text {
  color: #c3c4c4;
  font-family: -apple-system, "PingFangSC-Regular", "Microsoft YaHei", sans-serif;
  font-size: 22rpx;
  font-weight: 400;
}

/* ===== 底部留白 ===== */
.bottom-spacer {
  height: 48rpx;
}

/* ===== 底部固定区 ===== */
.bottom-bar {
  width: 750rpx;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding-top: 0;
  background: #fafafa;
}
.btn-next {
  width: 620rpx;
  height: 88rpx;
  background: #cccccc;
  border-radius: 44rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}
.btn-next-active {
  background: #58bbab;
}
.btn-next-text {
  color: #ffffff;
  font-family: "PingFangSC-Medium", sans-serif;
  font-size: 32rpx;
  font-weight: 500;
}
</style>
