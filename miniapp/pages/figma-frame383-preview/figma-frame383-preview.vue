<template>
  <view class="frame-383" @tap="onTap">
    <!-- 假状态栏已移除（真机系统自带） -->

    <!-- 假底部 Home Indicator 已移除（真机系统自带） -->

    <!-- Logo -->
    <image class="logo" src="/static/figma-frame383/_1-10.png" mode="widthFix" />
  </view>
</template>

<script>
export default {
  name: "FigmaFrame383Preview",
  methods: {
    onTap() {
      uni.redirectTo({ url: '/pages/figma-frame400-preview/figma-frame400-preview' });
    },
  },
};
</script>

<style scoped>
.frame-383 {
  background: linear-gradient(
    180deg,
    rgba(236, 253, 255, 1) 0%,
    rgba(255, 255, 255, 1) 100%
  );
  height: 100vh;
  /* 812px * 2 */
  position: relative;
  overflow: hidden;
}

/* ── 状态栏 ── */
.status-bar-i-phone {
  padding: 36rpx 50rpx 28rpx 52rpx;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  width: 750rpx;
  position: absolute;
  left: 0;
  top: 0;
}
.time-i-phone {
  flex-shrink: 0;
  width: 108rpx;
  height: 42rpx;
  position: relative;
}
.time {
  color: #000000;
  text-align: center;
  font-family: "SF Pro Text", sans-serif;
  font-size: 34rpx;
  font-weight: 600;
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 108rpx;
}
.cellular-wifi-battery {
  flex-shrink: 0;
  width: 156rpx;
  height: 26rpx;
  position: relative;
}
/* cellular 20×12px → 40rpx × 24rpx */
.icon-cellular {
  width: 40rpx;
  height: 24rpx;
  position: absolute;
  left: 0;
  top: 2rpx;
}
/* wifi 17×12px → 34rpx × 24rpx */
.icon-wifi {
  width: 34rpx;
  height: 24rpx;
  position: absolute;
  left: 54rpx;
  top: 2rpx;
}
/* battery 28×13px → 56rpx × 26rpx */
.icon-battery {
  width: 56rpx;
  height: 26rpx;
  position: absolute;
  right: 0;
  top: 0;
}

/* ── 底部指示条 ── */
.home-indicator-i-phone {
  width: 750rpx;
  height: 38rpx;
  position: absolute;
  left: 0;
  top: 1586rpx;
}
.home-indicator {
  background: #000000;
  border-radius: 192rpx;
  width: 268rpx;
  height: 10rpx;
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  bottom: 16rpx;
}

/* ── Logo ── */
/* 原 AutoHTML: 275×218px, left:49, top:504 */
.logo {
  width: 520rpx;
  position: absolute;
  left: 50%;
  top: 900rpx;
  transform: translateX(-50%);
}
</style>
