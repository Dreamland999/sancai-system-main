<template>
  <view class="frame-390">
    <!-- 假状态栏已移除（真机系统自带） -->

    <!-- 假底部 Home Indicator 已移除（真机系统自带） -->

    <!-- 关闭图标 + 取消 -->
    <view class="back-hit" @tap="onCancel">
      <image class="ico-close" src="/static/figma-frame390/close0.svg" mode="aspectFit" />
    </view>
    <view class="txt-cancel" @tap="onCancel">取消</view>

    <!-- Loading 文案 -->
    <view class="txt-loading">专属食材搜集中……</view>
  </view>
</template>

<script>
import { goBack } from '@/utils/nav.js';
import { recommend } from '@/api/recommend.js';

export default {
  name: "FigmaFrame390Preview",
  data() {
    return {
      _timer: null,
      _done: false,
    };
  },
  mounted() {
    this.fetchRecommend();
  },
  beforeUnmount() {
    this._done = true;
    if (this._timer) {
      clearTimeout(this._timer);
      this._timer = null;
    }
  },
  methods: {
    onCancel() {
      goBack();
    },
    goNext() {
      if (this._done) return;
      this._done = true;
      uni.redirectTo({ url: '/pages/figma-frame389-preview/figma-frame389-preview' });
    },
    async fetchRecommend() {
      // 至少显示 800ms loading
      const minWait = new Promise(resolve => setTimeout(resolve, 800));
      const input = uni.getStorageSync('recommend_input') || {};
      console.log('[Frame390] recommend payload', JSON.stringify(input));

      const result = await recommend(input);
      uni.setStorageSync('recommend_result', result);
      console.log('[Frame390] recommend_result saved, model_mode:', result.model_mode);

      await minWait;
      this.goNext();
    },
  },
};
</script>

<style scoped>
.frame-390 {
  width: 750rpx;
  height: 100vh;
  background: #ffffff;
  position: relative;
  overflow: hidden;
  padding-bottom: env(safe-area-inset-bottom);
  box-sizing: border-box;
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

/* 关闭图标热区 */
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
.ico-close {
  width: 48rpx;
  height: 48rpx;
}

/* 取消 */
.txt-cancel {
  color: #666666;
  font-family: "PingFangSc-Medium", sans-serif;
  font-size: 32rpx;
  font-weight: 500;
  position: absolute;
  left: 104rpx;
  top: 108rpx;
}

/* Loading 文案 */
.txt-loading {
  color: #111111;
  text-align: center;
  font-family: "ZCOOL XiaoWei", "Songti SC", "STSong", "KaiTi", serif;
  font-size: 46rpx;
  line-height: 56rpx;
  letter-spacing: 6rpx;
  font-weight: 400;
  position: absolute;
  left: 0;
  right: 0;
  bottom: 120rpx;
}
</style>
