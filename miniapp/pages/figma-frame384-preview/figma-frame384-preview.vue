<template>
  <view class="frame-384">
    <!-- 假状态栏已移除（真机系统自带） -->

    <!-- 假底部 Home Indicator 已移除（真机系统自带） -->

    <!-- 返回箭头 -->
    <view class="back-hit" @tap="onBack">
      <image class="ico-back" src="/static/figma-frame384/right0.svg" mode="aspectFit" />
    </view>
    <view class="txt-title">食养局</view>

    <!-- 卡片1：百料匣 -->
    <view class="card card-1" @tap="onTap('百料匣')">
      <view class="card-bg card-bg1"></view>
      <view class="card-bg card-bg1-overlay"></view>
      <image class="card-img" src="/static/figma-frame384/rectangle-13050.png" mode="aspectFill" />
      <view class="card-label card-label-right">百料匣</view>
    </view>

    <!-- 卡片2：安神匣 -->
    <view class="card card-2" @tap="onTap('安神匣')">
      <view class="card-bg card-bg2"></view>
      <image class="card2-i1" src="/static/figma-frame384/_919-fc-7-a-14-d-001-e-23699352-bb-266-f-3917-20.png" mode="aspectFill" />
      <image class="card2-i2" src="/static/figma-frame384/_919-fc-7-a-14-d-001-e-23699352-bb-266-f-3917-40.png" mode="aspectFill" />
      <image class="card2-i3" src="/static/figma-frame384/_919-fc-7-a-14-d-001-e-23699352-bb-266-f-3917-50.png" mode="aspectFill" />
      <image class="card2-i4" src="/static/figma-frame384/_919-fc-7-a-14-d-001-e-23699352-bb-266-f-3917-60.png" mode="aspectFill" />
      <image class="card2-i5" src="/static/figma-frame384/_919-fc-7-a-14-d-001-e-23699352-bb-266-f-3917-70.png" mode="aspectFill" />
      <view class="card-label card-label-right">安神匣</view>
    </view>

    <!-- 卡片3：解郁匣 -->
    <view class="card card-3" @tap="onTap('解郁匣')">
      <view class="card-bg card-bg3"></view>
      <image class="card3-i1" src="/static/figma-frame384/_919-fc-7-a-14-d-001-e-23699352-bb-266-f-3917-21.png" mode="aspectFill" />
      <image class="card3-i2" src="/static/figma-frame384/_919-fc-7-a-14-d-001-e-23699352-bb-266-f-3917-30.png" mode="aspectFill" />
      <image class="card3-i3" src="/static/figma-frame384/_919-fc-7-a-14-d-001-e-23699352-bb-266-f-3917-41.png" mode="aspectFill" />
      <view class="card-label card-label-left">解郁匣</view>
    </view>

    <!-- 卡片4：舒愉匣 -->
    <view class="card card-4" @tap="onTap('舒愉匣')">
      <view class="card-bg card-bg4"></view>
      <image class="card4-i1" src="/static/figma-frame384/_919-fc-7-a-14-d-001-e-23699352-bb-266-f-3917-22.png" mode="aspectFill" />
      <view class="card-label card-label-right">舒愉匣</view>
    </view>
  </view>
</template>

<script>
import { goBack } from '@/utils/nav.js';

export default {
  name: "FigmaFrame384Preview",
  data() { return {}; },
  methods: {
    onBack() { goBack(); },
    onTap(name) {
      if (name === '安神匣') {
        uni.navigateTo({ url: '/pages/figma-frame401-preview/figma-frame401-preview' });
      } else {
        uni.showToast({ title: name + '待补', icon: 'none' });
      }
    },
  },
};
</script>

<style scoped>
.frame-384 { width: 750rpx; height: 100vh; background: #fff; position: relative; overflow: hidden; padding-bottom: env(safe-area-inset-bottom); box-sizing: border-box; }

/* 状态栏 */
.status-bar { display: flex; flex-direction: row; align-items: center; justify-content: space-between; width: 780rpx; position: absolute; left: -14rpx; top: 0; padding: 36rpx 52rpx 28rpx 54rpx; box-sizing: border-box; }
.time-wrap { flex-shrink: 0; width: 108rpx; height: 42rpx; position: relative; }
.time { color: #000; text-align: center; font-family: "SfProText-Semibold", sans-serif; font-size: 34rpx; line-height: 44rpx; letter-spacing: -0.82rpx; font-weight: 600; position: absolute; left: 0; top: 50%; transform: translateY(-50%); width: 108rpx; }
.icons-wrap { flex-shrink: 0; width: 156rpx; height: 26rpx; position: relative; }
.icon-battery { width: 54rpx; height: 26rpx; position: absolute; right: 0; top: 0; }
.icon-wifi { width: 34rpx; height: 24rpx; position: absolute; left: 53rpx; top: 1rpx; }
.icon-cellular { width: 38rpx; height: 24rpx; position: absolute; left: 0; top: 1rpx; }

.home-bar { width: 780rpx; height: 38rpx; position: absolute; left: -14rpx; top: 1586rpx; }
.home-bar-inner { background: #000; border-radius: 200rpx; width: 268rpx; height: 10rpx; position: absolute; left: 50%; transform: translateX(-50%); bottom: 16rpx; }

.back-hit { position: absolute; left: 24rpx; top: 90rpx; width: 80rpx; height: 80rpx; z-index: 10; display: flex; align-items: center; justify-content: center; }
.ico-back { width: 48rpx; height: 48rpx; }
.txt-title { color: #333; text-align: center; font-family: "PingFangSc-Medium", sans-serif; font-size: 32rpx; font-weight: 500; position: absolute; left: 328rpx; top: 108rpx; }

/* 卡片共通 */
.card { position: absolute; left: 40rpx; width: 670rpx; height: 266rpx; overflow: hidden; border-radius: 200rpx; }
.card-bg { position: absolute; left: 0; top: 0; width: 670rpx; height: 266rpx; border-radius: 200rpx; }
.card-label { color: #fff; font-family: "ZCOOL XiaoWei", "Songti SC", "STSong", "KaiTi", serif; font-size: 48rpx; font-weight: 400; position: absolute; height: 38rpx; }
.card-label-right { left: auto; right: 60rpx; }
.card-label-left { left: 112rpx; }

/* 卡片1：百料匣 */
.card-1 { top: 222rpx; }
.card-bg1 { background: linear-gradient(-80.49deg, rgba(206,157,255,0.4) 0%, rgba(232,65,120,0.4) 100%); }
.card-bg1-overlay { background: linear-gradient(-90deg, rgba(246,133,80,0.6) 0%, rgba(156,85,51,0.07) 71.2%, rgba(144,78,47,0) 100%); box-shadow: 0 8rpx 8rpx rgba(0,0,0,0.25); }
.card-1 .card-img { width: 670rpx; height: 266rpx; position: absolute; left: 0; top: 0; border-radius: 200rpx; }
.card-1 .card-label { left: 112rpx; top: 114rpx; }

/* 卡片2：安神匣 */
.card-2 { top: 560rpx; }
.card-bg2 { background: linear-gradient(269.55deg, rgba(201,233,228,1) 0%, rgba(179,184,255,1) 100%); }
.card-2 .card-label { right: 130rpx; top: 110rpx; }
.card2-i1 { width: 154rpx; height: 150rpx; position: absolute; left: 117rpx; top: 59rpx; border-radius: 200rpx; }
.card2-i2 { width: 139rpx; height: 153rpx; position: absolute; left: 40rpx; top: 113rpx; border-radius: 200rpx; }
.card2-i3 { width: 74rpx; height: 82rpx; position: absolute; left: 335rpx; top: 75rpx; border-radius: 200rpx; }
.card2-i4 { width: 74rpx; height: 82rpx; position: absolute; left: 276rpx; top: 68rpx; border-radius: 200rpx; }
.card2-i5 { width: 52rpx; height: 57rpx; position: absolute; left: 311rpx; top: 235rpx; border-radius: 200rpx; }

/* 卡片3：解郁匣 */
.card-3 { top: 901rpx; height: 258rpx; }
.card-bg3 { background: linear-gradient(269.55deg, rgba(201,233,228,1) 0%, rgba(133,210,199,1) 100%); height: 258rpx; }
.card-3 .card-label { left: 112rpx; top: 107rpx; }
.card3-i1 { width: 248rpx; height: 242rpx; position: absolute; left: 446rpx; top: 25rpx; border-radius: 200rpx; }
.card3-i2 { width: 44rpx; height: 96rpx; position: absolute; left: 296rpx; top: 220rpx; border-radius: 200rpx; }
.card3-i3 { width: 27rpx; height: 58rpx; position: absolute; left: 389rpx; top: 67rpx; border-radius: 200rpx; }

/* 卡片4：舒愉匣 */
.card-4 { top: 1242rpx; }
.card-bg4 { background: linear-gradient(-89.15deg, rgba(255,163,197,0.2) 0%, rgba(246,167,129,0.8) 100%); }
.card-4 .card-label { right: 130rpx; top: 110rpx; }
.card4-i1 { width: 483rpx; height: 240rpx; position: absolute; left: -47rpx; top: 12rpx; border-radius: 200rpx; }
</style>
