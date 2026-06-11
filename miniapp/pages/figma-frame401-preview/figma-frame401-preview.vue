<template>
  <view class="frame-401">
    <!-- 假状态栏已移除（真机系统自带） -->

    <!-- 假底部 Home Indicator 已移除（真机系统自带） -->

    <!-- 返回箭头 + 标题 -->
    <view class="back-hit" @tap="onBack">
      <image class="ico-back" src="/static/figma-frame401/right0.svg" mode="aspectFit" />
    </view>
    <view class="txt-title">安神局</view>

    <!-- "基底：" -->
    <view class="sec-label sec-label-base">基底：</view>

    <!-- 基底食材卡片（2行×5列） -->
    <view
      v-for="(item, i) in baseCards"
      :key="'b' + i"
      class="ing-card ing-card-base"
      :style="{ left: cX[i % 5] + 'rpx', top: cY[i < 5 ? 0 : 1] + 'rpx' }"
      @tap="onSelect"
    >
      <view class="ing-card-bg ing-bg-base"></view>
      <image class="ing-card-img" :src="item.src" mode="aspectFill" />
      <view class="ing-card-name">{{ item.name }}</view>
    </view>

    <!-- "风味剂：" -->
    <view class="sec-label sec-label-flavor">风味剂：</view>

    <!-- 风味剂食材卡片（2行×5列） -->
    <view
      v-for="(item, i) in flavorCards"
      :key="'f' + i"
      class="ing-card ing-card-flavor"
      :style="{ left: cX[i % 5] + 'rpx', top: fY[i < 5 ? 0 : 1] + 'rpx' }"
      @tap="onSelect"
    >
      <view class="ing-card-bg ing-bg-flavor"></view>
      <image class="ing-card-img" :src="item.src" mode="aspectFill" />
      <view class="ing-card-name">{{ item.name }}</view>
    </view>

    <!-- 白色浮层面板 -->
    <view class="overlay-panel"></view>

    <!-- 8 个加号选择槽 -->
    <view
      v-for="(slot, i) in plusSlots"
      :key="'p' + i"
      class="plus-slot"
      :style="{ left: slot.l + 'rpx', top: slot.t + 'rpx' }"
      @tap="onAdd"
    >
      <view class="plus-slot-bg"></view>
      <image class="plus-slot-icon" :src="slot.src" mode="aspectFit" />
    </view>

    <!-- "下一步"按钮 -->
    <view class="btn-next" @tap="onNext">
      <view class="btn-next-bg"></view>
      <view class="btn-next-text">下一步</view>
    </view>
  </view>
</template>

<script>
import { goBack } from '@/utils/nav.js';

const STATIC = "/static/figma-frame401/";

export default {
  name: "FigmaFrame401Preview",
  data() {
    return {
      selectedCount: 0,
      cX: [46, 182, 318, 454, 590],
      cY: [296, 500],
      fY: [804, 1008],
      baseCards: [
        { src: STATIC + "image-710.png", name: "针茅" },
        { src: STATIC + "image-711.png", name: "茉莉花茶" },
        { src: STATIC + "image-712.png", name: "薄荷叶" },
        { src: STATIC + "image-713.png", name: "罗汉果" },
        { src: STATIC + "image-714.png", name: "菊花" },
        { src: STATIC + "image-715.png", name: "咖啡豆" },
        { src: STATIC + "image-716.png", name: "乌龙茶叶" },
        { src: STATIC + "image-717.png", name: "蓝楹花" },
        { src: STATIC + "image-718.png", name: "白茶" },
        { src: STATIC + "image-719.png", name: "玫瑰花" },
      ],
      flavorCards: [
        { src: STATIC + "image-70.png", name: "乌龙茶叶" },
        { src: STATIC + "image-71.png", name: "乌龙茶叶" },
        { src: STATIC + "image-72.png", name: "乌龙茶叶" },
        { src: STATIC + "image-73.png", name: "乌龙茶叶" },
        { src: STATIC + "image-74.png", name: "乌龙茶叶" },
        { src: STATIC + "image-75.png", name: "乌龙茶叶" },
        { src: STATIC + "image-76.png", name: "乌龙茶叶" },
        { src: STATIC + "image-77.png", name: "乌龙茶叶" },
        { src: STATIC + "image-78.png", name: "乌龙茶叶" },
        { src: STATIC + "image-79.png", name: "乌龙茶叶" },
      ],
      plusSlots: [
        { l: 88,  t: 970,  src: STATIC + "plus0.svg" },
        { l: 242, t: 970,  src: STATIC + "plus1.svg" },
        { l: 396, t: 970,  src: STATIC + "plus2.svg" },
        { l: 550, t: 970,  src: STATIC + "plus3.svg" },
        { l: 88,  t: 1190, src: STATIC + "plus4.svg" },
        { l: 242, t: 1190, src: STATIC + "plus5.svg" },
        { l: 396, t: 1190, src: STATIC + "plus6.svg" },
        { l: 550, t: 1190, src: STATIC + "plus7.svg" },
      ],
    };
  },
  methods: {
    onBack() { goBack(); },
    onSelect() { this.selectedCount++; },
    onAdd() { uni.showToast({ title: "添加食材", icon: "none" }); },
    onNext() {
      if (this.selectedCount === 0) {
        uni.showToast({ title: "请先选择食材", icon: "none" });
      } else {
        uni.navigateTo({ url: '/pages/figma-frame390-preview/figma-frame390-preview' });
      }
    },
  },
};
</script>

<style scoped>
.frame-401 { width: 750rpx; height: 100vh; background: linear-gradient(180deg, #fff 100%); position: relative; overflow: hidden; padding-bottom: env(safe-area-inset-bottom); box-sizing: border-box; }

.status-bar { display: flex; flex-direction: row; align-items: center; justify-content: space-between; width: 780rpx; position: absolute; left: -14rpx; top: 0; padding: 36rpx 52rpx 28rpx 54rpx; box-sizing: border-box; }
.time-wrap { flex-shrink: 0; width: 108rpx; height: 42rpx; position: relative; }
.time { color: #000; text-align: center; font-family: "SfProText-Semibold", sans-serif; font-size: 34rpx; line-height: 44rpx; letter-spacing: -0.82rpx; font-weight: 600; position: absolute; left: 0; top: 50%; transform: translateY(-50%); width: 108rpx; }
.icons-wrap { flex-shrink: 0; width: 156rpx; height: 26rpx; position: relative; }
.icon-battery { width: 54rpx; height: 26rpx; position: absolute; right: 0; top: 0; }
.icon-wifi { width: 34rpx; height: 24rpx; position: absolute; left: 53rpx; top: 1rpx; }
.icon-cellular { width: 38rpx; height: 24rpx; position: absolute; left: 0; top: 1rpx; }

.home-bar { background: rgba(255,255,255,0.8); width: 780rpx; height: 38rpx; position: absolute; left: -14rpx; top: 1586rpx; }
.home-bar-inner { background: #000; border-radius: 200rpx; width: 268rpx; height: 10rpx; position: absolute; left: 50%; transform: translateX(-50%); bottom: 16rpx; }

.back-hit { position: absolute; left: 24rpx; top: 90rpx; width: 80rpx; height: 80rpx; z-index: 10; display: flex; align-items: center; justify-content: center; }
.ico-back { width: 48rpx; height: 48rpx; }
.txt-title { color: #333; text-align: center; font-family: "PingFangSc-Medium", sans-serif; font-size: 32rpx; font-weight: 500; position: absolute; left: 328rpx; top: 108rpx; }

/* 分类标签 */
.sec-label { color: #333; font-family: "PingFangSc-Medium", sans-serif; font-size: 28rpx; font-weight: 500; position: absolute; left: 40rpx; }
.sec-label-base { top: 232rpx; }
.sec-label-flavor { top: 740rpx; }

/* 食材卡片 */
.ing-card { position: absolute; width: 116rpx; height: 180rpx; }
.ing-card-bg { width: 116rpx; height: 180rpx; position: absolute; left: 0; top: 0; border-radius: 40rpx; }
.ing-bg-base { background: rgba(133,210,199,0.2); }
.ing-bg-flavor { background: rgba(255,206,206,0.4); }
.ing-card-img { width: 106rpx; height: 106rpx; position: absolute; left: 5rpx; top: 34rpx; border-radius: 40rpx; }
.ing-card-name { color: #666; text-align: center; font-family: "PingFangSc-Medium", sans-serif; font-size: 20rpx; font-weight: 500; position: absolute; left: 0; top: 138rpx; width: 116rpx; }

/* 白色浮层面板 */
.overlay-panel { background: #fff; border-radius: 16rpx 16rpx 0 0; width: 750rpx; height: 708rpx; position: absolute; left: 0; top: 916rpx; box-shadow: 0 -4rpx 8rpx rgba(0,0,0,0.1); }

/* 加号选择槽 */
.plus-slot { position: absolute; width: 116rpx; height: 180rpx; }
.plus-slot-bg { background: rgba(238,238,238,0.6); border-radius: 40rpx; width: 116rpx; height: 180rpx; position: absolute; left: 0; top: 0; }
.plus-slot-icon { width: 146rpx; height: 146rpx; position: absolute; left: -15rpx; top: 17rpx; }

/* 下一步按钮 */
.btn-next { position: absolute; left: 156rpx; top: 1432rpx; width: 440rpx; height: 80rpx; }
.btn-next-bg { background: #ccc; border-radius: 60rpx; border: 2rpx solid #fff; width: 440rpx; height: 80rpx; position: absolute; left: 0; top: 0; }
.btn-next-text { color: #fff; text-align: center; font-family: "PingFangSc-Medium", sans-serif; font-size: 32rpx; font-weight: 500; position: absolute; left: 0; top: 50%; transform: translateY(-50%); width: 440rpx; }
</style>
