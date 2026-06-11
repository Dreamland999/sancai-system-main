<template>
  <view class="frame-389">
    <!-- 顶部白色底色 -->
    <view class="top-bar"></view>

    <!-- 假状态栏已移除（真机系统自带） -->

    <!-- 假底部 Home Indicator 已移除（真机系统自带） -->

    <!-- 返回箭头 + 热区 -->
    <view class="back-hit" @tap="onBack">
      <image class="ico-back" src="/static/figma-frame389/right0.svg" mode="aspectFit" />
    </view>
    <!-- 标题 -->
    <view class="txt-title">配方选择</view>

    <!-- 顶部水果装饰图 -->
    <image
      class="img-fruit"
      src="/static/figma-frame389/_20260602215955-767-157-10.png"
      mode="aspectFill"
    />

    <!-- 中下部彩色装饰带（group-13930.svg 为空文件，用 CSS 替代） -->
    <view class="deco-band"></view>

    <!-- 配方标题 -->
    <view class="txt-recipe">{{ recipe.name }}</view>

    <!-- 推荐理由 -->
    <view class="section-title section-title-1">推荐理由</view>
    <view class="section-body section-body-1">
      <text>{{ recipe.match_reason }}</text>
    </view>

    <!-- 配方功效 -->
    <view class="section-title section-title-2">配方功效</view>
    <view class="section-body section-body-2">
      <text>{{ recipeDescription }}</text>
    </view>

    <!-- 甜度 / 温度 -->
    <view class="section-title section-title-3">甜度 / 温度</view>
    <view class="section-body section-body-3">
      <text>{{ recipe.sweetness }} / {{ recipe.temperature }}</text>
      <text>推荐指数：{{ recipe.score }}</text>
    </view>

    <!-- 底部莲花按钮 -->
    <view class="lotus-btn" @tap="onLotus">
      <view class="lotus-white"></view>
      <view class="lotus-glow"></view>
      <image
        class="lotus-icon"
        src="/static/figma-frame389/b-8-b-9-a-543-d-10-f-48-fafb-88-aa-0-fb-39-d-4987-10.png"
        mode="aspectFill"
      />
    </view>
  </view>
</template>

<script>
import { sendFeedback } from '@/api/feedback.js';

const FRAME399 = '/pages/figma-frame399-preview/figma-frame399-preview';

function fallbackRecipe() {
  return {
    name: '桃气西瓜冰沙',
    match_reason: '西瓜清热解暑，茉莉花茶安神宁心',
    description: '清热解暑，平复烦躁',
    polished_text: '清热解暑，平复烦躁，补水消肿，唤醒活力',
    sweetness: '半糖',
    temperature: '冰',
    score: 0.92,
  };
}

export default {
  name: "FigmaFrame389Preview",
  data() {
    return {
      recipe: fallbackRecipe(),
    };
  },
  computed: {
    recipeDescription() {
      return this.recipe.description || this.recipe.polished_text || '';
    },
  },
  mounted() {
    try {
      const result = uni.getStorageSync('recommend_result');
      const top = result?.recommendations?.[0];
      if (top) {
        this.recipe = {
          recipe_id: top.recipe_id || '',
          name: top.name || fallbackRecipe().name,
          type: top.type || '',
          match_reason: top.match_reason || fallbackRecipe().match_reason,
          description: top.description || top.polished_text || fallbackRecipe().description,
          polished_text: top.polished_text || '',
          sweetness: top.sweetness || fallbackRecipe().sweetness,
          temperature: top.temperature || fallbackRecipe().temperature,
          score: top.score ?? fallbackRecipe().score,
          health_notes: top.health_notes || [],
          visual_mapping: top.visual_mapping || [],
        };
        uni.setStorageSync('current_recipe', this.recipe);
        console.log('[Frame389] loaded recommend_result, recipe:', this.recipe.name);
        console.log('[Frame389] score:', top.score, 'visual_prompt:', top.visual_prompt);
      }
    } catch (e) {
      console.log('[Frame389] no recommend_result, using fallback');
    }
    sendFeedback('view_recommendation');
  },
  methods: {
    onBack() {
      console.log('[Frame389] back -> Frame399');
      uni.redirectTo({
        url: FRAME399,
        fail(err) { console.error('[Frame389] back to Frame399 failed', err); }
      });
    },
    onLotus() {
      sendFeedback('click_adjust');
      uni.redirectTo({ url: '/pages/figma-frame391-preview/figma-frame391-preview' });
    },
  },
};
</script>

<style scoped>
.frame-389 {
  width: 750rpx;
  height: 100vh;
  background: #ffffff;
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

/* Home Indicator */
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
  left: 20rpx;
  top: 86rpx;
  width: 80rpx;
  height: 80rpx;
  z-index: 5;
  display: flex;
  align-items: center;
  justify-content: center;
}
.ico-back {
  width: 48rpx;
  height: 48rpx;
}

/* 标题 */
.txt-title {
  color: #333333;
  text-align: center;
  font-family: "PingFangSc-Medium", sans-serif;
  font-size: 32rpx;
  font-weight: 500;
  position: absolute;
  left: 312rpx;
  top: 108rpx;
}

/* 顶部水果装饰图 */
.img-fruit {
  width: 762rpx;
  height: 858rpx;
  position: absolute;
  left: -12rpx;
  top: -4rpx;
  z-index: 2;
  pointer-events: none;
}

/* 中下部彩色装饰带（替代空 SVG） */
.deco-band {
  position: absolute;
  left: -10rpx;
  top: 760rpx;
  width: 760rpx;
  height: 200rpx;
  background: linear-gradient(90deg,
    rgba(133, 210, 199, 0.15) 0%,
    rgba(255, 158, 190, 0.1) 50%,
    rgba(255, 165, 165, 0.15) 100%
  );
  border-radius: 0;
  opacity: 0.6;
  pointer-events: none;
}

/* 配方标题 */
.txt-recipe {
  color: #000000;
  text-align: right;
  font-family: "PingFangSc-Heavy", sans-serif;
  font-size: 32rpx;
  font-weight: 400;
  position: absolute;
  left: 274rpx;
  top: 832rpx;
}

/* 段落小标题 */
.section-title {
  color: #333333;
  font-family: "PingFangSc-Medium", sans-serif;
  font-size: 28rpx;
  font-weight: 500;
  position: absolute;
  left: 76rpx;
}
.section-title-1 { top: 902rpx; }
.section-title-2 { top: 1086rpx; }
.section-title-3 { top: 1232rpx; }

/* 段落正文 */
.section-body {
  color: #666666;
  font-family: "PingFangSc-Regular", sans-serif;
  font-size: 26rpx;
  font-weight: 400;
  line-height: 40rpx;
  position: absolute;
  left: 92rpx;
  width: 544rpx;
}
.section-body text {
  display: block;
}
.section-body-1 { top: 946rpx; }
.section-body-2 { top: 1130rpx; }
.section-body-3 { top: 1276rpx; }

/* 底部莲花按钮 */
.lotus-btn {
  position: absolute;
  left: 268rpx;
  top: 1370rpx;
  width: 192rpx;
  height: 192rpx;
}
.lotus-white {
  background: #ffffff;
  border-radius: 50%;
  width: 192rpx;
  height: 192rpx;
  position: absolute;
  left: 0;
  top: 0;
}
.lotus-glow {
  background: rgba(122, 233, 217, 0.8);
  border-radius: 50%;
  width: 144rpx;
  height: 144rpx;
  position: absolute;
  left: 24rpx;
  top: 24rpx;
  filter: blur(30rpx);
}
.lotus-icon {
  width: 112rpx;
  height: 112rpx;
  position: absolute;
  left: 40rpx;
  top: 40rpx;
  border-radius: 50%;
}
</style>
