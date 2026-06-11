<template>
  <view class="frame-382">
    <!-- 假状态栏已移除（真机系统自带） -->

    <!-- 假底部 Home Indicator 已移除（真机系统自带） -->

    <!-- 返回 + 标题 -->
    <view class="back-hit" @tap="onBack">
      <image class="ico-back" src="/static/figma-frame382/right0.svg" />
    </view>
    <view class="txt-title">实时了解</view>
    <view class="txt-history" @tap="onHistory">历史</view>

    <!-- 圆形 logo 区 -->
    <view class="logo-area">
      <view class="logo-glow-outer"></view>
      <view class="logo-glow-inner"></view>
      <image
        class="logo-img"
        src="/static/figma-frame382/b-8-b-9-a-543-d-10-f-48-fafb-88-aa-0-fb-39-d-4987-10.png"
        mode="aspectFit"
        @tap="onLogo"
      />
    </view>

    <!-- 识别文案 -->
    <view class="listening-texts">
      <text class="t-muted">小才与您的眼睛产生了对话...</text>
      <text class="t-muted">小才正在了解您的心情......</text>
      <text class="t-active">小才正在聆听您的心跳...</text>
      <text class="t-dots">......</text>
    </view>
  </view>
</template>

<script>
import { goBack } from '@/utils/nav.js';

export default {
  name: "FigmaFrame382Preview",
  methods: {
    onBack()    { goBack(); },
    onHistory() { uni.showToast({ title: "历史", icon: "none" }); },
    onLogo() {
      const recognitionFlow = uni.getStorageSync('recognition_flow');
      if (recognitionFlow) {
        uni.removeStorageSync('recognition_flow');
        uni.redirectTo({ url: '/pages/figma-frame399-preview/figma-frame399-preview' });
      } else {
        uni.navigateTo({ url: '/pages/figma-frame394-preview/figma-frame394-preview' });
      }
    },
  },
};
</script>

<style scoped>
.frame-382 {
  background: linear-gradient(180deg, rgba(236,253,255,1) 0%, rgba(255,255,255,1) 100%);
  height: 100vh;
  position: relative;
  overflow: hidden;
}

/* status bar */
.status-bar { padding: 36rpx 50rpx 28rpx 52rpx; display: flex; flex-direction: row; align-items: center; justify-content: space-between; width: 750rpx; position: absolute; left: 0; top: 0; }
.time-wrap { flex-shrink: 0; width: 108rpx; height: 42rpx; position: relative; }
.time { color: #000; text-align: center; font-family: "SF Pro Text", sans-serif; font-size: 34rpx; font-weight: 600; position: absolute; left: 0; top: 50%; transform: translateY(-50%); width: 108rpx; }
.icons-wrap { flex-shrink: 0; width: 156rpx; height: 26rpx; position: relative; }
.icon-cellular { width: 38rpx; height: 24rpx; position: absolute; left: 0; top: 2rpx; }
.icon-wifi { width: 34rpx; height: 24rpx; position: absolute; left: 54rpx; top: 2rpx; }
.icon-battery { width: 56rpx; height: 26rpx; position: absolute; right: 0; top: 0; }

/* home bar */
.home-bar { width: 750rpx; height: 38rpx; position: absolute; left: 0; top: 1586rpx; }
.home-bar-inner { background: #000; border-radius: 192rpx; width: 268rpx; height: 10rpx; position: absolute; left: 50%; transform: translateX(-50%); bottom: 16rpx; }

/* nav */
.back-hit { position: absolute; left: 4rpx; top: 90rpx; width: 80rpx; height: 80rpx; z-index: 10; display: flex; align-items: center; justify-content: center; }
.ico-back { width: 48rpx; height: 48rpx; }
.txt-title { color: #333; font-size: 32rpx; font-weight: 500; position: absolute; left: 308rpx; top: 108rpx; }
.txt-history { color: #333; font-size: 32rpx; font-weight: 500; position: absolute; right: 120rpx; top: 108rpx; }

/* logo circle area (252×252px → 504×504rpx, left:60 → 120rpx, top:210 → 420rpx) */
.logo-area { width: 504rpx; height: 504rpx; position: absolute; left: 120rpx; top: 420rpx; }
.logo-glow-outer { border-radius: 50%; width: 100%; height: 504rpx; position: absolute; left: 0; top: 0; background: rgba(255,255,255,0.3); }
.logo-glow-inner { border-radius: 50%; width: 75%; height: 378rpx; position: absolute; left: 12.5%; top: 64rpx; background: rgba(107,230,213,0.22); }
.logo-img { width: 45%; height: 228rpx; position: absolute; left: 27.5%; top: 138rpx; }

/* listening text container */
.listening-texts {
  position: absolute;
  left: 50%;
  top: 960rpx;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 600rpx;
}
.t-muted {
  display: block;
  color: #bbb;
  font-size: 26rpx;
  line-height: 44rpx;
  margin-bottom: 16rpx;
}
.t-active {
  display: block;
  color: #333;
  font-size: 28rpx;
  font-weight: 600;
  line-height: 44rpx;
  margin-bottom: 16rpx;
}
.t-dots {
  display: block;
  color: #aaa;
  font-size: 30rpx;
  font-weight: 600;
  line-height: 44rpx;
}
</style>
