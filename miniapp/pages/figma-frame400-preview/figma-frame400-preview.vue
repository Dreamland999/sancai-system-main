<template>
  <view class="home-new">
    <!-- 雨景背景 -->
    <image class="home-bg" src="/static/figma-frame400-new/bg-rain.jpg" mode="scaleToFill" />

    <!-- 顶部定位 -->
    <view class="top-location">
      <image class="icon-location" src="/static/figma-frame400-new/icon-location.png" mode="aspectFit" />
      <text class="location-text">华南理工大学…</text>
      <image class="icon-chevron" src="/static/figma-frame400-new/icon-chevron.png" mode="aspectFit" />
    </view>

    <!-- 顶部天气 -->
    <view class="top-weather">
      <text class="weather-text">中雨</text>
      <image class="icon-weather" src="/static/figma-frame400-new/icon-weather-rain.png" mode="aspectFit" />
    </view>

    <!-- 诗句 -->
    <view class="poem-area">
      <text class="poem poem-1">松&#10;间&#10;沙&#10;路&#10;净&#10;无&#10;泥</text>
      <text class="poem poem-2">山&#10;下&#10;兰&#10;芽&#10;短&#10;浸&#10;溪</text>
      <text class="poem poem-3">潇&#10;潇&#10;暮&#10;雨&#10;子&#10;规&#10;啼</text>
      <image class="poem-seal" src="/static/figma-frame400-new/poem-seal.png" mode="aspectFit" />
    </view>

    <!-- 推荐卡片 -->
    <view class="rec-card" @tap="onTapDetail">
      <image class="rec-card-img" src="/static/figma-frame400-new/card-visual.png" mode="scaleToFill" />
      <view class="rec-text-layer">
        <image class="rec-lotus" src="/static/figma-frame400-new/card-decor-lotus.png" mode="aspectFit" />
        <text class="rec-tip">中雨微凉，宜温润清养</text>
        <text class="rec-label">今日推荐：</text>
        <text class="rec-name">茉莉七抹乌昔</text>
        <view class="rec-detail-btn">
          <text class="rec-detail-txt">查看详情</text>
          <image class="ico-arrow-sm" src="/static/figma-frame400-new/icon-arrow-sm.png" mode="aspectFit" />
        </view>
      </view>
    </view>

    <!-- 底部入口：食材库 -->
    <view class="entry-food" @tap="onTapFoodLib">
      <image class="entry-icon-food" src="/static/figma-frame400-new/icon-food.png" mode="aspectFit" />
      <text class="entry-label food-label">食材库</text>
    </view>

    <!-- 底部入口：制作 -->
    <view class="entry-make" @tap="onTapMake">
      <image class="entry-icon-make" src="/static/figma-frame400-new/icon-make.png" mode="aspectFit" />
      <text class="entry-label make-label">制作</text>
    </view>

    <!-- 底部入口：配方库 -->
    <view class="entry-recipe" @tap="onTapRecipeLib">
      <image class="entry-icon-recipe" src="/static/figma-frame400-new/icon-recipe.png" mode="aspectFit" />
      <text class="entry-label recipe-label">配方库</text>
    </view>
  </view>
</template>

<script>
import { safeNavigateTo } from '@/utils/nav.js';
import { resetRecommendSession } from '@/utils/session.js';

export default {
  name: "FigmaHomePreview",
  methods: {
    onTapDetail() {
      uni.showToast({ title: '详情待接入', icon: 'none' });
    },
    onTapFoodLib() {
      console.log('[Frame400] click 食材库');
      safeNavigateTo('/pages/figma-frame384-preview/figma-frame384-preview');
    },
    onTapMake() {
      console.log('[Frame400] click 制作');
      resetRecommendSession();
      safeNavigateTo('/pages/figma-frame396-preview/figma-frame396-preview');
    },
    onTapRecipeLib() {
      console.log('[Frame400] click 配方库');
      uni.showToast({ title: '配方库待补', icon: 'none' });
    },
  },
};
</script>

<style scoped>
.home-new {
  width: 750rpx;
  height: 100vh;
  position: relative;
  overflow: hidden;
  background: #dcefeb;
}

/* ===== 雨景背景 ===== */
.home-bg {
  position: absolute;
  left: 0;
  top: 0;
  width: 750rpx;
  height: 1586rpx;
  z-index: 0;
}

/* ===== 顶部定位 ===== */
.top-location {
  position: absolute;
  left: 35rpx;
  top: 110rpx;
  height: 46rpx;
  z-index: 2;
  display: flex;
  align-items: center;
}
.icon-location {
  width: 34rpx;
  height: 42rpx;
}
.location-text {
  margin-left: 18rpx;
  font-size: 26rpx;
  color: #3f6b6a;
}
.icon-chevron {
  margin-left: 16rpx;
  width: 12rpx;
  height: 22rpx;
}

/* ===== 顶部天气 ===== */
.top-weather {
  position: absolute;
  left: 520rpx;
  top: 112rpx;
  height: 46rpx;
  z-index: 2;
  display: flex;
  align-items: center;
}
.weather-text {
  font-size: 26rpx;
  color: #427271;
}
.icon-weather {
  margin-left: 14rpx;
  width: 34rpx;
  height: 34rpx;
}

/* ===== 诗句 ===== */
.poem-area {
  position: absolute;
  left: 590rpx;
  top: 245rpx;
  width: 130rpx;
  height: 650rpx;
  z-index: 2;
}
.poem {
  position: absolute;
  width: 44rpx;
  text-align: center;
  white-space: pre-line;
  font-family: "Songti SC", "STSong", "SimSun", "PingFang SC", serif;
  font-size: 36rpx;
  line-height: 48rpx;
  color: #2f6f6a;
  font-weight: 500;
}
.poem-1 {
  right: 0;
  top: -50rpx;
}
.poem-2 {
  right: 58rpx;
  top: -50rpx;
}
.poem-3 {
  right: 0;
  top: 300rpx;
}
.poem-seal {
  position: absolute;
  right: 4rpx;
  top: 628rpx;
  width: 32rpx;
  height: 38rpx;
}

/* ===== 推荐卡片 ===== */
.rec-card {
  position: absolute;
  left: 54rpx;
  top: 965rpx;
  width: 643rpx;
  height: 327rpx;
  z-index: 3;
}
.rec-card-img {
  position: absolute;
  left: 0;
  top: 0;
  width: 643rpx;
  height: 327rpx;
  z-index: 0;
}
.rec-text-layer {
  position: absolute;
  left: 0;
  top: 0;
  width: 643rpx;
  height: 327rpx;
  z-index: 1;
}
.rec-lotus {
  position: absolute;
  left: 55rpx;
  top: 55rpx;
  width: 36rpx;
  height: 36rpx;
  z-index: 2;
}
.rec-tip {
  position: absolute;
  left: 100rpx;
  top: 58rpx;
  font-size: 25rpx;
  color: #4a7a75;
  font-family: "Songti SC", "STSong", "PingFang SC", serif;
}
.rec-label {
  position: absolute;
  left: 72rpx;
  top: 120rpx;
  font-size: 21rpx;
  color: #4a7a75;
}
.rec-name {
  position: absolute;
  left: 72rpx;
  top: 170rpx;
  font-size: 42rpx;
  line-height: 48rpx;
  color: #30635f;
  font-family: "Songti SC", "STSong", "PingFang SC", serif;
  font-weight: 600;
}
.rec-detail-btn {
  position: absolute;
  left: 72rpx;
  top: 230rpx;
  width: 160rpx;
  height: 54rpx;
  border: 1rpx solid #9dbeba;
  border-radius: 27rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}
.ico-arrow-sm {
  width: 13rpx;
  height: 22rpx;
  margin-left: 8rpx;
}
.rec-detail-txt {
  font-size: 22rpx;
  color: #739a97;
}

/* ===== 底部入口 ===== */
.entry-food,
.entry-make,
.entry-recipe {
  position: absolute;
  z-index: 4;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.entry-food {
  left: 78rpx;
  top: 1370rpx;
  width: 150rpx;
}
.entry-make {
  left: 285rpx;
  top: 1330rpx;
  width: 180rpx;
}
.entry-recipe {
  right: 78rpx;
  top: 1370rpx;
  width: 150rpx;
}
.entry-icon-food,
.entry-icon-recipe {
  width: 108rpx;
  height: 108rpx;
}
.entry-icon-make {
  width: 178rpx;
  height: 178rpx;
}
.entry-label {
  margin-top: 8rpx;
  font-size: 24rpx;
  color: #2f6f6a;
}
.make-label {
  font-size: 26rpx;
  font-weight: 600;
}
</style>
