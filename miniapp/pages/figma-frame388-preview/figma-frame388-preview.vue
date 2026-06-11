<template>
  <view class="frame-388">
    <!-- 顶部白色底色 -->
    <view class="top-bar"></view>

    <!-- 假状态栏已移除（真机系统自带） -->

    <!-- 假底部 Home Indicator 已移除（真机系统自带） -->

    <!-- 返回箭头 -->
    <view class="back-hit" @tap="onBack">
      <image class="ico-back" src="/static/figma-frame388/right0.svg" mode="aspectFit" />
    </view>
    <!-- 标题 -->
    <view class="txt-title">支付</view>

    <!-- 左上大面积装饰背景（group-12290.svg 为空，CSS 绘制） -->
    <view class="bg-decor"></view>

    <!-- 杯子后方白色柔光 -->
    <view class="cup-glow"></view>

    <!-- 杯子容器（frame-251） -->
    <view class="cup-container">
      <!-- 杯子裁剪区 _1 -->
      <view class="cup-clip">
        <image class="cup-v0" src="/static/figma-frame388/vector0.svg" mode="aspectFit" />
        <image class="cup-g13" src="/static/figma-frame388/group-13130.svg" mode="aspectFit" />
        <image class="cup-g16" src="/static/figma-frame388/group-13160.svg" mode="aspectFit" />
        <image class="cup-v1" src="/static/figma-frame388/vector1.svg" mode="aspectFit" />
        <!-- group-13390.svg 为空，跳过 -->
      </view>
      <image class="cup-g13430" src="/static/figma-frame388/group-13430.svg" mode="aspectFit" />
      <image class="cup-g13170" src="/static/figma-frame388/group-13170.svg" mode="aspectFit" />
      <image class="cup-g13431" src="/static/figma-frame388/group-13431.svg" mode="aspectFit" />
    </view>

    <!-- 饮品名称 -->
    <view class="drink-name">解暑纤果茶</view>

    <!-- 配送服务按钮（白底青边框） -->
    <view class="btn-delivery" @tap="onDelivery">
      <view class="btn-delivery-bg"></view>
      <view class="btn-delivery-text">配送服务</view>
    </view>

    <!-- 附近自提按钮（青绿色实心） -->
    <view class="btn-pickup" @tap="onPickup">
      <view class="btn-pickup-bg"></view>
      <view class="btn-pickup-text">附近自提</view>
    </view>
  </view>
</template>

<script>
export default {
  name: "FigmaFrame388Preview",
  data() {
    return {};
  },
  mounted() {
    const config = uni.getStorageSync('custom_recipe_config') || {};
    const recipe = uni.getStorageSync('current_recipe') || {};
    console.log('[Frame388] custom_recipe_config:', config, 'recipe:', recipe.name);
  },
  methods: {
    onBack() {
      console.log('[Frame388] click back');
      const pages = getCurrentPages();
      if (pages.length > 1) {
        uni.navigateBack({
          fail(err) { console.error('[Frame388] navigateBack failed', err); }
        });
      } else {
        uni.redirectTo({
          url: '/pages/figma-frame391-preview/figma-frame391-preview',
          fail(err) { console.error('[Frame388] redirectTo failed', err); }
        });
      }
    },
    onDelivery() {
      console.log('[Frame388] click delivery');
      uni.showToast({ title: '配送页待补', icon: 'none' });
    },
    onPickup() {
      console.log('[Frame388] click pickup -> navigateTo Frame387');
      uni.navigateTo({ url: '/pages/figma-frame387-preview/figma-frame387-preview' });
    },
  },
};
</script>

<style scoped>
.frame-388 {
  width: 750rpx; height: 100vh; background: #fff;
  position: relative; overflow: hidden;
  padding-bottom: env(safe-area-inset-bottom); box-sizing: border-box;
}

/* 顶部白色底色 */
.top-bar { background: #fff; width: 750rpx; height: 176rpx; position: absolute; left: 0; top: -10rpx; }

/* 状态栏 */
.status-bar { display: flex; flex-direction: row; align-items: center; justify-content: space-between; width: 780rpx; position: absolute; left: -14rpx; top: 0; padding: 36rpx 52rpx 28rpx 54rpx; box-sizing: border-box; }
.time-wrap { flex-shrink: 0; width: 108rpx; height: 42rpx; position: relative; }
.time { color: #333; text-align: center; font-family: "SfProText-Semibold", sans-serif; font-size: 34rpx; line-height: 44rpx; letter-spacing: -0.82rpx; font-weight: 600; position: absolute; left: 0; top: 50%; transform: translateY(-50%); width: 108rpx; }
.icons-wrap { flex-shrink: 0; width: 156rpx; height: 26rpx; position: relative; }
.icon-battery { width: 54rpx; height: 26rpx; position: absolute; right: 0; top: 0; }
.icon-wifi { width: 34rpx; height: 24rpx; position: absolute; left: 53rpx; top: 1rpx; }
.icon-cellular { width: 38rpx; height: 24rpx; position: absolute; left: 0; top: 1rpx; }

/* Home Indicator */
.home-bar { width: 780rpx; height: 38rpx; position: absolute; left: -14rpx; top: 1586rpx; }
.home-bar-inner { background: #000; border-radius: 200rpx; width: 268rpx; height: 10rpx; position: absolute; left: 50%; transform: translateX(-50%); bottom: 16rpx; }

/* 返回箭头热区 */
.back-hit { position: absolute; left: 18rpx; top: 84rpx; width: 88rpx; height: 88rpx; z-index: 10; display: flex; align-items: center; justify-content: center; }
.ico-back { width: 48rpx; height: 48rpx; }
.txt-title { color: #333; text-align: center; font-family: "PingFangSc-Medium", sans-serif; font-size: 32rpx; font-weight: 500; position: absolute; left: 344rpx; top: 108rpx; }

/* 装饰背景（group-12290.svg 为空，CSS 替代） */
.bg-decor { position: absolute; left: -478rpx; top: -616rpx; width: 900rpx; height: 900rpx; background: radial-gradient(ellipse at 65% 55%, rgba(133,210,199,0.12) 0%, rgba(133,210,199,0.04) 40%, transparent 70%); border-radius: 50%; pointer-events: none; }

/* 杯子后方柔光（ellipse-47） */
.cup-glow { background: #fff; border-radius: 50%; width: 316rpx; height: 312rpx; position: absolute; left: 220rpx; top: 386rpx; filter: blur(80rpx); }

/* frame-251 杯子容器 */
.cup-container { position: absolute; left: 166rpx; top: 410rpx; width: 420rpx; height: 445rpx; }
.cup-clip { width: 420rpx; height: 420rpx; position: absolute; left: 0; top: 25rpx; overflow: hidden; }

/* 杯子内 SVG（相对 420×420rpx） */
.cup-v0  { width: 174rpx; height: 63rpx; position: absolute; left: 124rpx; top: 357rpx; }
.cup-g13 { width: 235rpx; height: 389rpx; position: absolute; left: 92rpx; top: 6rpx; }
.cup-g16 { width: 239rpx; height: 171rpx; position: absolute; left: 92rpx; top: 63rpx; }
.cup-v1  { width: 30rpx; height: 249rpx; position: absolute; left: 288rpx; top: 107rpx; }

/* 杯子外装饰 SVG（相对 cup-container） */
.cup-g13430 { width: 100rpx; height: 100rpx; position: absolute; left: 98rpx; top: -12rpx; }
.cup-g13170 { width: 255rpx; height: 162rpx; position: absolute; left: 83rpx; top: 0; }
.cup-g13431 { width: 100rpx; height: 100rpx; position: absolute; left: 197rpx; top: 15rpx; }

/* 饮品名称 */
.drink-name { color: #000; text-align: left; font-family: "ZCOOL XiaoWei", "Songti SC", "STSong", "KaiTi", serif; font-size: 48rpx; font-weight: 400; position: absolute; left: 252rpx; top: 898rpx; }

/* 配送服务按钮（白底青边框） */
.btn-delivery { position: absolute; left: 136rpx; top: 1112rpx; width: 480rpx; height: 100rpx; z-index: 5; }
.btn-delivery-bg { background: #fff; border-radius: 60rpx; border: 2rpx solid #85d2c7; width: 480rpx; height: 100rpx; position: absolute; left: 0; top: 0; pointer-events: none; }
.btn-delivery-text { color: #85d2c7; text-align: center; font-family: "PingFangSc-Medium", sans-serif; font-size: 40rpx; font-weight: 500; position: absolute; left: 0; top: 50%; transform: translateY(-50%); width: 480rpx; pointer-events: none; }

/* 附近自提按钮（青绿实心白字） */
.btn-pickup { position: absolute; left: 136rpx; top: 1272rpx; width: 480rpx; height: 100rpx; z-index: 5; }
.btn-pickup-bg { background: #56bfb0; border-radius: 60rpx; border: 2rpx solid #fff; width: 480rpx; height: 100rpx; position: absolute; left: 0; top: 0; pointer-events: none; }
.btn-pickup-text { color: #fff; text-align: center; font-family: "PingFangSc-Medium", sans-serif; font-size: 40rpx; font-weight: 500; position: absolute; left: 0; top: 50%; transform: translateY(-50%); width: 480rpx; pointer-events: none; }
</style>
