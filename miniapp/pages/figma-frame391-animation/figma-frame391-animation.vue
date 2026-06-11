<template>
  <view class="frame-anim">
    <video
      class="anim-video"
      :src="videoSrc"
      autoplay
      muted
      :controls="false"
      :show-center-play-btn="false"
      :show-play-btn="false"
      :show-fullscreen-btn="false"
      :enable-progress-gesture="false"
      object-fit="cover"
      @ended="onVideoEnd"
      @error="onVideoError"
    />
    <view class="skip-btn" @tap="onSkip">跳过</view>
  </view>
</template>

<script>
import { BASE_URL } from '@/utils/request.js';

const NEXT_PAGE = {
  recommend: '/pages/figma-frame389-preview/figma-frame389-preview',
  making:    '/pages/figma-frame388-preview/figma-frame388-preview',
};

export default {
  name: "FigmaFrame391Animation",
  data() {
    return { type: 'making', hasNavigated: false };
  },
  computed: {
    videoSrc() {
      return BASE_URL + '/video/' + this.type + '.mp4';
    },
    nextPage() {
      return NEXT_PAGE[this.type] || NEXT_PAGE.making;
    },
  },
  onLoad(options) {
    if (options && options.type) {
      this.type = options.type;
    }
    console.log('[anim] type=' + this.type + ', next=' + NEXT_PAGE[this.type]);
  },
  methods: {
    onVideoEnd() {
      this.videoDone = true;
      this.goNext();
    },
    onVideoError(e) {
      console.error('[anim] video error:', e);
      this.videoDone = true;
      this.goNext();
    },
    onSkip() {
      console.log('[anim] skip clicked, navigating to', this.nextPage);
      this.goNext();
    },
    goNext() {
      if (this.hasNavigated) return;
      this.hasNavigated = true;
      uni.redirectTo({ url: this.nextPage });
    },
  },
};
</script>

<style scoped>
.frame-anim { width: 750rpx; height: 100vh; background: #000; position: relative; }
.anim-video { width: 750rpx; height: 100vh; }
.skip-btn {
  position: absolute;
  bottom: 100rpx;
  right: 30rpx;
  padding: 12rpx 32rpx;
  background: rgba(255, 255, 255, 0.2);
  color: rgba(255, 255, 255, 0.7);
  font-size: 26rpx;
  border-radius: 40rpx;
  z-index: 10;
  min-width: 80rpx;
  text-align: center;
}
</style>
