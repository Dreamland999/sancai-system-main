<template>
  <view class="frame-398">
    <!-- 白色导航栏 -->
    <view class="nav-bg"></view>

    <!-- 假状态栏已移除（真机系统自带） -->

    <!-- 假底部 Home Indicator 已移除（真机系统自带） -->

    <!-- 返回 + 标题 -->
    <view class="back-hit" @tap="onBack">
      <image class="ico-back" src="/static/figma-frame398/right0.svg" />
    </view>
    <view class="txt-title">实时了解</view>
    <view class="txt-history" @tap="onHistory">历史</view>

    <!-- 面部信息识别 -->
    <view class="txt-face-title">面部信息识别</view>
    <view class="txt-face-hint">请确认您的面容完全放置在圆框内~</view>

    <!-- 摄像头预览区 -->
    <camera
      v-if="showCamera"
      class="face-camera"
      device-position="front"
      flash="off"
      @initdone="onCameraInit"
      @error="onCameraError"
    />
    <!-- 摄像头不可用时的占位图 -->
    <image v-else class="face-img" src="/static/figma-frame398/ellipse-340.png" mode="aspectFill" />

    <!-- 圆形边框覆盖层 -->
    <image class="circle-border" src="/static/figma-frame398/div8.svg" />

    <!-- 仪器信息识别 -->
    <view class="txt-device-title">仪器信息识别</view>
    <image class="ico-bluetooth" src="/static/figma-frame398/bluetooth0.svg" />
    <view class="txt-device-name">手臂穿戴设备</view>
    <view class="txt-device-id">LP：2246：325667</view>
    <view class="btn-disconnect" @tap="onDisconnect"><view class="txt-disconnect">断连</view></view>
    <view class="btn-add" @tap="onAdd"><image class="ico-plus" src="/static/figma-frame398/plus0.svg" /></view>

    <!-- 开始识别 -->
    <view class="btn-start" :class="{ 'btn-start-disabled': recognizing }" @tap="onStart">
      <view class="txt-start">{{ recognizing ? '识别中...' : '开始识别' }}</view>
    </view>
  </view>
</template>

<script>
import { goBack } from '@/utils/nav.js';
import { predictEmotion } from '@/api/emotion.js';

const EMOTION_TO_MOOD = {
  happy: '开心',
  neutral: '平静',
  sad: '低落',
  angry: '烦躁',
  fearful: '紧张'
};

function getDefaultInput() {
  return {
    scene: [],
    body: [],
    mood: [],
    needs: [],
    limits: [],
    flavor_preference: [],
    temperature_preference: []
  };
}

function mapEmotionToRecommendInput(result) {
  // 摄像头识别总是基于干净默认值，不继承旧 input
  const input = getDefaultInput();

  const moodTag = EMOTION_TO_MOOD[result.emotion];
  if (moodTag) {
    input.mood = [moodTag];
  }
  // unknown/disgust/surprised → mood 保持空

  uni.setStorageSync('recommend_input', input);
  console.log('[Frame398] recommend_input after emotion (clean)', JSON.stringify(input));
  return input;
}

export default {
  name: "FigmaFrame398Preview",
  data() {
    return {
      cameraReady: false,
      cameraError: '',
      recognizing: false,
      showCamera: true
    };
  },
  mounted() {
    // #ifdef MP-WEIXIN
    try {
      this.cameraCtx = uni.createCameraContext();
    } catch (e) {
      console.log('[Frame398] createCameraContext failed, will fallback to chooseImage');
    }
    // #endif
  },
  methods: {
    onBack() {
      goBack();
    },
    onHistory() {
      uni.showToast({ title: "历史", icon: "none" });
    },
    onDisconnect() {
      uni.showToast({ title: "已断连", icon: "none" });
    },
    onAdd() {
      uni.showToast({ title: "添加设备", icon: "none" });
    },
    onCameraInit(e) {
      console.log('[Frame398] camera init done', e);
      this.cameraReady = true;
      this.cameraError = '';
    },
    onCameraError(e) {
      console.error('[Frame398] camera error', e);
      this.cameraReady = false;
      this.cameraError = e.detail ? e.detail.errMsg : '相机初始化失败';
      this.showCamera = false;
      uni.showToast({ title: '摄像头不可用，可从相册选择', icon: 'none' });
    },
    async onStart() {
      if (this.recognizing) return;
      this.recognizing = true;

      // 1. 拍照
      let tempFilePath;
      try {
        tempFilePath = await this.captureImage();
        if (!tempFilePath) {
          this.recognizing = false;
          return;
        }
      } catch (e) {
        console.log('[Frame398] capture cancelled', e);
        this.recognizing = false;
        uni.showToast({ title: '已取消识别，可手动选择', icon: 'none' });
        uni.navigateTo({ url: '/pages/figma-frame394-preview/figma-frame394-preview' });
        return;
      }

      // 2. 上传识别
      uni.showLoading({ title: '识别中...' });
      try {
        const result = await predictEmotion(tempFilePath);
        uni.hideLoading();
        this.recognizing = false;

        uni.setStorageSync('emotion_result', result);
        console.log('[Frame398] emotion_result saved', result);

        if (result.emotion && result.emotion !== 'unknown') {
          mapEmotionToRecommendInput(result);
          uni.setStorageSync('recognition_flow', true);
          const cn = EMOTION_TO_MOOD[result.emotion] || result.emotion_cn;
          uni.showToast({ title: '识别到：' + cn, icon: 'none' });
          setTimeout(() => {
            uni.navigateTo({ url: '/pages/figma-frame382-preview/figma-frame382-preview' });
          }, 800);
        } else {
          uni.showToast({ title: '暂未识别到明确情绪，可手动选择', icon: 'none' });
          setTimeout(() => {
            uni.navigateTo({ url: '/pages/figma-frame394-preview/figma-frame394-preview' });
          }, 1200);
        }
      } catch (e) {
        uni.hideLoading();
        this.recognizing = false;
        console.error('[Frame398] emotion predict failed:', e);
        uni.showToast({ title: '识别未成功，可手动选择', icon: 'none' });
        setTimeout(() => {
          uni.navigateTo({ url: '/pages/figma-frame394-preview/figma-frame394-preview' });
        }, 1200);
      }
    },

    /** 拍照：优先用 camera.takePhoto，失败 fallback 到 chooseImage */
    async captureImage() {
      // try camera first
      if (this.cameraReady && this.cameraCtx) {
        try {
          const res = await new Promise((resolve, reject) => {
            this.cameraCtx.takePhoto({
              quality: 'normal',
              success: resolve,
              fail: reject
            });
          });
          console.log('[Frame398] camera takePhoto success:', res.tempImagePath);
          return res.tempImagePath;
        } catch (e) {
          console.error('[Frame398] takePhoto failed, fallback to chooseImage:', e);
          // fallback to chooseImage below
        }
      }

      // fallback: choose from album/camera
      try {
        const res = await new Promise((resolve, reject) => {
          uni.chooseImage({
            count: 1,
            sourceType: ['album', 'camera'],
            success: resolve,
            fail: reject
          });
        });
        if (res.tempFilePaths && res.tempFilePaths.length) {
          return res.tempFilePaths[0];
        }
      } catch (e) {
        return null;
      }
      return null;
    }
  }
};
</script>

<style scoped>
.frame-398 { background: #ffffff; height: 100vh; position: relative; overflow: hidden; }

/* nav */
.nav-bg { background: #ffffff; width: 750rpx; height: 176rpx; position: absolute; left: 0; top: 0; }

/* status bar */
.status-bar { padding: 36rpx 50rpx 28rpx 52rpx; display: flex; flex-direction: row; align-items: center; justify-content: space-between; width: 750rpx; position: absolute; left: 0; top: 0; }
.time-wrap { flex-shrink: 0; width: 108rpx; height: 42rpx; position: relative; }
.time { color: #000; text-align: center; font-family: "SF Pro Text", sans-serif; font-size: 34rpx; font-weight: 600; position: absolute; left: 0; top: 50%; transform: translateY(-50%); width: 108rpx; }
.icons-wrap { flex-shrink: 0; width: 156rpx; height: 26rpx; position: relative; }
.icon-cellular { width: 38rpx; height: 24rpx; position: absolute; left: 0; top: 2rpx; }
.icon-wifi { width: 34rpx; height: 24rpx; position: absolute; left: 54rpx; top: 2rpx; }
.icon-battery { width: 56rpx; height: 26rpx; position: absolute; right: 0; top: 0; }

/* home indicator */
.home-bar { width: 750rpx; height: 38rpx; position: absolute; left: 0; top: 1586rpx; }
.home-bar-inner { background: #000; border-radius: 192rpx; width: 268rpx; height: 10rpx; position: absolute; left: 50%; transform: translateX(-50%); bottom: 16rpx; }

/* nav content */
.back-hit { position: absolute; left: 4rpx; top: 90rpx; width: 80rpx; height: 80rpx; z-index: 10; display: flex; align-items: center; justify-content: center; }
.ico-back { width: 48rpx; height: 48rpx; }
.txt-title { color: #333; font-size: 32rpx; font-weight: 500; position: absolute; left: 308rpx; top: 108rpx; }
.txt-history { color: #333; font-size: 32rpx; font-weight: 500; position: absolute; left: 646rpx; top: 108rpx; }

/* face section */
.txt-face-title { color: #333; text-align: center; font-size: 32rpx; font-weight: 500; position: absolute; left: 60rpx; top: 224rpx; z-index: 5; }
.txt-face-hint { color: #666; text-align: center; font-size: 28rpx; position: absolute; left: 158rpx; top: 308rpx; z-index: 5; }

/* 摄像头预览 — 替换原静态 face-img 区域 */
.face-camera {
  position: absolute;
  left: 116rpx;
  top: 418rpx;
  width: 518rpx;
  height: 518rpx;
  z-index: 1;
}

/* 摄像头不可用时的占位图 */
.face-img {
  border-radius: 50%;
  border: 2rpx solid #85d2c7;
  width: 518rpx;
  height: 518rpx;
  position: absolute;
  left: 116rpx;
  top: 418rpx;
  z-index: 1;
}

/* 圆形边框 — 覆盖在摄像头上面 */
.circle-border {
  width: 616rpx;
  height: 616rpx;
  position: absolute;
  left: 68rpx;
  top: 368rpx;
  z-index: 3;
  pointer-events: none;
}

/* device section */
.txt-device-title { color: #333; font-size: 32rpx; font-weight: 500; position: absolute; left: 60rpx; top: 1042rpx; }
.ico-bluetooth { width: 64rpx; height: 64rpx; position: absolute; left: 58rpx; top: 1150rpx; }
.txt-device-name { color: #85d2c7; font-size: 28rpx; font-weight: 500; position: absolute; left: 156rpx; top: 1144rpx; }
.txt-device-id { color: #ccc; font-size: 24rpx; font-weight: 500; position: absolute; left: 156rpx; top: 1184rpx; }
.btn-disconnect { background: rgba(133,210,199,0.2); border-radius: 8rpx; border: 2rpx solid #85d2c7; width: 120rpx; height: 48rpx; position: absolute; left: 570rpx; top: 1158rpx; display: flex; align-items: center; justify-content: center; }
.txt-disconnect { color: #85d2c7; font-size: 28rpx; font-weight: 500; }
.btn-add { background: #85d2c7; border-radius: 8rpx; width: 64rpx; height: 64rpx; position: absolute; left: 58rpx; top: 1250rpx; display: flex; align-items: center; justify-content: center; }
.ico-plus { width: 60rpx; height: 60rpx; }

/* start button */
.btn-start { background: #56bfb0; border-radius: 64rpx; border: 2rpx solid #fff; width: 440rpx; height: 80rpx; position: absolute; left: 156rpx; top: 1412rpx; display: flex; align-items: center; justify-content: center; }
.btn-start-disabled { opacity: 0.6; }
.txt-start { color: #fff; font-size: 32rpx; font-weight: 500; }
</style>
