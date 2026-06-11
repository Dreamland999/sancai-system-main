<template>
  <view class="frame-394">
    <!-- 顶部白色底色 -->
    <view class="top-bar"></view>

    <!-- 假状态栏已移除（真机系统自带） -->

    <!-- 假底部 Home Indicator 已移除（真机系统自带） -->

    <!-- 返回箭头 -->
    <view class="back-hit" @tap="onBack">
      <image class="ico-back" src="/static/figma-frame394/right0.svg" mode="aspectFit" />
    </view>
    <!-- 标题 -->
    <view class="txt-title">状态显化</view>
    <!-- 历史 -->
    <view class="txt-history" @tap="onHistory">历史</view>

    <!-- ===== 三个主题图标 ===== -->
    <!-- 形 — 绿色 — 身体状态 -->
    <view
      class="state-item state-item-l1"
      :class="{ 'state-active': selectedCategory === 'body' }"
      @tap="onTapCategory('body')"
    >
      <view class="state-glow state-glow-green"></view>
      <view class="state-ring state-ring-green"></view>
      <image class="state-icon state-icon-1" src="/static/figma-frame394/group-13620.svg" mode="aspectFit" />
      <view class="state-label" :class="{ 'state-label-active': selectedCategory === 'body' }">形</view>
    </view>

    <!-- 心 — 粉色 — 情绪心境 -->
    <view
      class="state-item state-item-l2"
      :class="{ 'state-active': selectedCategory === 'mood' }"
      @tap="onTapCategory('mood')"
    >
      <view class="state-glow state-glow-pink"></view>
      <view class="state-ring state-ring-pink"></view>
      <image class="state-icon state-icon-2" src="/static/figma-frame394/group-13621.svg" mode="aspectFit" />
      <view class="state-label" :class="{ 'state-label-active': selectedCategory === 'mood' }">心</view>
    </view>

    <!-- 境 — 橙色 — 外部环境 -->
    <view
      class="state-item state-item-l3"
      :class="{ 'state-active': selectedCategory === 'scene' }"
      @tap="onTapCategory('scene')"
    >
      <view class="state-glow state-glow-orange"></view>
      <view class="state-ring state-ring-orange"></view>
      <image class="state-icon state-icon-3" src="/static/figma-frame394/group-13622.svg" mode="aspectFit" />
      <view class="state-label" :class="{ 'state-label-active': selectedCategory === 'scene' }">境</view>
    </view>

    <!-- 分类标签卡片 -->
    <view v-if="selectedCategory && currentCategoryCfg" class="body-card">
      <image class="card-bg" src="/static/figma-frame394/union0.svg" mode="aspectFit" />
      <view class="card-close" @tap="closeCard">收起 ▴</view>
      <view class="card-title">{{ currentCategoryCfg.label }}</view>
      <view class="card-tags">
        <view
          v-for="tag in currentCategoryCfg.tags"
          :key="tag"
          class="card-tag"
          :class="{ 'tag-selected': selectedByField[selectedCategory].indexOf(tag) !== -1 }"
          @tap="onToggleTag(tag)"
        >{{ tag }}</view>
      </view>
    </view>

    <!-- 下一步按钮 -->
    <view
      class="btn-next"
      :class="{ 'btn-next-active': hasAnySelection }"
      @tap="onNext"
    >
      <view class="btn-next-bg"></view>
      <view class="btn-next-text">下一步</view>
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
      }
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
  methods: {
    onBack() {
      goBack();
    },
    onHistory() {
      uni.showToast({ title: "历史", icon: "none" });
    },
    onTapCategory(category) {
      this.selectedCategory = category;
    },
    closeCard() {
      this.selectedCategory = null;
    },
    onToggleTag(tag) {
      if (!this.selectedCategory) return;
      this.touchedFields[this.selectedCategory] = true;
      const arr = this.selectedByField[this.selectedCategory];
      const idx = arr.indexOf(tag);

      // scene: 单选
      if (this.selectedCategory === 'scene') {
        this.selectedByField.scene = [tag];
        return;
      }

      if (idx === -1) {
        // body: "良好" 清掉其他不适
        if (this.selectedCategory === 'body' && tag === '良好') {
          this.selectedByField.body = ['良好'];
          return;
        }
        // body: 选不适标签时清除"良好"
        if (this.selectedCategory === 'body') {
          const gIdx = arr.indexOf('良好');
          if (gIdx !== -1) arr.splice(gIdx, 1);
        }
        // body: 饥饿/饱腹 互斥
        if (tag === '饥饿' && arr.indexOf('饱腹') !== -1) arr.splice(arr.indexOf('饱腹'), 1);
        if (tag === '饱腹' && arr.indexOf('饥饿') !== -1) arr.splice(arr.indexOf('饥饿'), 1);
        // body: 感觉冷/热 互斥
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
    }
  }
};
</script>

<style scoped>
.frame-394 {
  width: 750rpx;
  height: 100vh;
  background: #ffffff;
  position: relative;
  overflow: hidden;
}

.top-bar {
  background: #ffffff;
  width: 750rpx;
  height: 176rpx;
  position: absolute;
  left: 0;
  top: 0;
}

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

.back-hit {
  position: absolute;
  left: 24rpx;
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

.txt-title {
  color: #333333;
  text-align: center;
  font-family: "PingFangSc-Medium", sans-serif;
  font-size: 32rpx;
  font-weight: 500;
  position: absolute;
  left: 308rpx;
  top: 108rpx;
}

.txt-history {
  color: #333333;
  text-align: left;
  font-family: "PingFangSc-Medium", sans-serif;
  font-size: 32rpx;
  font-weight: 500;
  position: absolute;
  left: 646rpx;
  top: 108rpx;
}

/* ===== 状态图标共用 ===== */
.state-item {
  position: absolute;
  z-index: 5;
}
.state-glow {
  border-radius: 50%;
  width: 156rpx;
  height: 156rpx;
  position: absolute;
  left: 0;
  top: 0;
}
.state-ring {
  border-radius: 50%;
  width: 60rpx;
  height: 60rpx;
  position: absolute;
  left: 46rpx;
  top: 54rpx;
  filter: blur(10rpx);
}
.state-icon {
  position: absolute;
}
.state-icon-1 {
  width: 72rpx;
  height: 54rpx;
  left: 42rpx;
  top: 48rpx;
}
.state-icon-2 {
  width: 72rpx;
  height: 68rpx;
  left: 42rpx;
  top: 42rpx;
}
.state-icon-3 {
  width: 78rpx;
  height: 78rpx;
  left: 40rpx;
  top: 37rpx;
}
.state-label {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  bottom: -32rpx;
  color: #999;
  font-family: "ZCOOL XiaoWei", "Songti SC", serif;
  font-size: 22rpx;
  white-space: nowrap;
}
.state-label-active {
  color: #333;
}
.state-active .state-icon-1,
.state-active .state-icon-2,
.state-active .state-icon-3 {
  transform: scale(1.1);
}

/* 绿色 — 形（身体状态） */
.state-item-l1 { left: 100rpx; top: 1120rpx; }
.state-glow-green {
  background: #f1fff2;
  box-shadow: 0px 8rpx 15rpx 0px rgba(133, 210, 199, 0.2);
  filter: blur(2rpx);
}
.state-ring-green { border: 16rpx solid rgba(119, 227, 212, 0.6); }

/* 粉色 — 心（情绪心境） */
.state-item-l2 { left: 308rpx; top: 1120rpx; }
.state-glow-pink {
  background: #fff1f4;
  box-shadow: 0px 8rpx 15rpx 0px rgba(133, 210, 199, 0.2);
  filter: blur(2rpx);
}
.state-ring-pink { border: 16rpx solid rgba(255, 158, 190, 0.6); }

/* 橙色 — 境（外部环境） */
.state-item-l3 { left: 516rpx; top: 1120rpx; }
.state-glow-orange {
  background: #fff5f1;
  box-shadow: 0px 8rpx 15rpx 0px rgba(133, 210, 199, 0.2);
  filter: blur(2rpx);
}
.state-ring-orange { border: 16rpx solid rgba(255, 165, 165, 0.6); }

/* ===== 分类标签卡片 ===== */
.body-card {
  position: absolute;
  left: 34rpx;
  top: 760rpx;
  width: 682rpx;
  height: 290rpx;
  z-index: 2;
}
.card-bg {
  position: absolute;
  left: 0;
  top: 0;
  width: 682rpx;
  height: 100%;
}
.card-close {
  position: absolute;
  right: 24rpx;
  top: 12rpx;
  color: #85d2c7;
  font-family: "PingFangSc-Regular", sans-serif;
  font-size: 24rpx;
  z-index: 3;
  padding: 8rpx 16rpx;
}
.card-title {
  color: #333333;
  font-family: "ZcoolXiaoWei-Regular", sans-serif;
  font-size: 32rpx;
  font-weight: 400;
  position: absolute;
  left: 40rpx;
  top: 44rpx;
}
.card-tags {
  position: absolute;
  left: 40rpx;
  top: 100rpx;
  right: 40rpx;
  display: flex;
  flex-wrap: wrap;
  gap: 16rpx 20rpx;
}
.card-tag {
  background: rgba(255, 255, 255, 0.85);
  border: 2rpx solid transparent;
  border-radius: 50rpx;
  padding: 8rpx 20rpx;
  color: #666666;
  font-family: "PingFangSc-Regular", sans-serif;
  font-size: 24rpx;
  font-weight: 400;
  white-space: nowrap;
}
.tag-selected {
  border-color: #85d2c7;
  color: #333333;
  background: rgba(133, 210, 199, 0.12);
}

/* ===== 下一步按钮 ===== */
.btn-next {
  position: absolute;
  left: 156rpx;
  top: 1412rpx;
  width: 440rpx;
  height: 80rpx;
}
.btn-next-bg {
  background: #cccccc;
  border-radius: 60rpx;
  border: 2rpx solid #ffffff;
  width: 440rpx;
  height: 80rpx;
  position: absolute;
  left: 0;
  top: 0;
}
.btn-next-text {
  color: #ffffff;
  text-align: center;
  font-family: "PingFangSc-Medium", sans-serif;
  font-size: 32rpx;
  font-weight: 500;
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 440rpx;
}
.btn-next-active .btn-next-bg {
  background: #56bfb0;
}
</style>
