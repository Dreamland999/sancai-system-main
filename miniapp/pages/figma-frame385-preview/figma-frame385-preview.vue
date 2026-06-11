<template>
  <view class="frame-385">
    <!-- 假状态栏已移除（真机系统自带） -->

    <!-- 假底部 Home Indicator 已移除（真机系统自带） -->

    <!-- 返回箭头 -->
    <view class="back-hit" @tap="onBack">
      <image class="ico-back" src="/static/figma-frame385/right0.svg" mode="aspectFit" />
    </view>
    <view class="txt-title">订单生成</view>

    <!-- 莲花线稿 logo -->
    <image class="img-logo" src="/static/figma-frame385/_1-20.png" mode="aspectFit" @tap="onTap" />

    <!-- 取餐码 305 -->
    <view class="code-num" @tap="onTap">305</view>

    <!-- 条形码 -->
    <image class="img-barcode" src="/static/figma-frame385/image-60.png" mode="aspectFit" @tap="onTap" />
  </view>
</template>

<script>
import { goBack } from '@/utils/nav.js';
import { sendFeedback } from '@/api/feedback.js';

export default {
  name: "FigmaFrame385Preview",
  data() { return {}; },
  mounted() {
    const config = uni.getStorageSync('custom_recipe_config') || {};
    const recipe = uni.getStorageSync('current_recipe') || {};
    console.log('[Frame385] custom_recipe_config:', config, 'recipe:', recipe.name);
  },
  methods: {
    onBack() { goBack(); },
    onTap() {
      const config = uni.getStorageSync('custom_recipe_config') || {};
      const recipe = uni.getStorageSync('current_recipe') || {};
      sendFeedback('create_order', { custom_recipe_config: config, recipe_id: recipe.recipe_id, recipe_name: recipe.name });
      uni.redirectTo({ url: '/pages/figma-frame386-preview/figma-frame386-preview' });
    },
  },
};
</script>

<style scoped>
.frame-385 { width: 750rpx; height: 100vh; background: linear-gradient(180deg, rgba(236,253,255,1) 0%, rgba(255,255,255,1) 100%); position: relative; overflow: hidden; padding-bottom: env(safe-area-inset-bottom); box-sizing: border-box; }

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
.txt-title { color: #333; text-align: center; font-family: "PingFangSc-Medium", sans-serif; font-size: 32rpx; font-weight: 500; position: absolute; left: 312rpx; top: 108rpx; }

.img-logo { width: 530rpx; height: 266rpx; position: absolute; left: 106rpx; top: 338rpx; }

.code-num { color: #85d2c7; font-family: "ZCOOL XiaoWei", "Songti SC", "STSong", "KaiTi", serif; font-size: 128rpx; font-weight: 400; position: absolute; left: 270rpx; top: 684rpx; }

.img-barcode { width: 450rpx; height: 272rpx; position: absolute; left: 150rpx; top: 876rpx; }
</style>
