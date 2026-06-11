<template>
  <view class="frame-387">
    <!-- 地图背景 -->
    <image class="map-bg" src="/static/figma-frame387/image-50.jpg" mode="aspectFill" />

    <!-- 假状态栏已移除（真机系统自带） -->

    <!-- 返回 + 标题 -->
    <view class="back-hit" @tap="onBack">
      <image class="ico-back" src="/static/figma-frame387/right0.svg" mode="aspectFit" />
    </view>
    <view class="txt-title">确定门店</view>

    <!-- 地图 marker -->
    <image class="map-marker" src="/static/figma-frame387/_10.svg" mode="aspectFit" />

    <!-- 白色圆角面板 -->
    <view class="panel">
      <!-- 搜索栏 -->
      <view class="panel-location">华南理工大学…</view>
      <view class="search-box" @tap="onSearch">
        <image class="search-icon" src="/static/figma-frame387/search0.svg" mode="aspectFit" />
        <text class="search-text">搜索地址</text>
      </view>
      <image class="locate-icon" src="/static/figma-frame387/_11.svg" mode="aspectFit" @tap="onLocate" />

      <!-- 门店列表 scroll-view -->
      <scroll-view class="store-list" scroll-y>
        <view
          v-for="(store, i) in stores"
          :key="i"
          class="store-card"
          :class="{ 'store-active': i === 0 }"
          @tap="goOrderCode"
        >
          <view class="store-bg" style="pointer-events: none;"></view>
          <image class="store-img" :src="store.img" mode="aspectFill" style="pointer-events: none;" />
          <view class="store-name" style="pointer-events: none;">{{ store.name }}</view>
          <view class="store-distance" style="pointer-events: none;">{{ store.distance }}</view>
          <view class="store-addr" style="pointer-events: none;">{{ store.address }}</view>
        </view>
      </scroll-view>
    </view>

    <!-- 假底部 Home Indicator 已移除（真机系统自带） -->
  </view>
</template>

<script>
import { goBack } from '@/utils/nav.js';
import { sendFeedback } from '@/api/feedback.js';

const S = "/static/figma-frame387/";
export default {
  name: "FigmaFrame387Preview",
  data() {
    return {
      stores: [
        { img: S + "rectangle-13030.png", name: "华南理工大学售货机", distance: "256m |", address: "华南理工大学大学城校区C10楼下" },
        { img: S + "rectangle-13031.png", name: "广州工业大学售货机", distance: "1.2km |", address: "广州工业大学大学城校区E13楼下" },
        { img: S + "rectangle-13032.png", name: "万胜围广场售货机", distance: "6.8km |", address: "万胜围地铁站D口出口处" },
        { img: S + "rectangle-13033.png", name: "琶洲广交会售货机", distance: "256m |", address: "华南理工大学大学城校区C10楼下" },
      ],
    };
  },
  methods: {
    onBack() {
      console.log('[Frame387] click back');
      goBack();
    },
    onSearch() { uni.showToast({ title: "搜索地址", icon: "none" }); },
    onLocate() { uni.showToast({ title: "定位", icon: "none" }); },
    goOrderCode() {
      console.log('[Frame387] click store card');
      const card = this.stores[0] || {};
      sendFeedback('select_store', { store_name: card.name || '' });
      uni.redirectTo({ url: '/pages/figma-frame385-preview/figma-frame385-preview' });
    },
  },
};
</script>

<style scoped>
.frame-387 { width: 750rpx; height: 100vh; background: #fff; position: relative; overflow: hidden; padding-bottom: env(safe-area-inset-bottom); box-sizing: border-box; }

/* 地图背景 */
.map-bg { width: 1782rpx; height: 3168rpx; position: absolute; left: -180rpx; top: -1380rpx; }

/* 顶部白色半透明条 */
.top-bar-bg { background: rgba(255,255,255,0.8); width: 750rpx; height: 176rpx; position: absolute; left: 0; top: 0; }

/* 状态栏 */
.status-bar { display: flex; flex-direction: row; align-items: center; justify-content: space-between; width: 780rpx; position: absolute; left: -14rpx; top: 0; padding: 36rpx 52rpx 28rpx 54rpx; box-sizing: border-box; z-index: 2; }
.time-wrap { flex-shrink: 0; width: 108rpx; height: 42rpx; position: relative; }
.time { color: #000; text-align: center; font-family: "SfProText-Semibold", sans-serif; font-size: 34rpx; line-height: 44rpx; letter-spacing: -0.82rpx; font-weight: 600; position: absolute; left: 0; top: 50%; transform: translateY(-50%); width: 108rpx; }
.icons-wrap { flex-shrink: 0; width: 156rpx; height: 26rpx; position: relative; }
.icon-battery { width: 54rpx; height: 26rpx; position: absolute; right: 0; top: 0; }
.icon-wifi { width: 34rpx; height: 24rpx; position: absolute; left: 53rpx; top: 1rpx; }
.icon-cellular { width: 38rpx; height: 24rpx; position: absolute; left: 0; top: 1rpx; }

/* 返回 + 标题 */
.back-hit { position: absolute; left: 24rpx; top: 90rpx; width: 80rpx; height: 80rpx; z-index: 10; display: flex; align-items: center; justify-content: center; }
.ico-back { width: 48rpx; height: 48rpx; }
.txt-title { color: #333; text-align: center; font-family: "PingFangSc-Medium", sans-serif; font-size: 32rpx; font-weight: 500; position: absolute; left: 312rpx; top: 108rpx; z-index: 2; }

/* 地图 marker */
.map-marker { width: 72rpx; height: 72rpx; position: absolute; left: 348rpx; top: 232rpx; z-index: 2; }

/* 白色圆角面板 */
.panel { background: #fff; border-radius: 40rpx 40rpx 0 0; width: 750rpx; height: 978rpx; position: absolute; left: 0; top: 646rpx; z-index: 3; }

/* 当前位置 + 搜索栏 */
.panel-location { color: #666; font-family: "PingFangSc-Regular", sans-serif; font-size: 28rpx; font-weight: 400; position: absolute; left: 30rpx; top: 56rpx; }
.search-box { background: rgba(133,210,199,0.2); border-radius: 20rpx; border: 2rpx solid #85d2c7; width: 456rpx; height: 60rpx; position: absolute; left: 254rpx; top: 46rpx; display: flex; align-items: center; padding-left: 28rpx; box-sizing: border-box; }
.search-icon { width: 32rpx; height: 32rpx; }
.search-text { color: #85d2c7; font-family: "PingFangSc-Regular", sans-serif; font-size: 28rpx; font-weight: 400; margin-left: 8rpx; }
.locate-icon { width: 40rpx; height: 40rpx; position: absolute; right: 30rpx; top: 56rpx; }

/* 门店列表 */
.store-list { position: absolute; left: 40rpx; top: 140rpx; width: 670rpx; height: 820rpx; }

/* 门店卡片 */
.store-card { width: 670rpx; height: 200rpx; margin-bottom: 20rpx; position: relative; border-radius: 16rpx; overflow: hidden; }
.store-bg { width: 670rpx; height: 200rpx; position: absolute; left: 0; top: 0; border-radius: 16rpx; background: #fff; }
.store-active .store-bg { background: rgba(133,210,199,0.2); }

.store-img { width: 120rpx; height: 120rpx; position: absolute; left: 28rpx; top: 40rpx; border-radius: 8rpx; }
.store-name { color: #333; font-family: "PingFangSc-Medium", sans-serif; font-size: 32rpx; font-weight: 500; position: absolute; left: 184rpx; top: 48rpx; }
.store-distance { color: #666; font-family: "PingFangSc-Medium", sans-serif; font-size: 24rpx; font-weight: 500; position: absolute; left: 182rpx; top: 116rpx; }
.store-addr { color: #999; font-family: "PingFangSc-Regular", sans-serif; font-size: 24rpx; font-weight: 400; position: absolute; left: 270rpx; top: 116rpx; white-space: nowrap; }

/* Home Indicator */
.home-bar { width: 780rpx; height: 38rpx; position: absolute; left: -14rpx; top: 1586rpx; z-index: 3; }
.home-bar-inner { background: #000; border-radius: 200rpx; width: 268rpx; height: 10rpx; position: absolute; left: 50%; transform: translateX(-50%); bottom: 16rpx; }
</style>
