<template>
  <view class="frame-400">
    <image class="image-17" src="/static/figma-home/image-170.png" mode="aspectFill" />
    <image class="image-18" src="/static/figma-home/image-180.png" mode="aspectFill" />
    <view class="ellipse-39"></view>
    <view class="ellipse-3"></view>
    <view class="ellipse-2"></view>
    <image
      class="b-8-b-9-a-543-d-10-f-48-fafb-88-aa-0-fb-39-d-4987-1"
      src="/static/figma-home/b-8-b-9-a-543-d-10-f-48-fafb-88-aa-0-fb-39-d-4987-10.png"
      mode="aspectFill"
    />

    <!-- 假状态栏已移除（真机系统自带） -->

    <!-- 假底部 Home Indicator 已移除（真机系统自带） -->

    <!-- 诗句 -->
    <view class="div3">
      山下兰芽短浸溪
      <br />
      <br />
    </view>
    <view class="div4">
      松间沙路净无泥
      <br />
      <br />
      潇潇暮雨子规啼
    </view>

    <!-- 天气/位置 -->
    <image class="local" src="/static/figma-home/local0.svg" />
    <view class="div5">华南理工大学…</view>
    <image class="right" src="/static/figma-home/right0.svg" />
    <image class="shade" src="/static/figma-home/shade0.svg" />
    <view class="div6">中雨</view>
    <image class="me" src="/static/figma-home/me0.svg" />

    <!-- 底部入口热区 -->
    <view class="hit-foodlib" @tap="onTapFoodLib">食材库</view>
    <view class="hit-recipelib" @tap="onTapRecipeLib">配方库</view>
    <view class="hit-make" @tap="onTapMake">制作</view>

    <!-- 底部装饰 -->
    <view class="ellipse-32"></view>
    <view class="ellipse-22"></view>
    <image class="leaves" src="/static/figma-home/leaves0.svg" />
    <view class="ellipse-33"></view>
    <view class="ellipse-23"></view>
    <image class="intersect-selection" src="/static/figma-home/intersect-selection0.svg" />
  </view>
</template>

<script>
import { safeNavigateTo } from '@/utils/nav.js';
import { resetRecommendSession } from '@/utils/session.js';

export default {
  name: "FigmaHomePreview",
  methods: {
    onTapFoodLib() {
      console.log('[Frame400] click 食材库');
      safeNavigateTo('/pages/figma-frame384-preview/figma-frame384-preview');
    },
    onTapMake() {
      console.log('[Frame400] click 制作');
      resetRecommendSession();
      safeNavigateTo('/pages/figma-frame396-preview/figma-frame396-preview');
    },
    onTapRecipeLib() {
      console.log('[Frame400] click 配方库');
      uni.showToast({ title: '配方库待补', icon: 'none' });
    },
  },
};
</script>

<style scoped>
.frame-400 {
  background: linear-gradient(
    175.98deg,
    rgba(147, 219, 213, 1) 0%,
    rgba(255, 255, 255, 1) 85.1%
  );
  height: 100vh;
  /* 812px * 2 */
  position: relative;
  overflow: hidden;
}

/* ── 背景装饰图 ── */
.image-17 {
  width: 2004rpx;
  height: 1224rpx;
  position: absolute;
  left: -1238rpx;
  top: -120rpx;
  pointer-events: none;
}
.image-18 {
  width: 2004rpx;
  height: 1224rpx;
  position: absolute;
  left: -1060rpx;
  top: 658rpx;
  pointer-events: none;
}

/* ── 底部模糊圆 ── */
.ellipse-39 {
  border-radius: 50%;
  width: 548rpx;
  height: 548rpx;
  position: absolute;
  left: 2rpx;
  top: 1530rpx;
  }

/* ── 制作按钮圆形背景 ── */
.ellipse-3 {
  background: #ffffff;
  border-radius: 50%;
  width: 192rpx;
  height: 192rpx;
  position: absolute;
  left: 280rpx;
  top: 1242rpx;
}
.ellipse-2 {
  background: rgba(122, 233, 217, 0.8);
  border-radius: 50%;
  width: 144rpx;
  height: 144rpx;
  position: absolute;
  left: 304rpx;
  top: 1266rpx;
  }
.b-8-b-9-a-543-d-10-f-48-fafb-88-aa-0-fb-39-d-4987-1 {
  width: 112rpx;
  height: 112rpx;
  position: absolute;
  left: 320rpx;
  top: 1282rpx;
}

/* ── 文字（保留样式但不再绑事件，仅作展示）── */
.div {
  color: #666666;
  text-align: left;
  font-family: "PingFang SC", sans-serif;
  font-size: 28rpx;
  font-weight: 400;
  position: absolute;
  left: 102rpx;
  top: 1470rpx;
  pointer-events: none;
}
.div2 {
  color: #666666;
  text-align: left;
  font-family: "PingFang SC", sans-serif;
  font-size: 28rpx;
  font-weight: 400;
  position: absolute;
  left: 568rpx;
  top: 1470rpx;
  pointer-events: none;
}

/* ── 状态栏 (Figma 对照) ── */
.status-bar-i-phone {
  padding: 36rpx 52rpx 28rpx 54rpx;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  width: 780rpx;
  position: absolute;
  left: -14rpx;
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
  line-height: 44rpx;
  font-weight: 600;
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 108rpx;
}
.cellular-wifi-battery-i-phone {
  flex-shrink: 0;
  width: 157rpx;
  height: 26rpx;
  position: relative;
}
.battery {
  width: 35%;
  height: 100%;
  position: absolute;
  right: 0;
}
.wifi {
  width: 34rpx;
  height: 24rpx;
  position: absolute;
  left: 53rpx;
  top: 2rpx;
}
.cellular-connection {
  width: 38rpx;
  height: 24rpx;
  position: absolute;
  left: 0;
  top: 2rpx;
}

/* ── 底部指示条 ── */
.home-indicator-i-phone {
  width: 780rpx;
  height: 38rpx;
  position: absolute;
  left: -14rpx;
  top: 1586rpx;
}
.home-indicator {
  background: #000000;
  border-radius: 200rpx;
  width: 268rpx;
  height: 10rpx;
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  bottom: 16rpx;
}

/* ── 诗句 ── */
.div3 {
  color: #ffffff;
  text-align: left;
  font-family: "ZCOOL XiaoWei", "ZcoolXiaoWei-Regular", serif;
  font-size: 48rpx;
  font-weight: 400;
  position: absolute;
  left: 578rpx;
  top: 226rpx;
  width: 70rpx;
}
.div4 {
  color: #ffffff;
  text-align: left;
  font-family: "ZCOOL XiaoWei", "ZcoolXiaoWei-Regular", serif;
  font-size: 48rpx;
  font-weight: 400;
  position: absolute;
  left: 648rpx;
  top: 226rpx;
  width: 70rpx;
}

/* ── 天气/位置 ── */
.local {
  width: 48rpx;
  height: 48rpx;
  position: absolute;
  left: 40rpx;
  top: 114rpx;
}
.div5 {
  color: #ffffff;
  text-align: left;
  font-family: "PingFang SC", sans-serif;
  font-size: 28rpx;
  font-weight: 400;
  position: absolute;
  left: 110rpx;
  top: 118rpx;
}
.right {
  width: 40rpx;
  height: 40rpx;
  position: absolute;
  left: 302rpx;
  top: 118rpx;
}
.shade {
  width: 48rpx;
  height: 48rpx;
  position: absolute;
  left: 582rpx;
  top: 110rpx;
}
.div6 {
  color: #ffffff;
  text-align: left;
  font-family: "PingFang SC", sans-serif;
  font-size: 28rpx;
  font-weight: 400;
  position: absolute;
  left: 516rpx;
  top: 116rpx;
}
.me {
  width: 48rpx;
  height: 48rpx;
  position: absolute;
  left: 662rpx;
  top: 110rpx;
}

/* ── 制作（原文字保留样式但仅作展示）── */
.div7 {
  color: #666666;
  text-align: left;
  font-family: "PingFang SC", sans-serif;
  font-size: 28rpx;
  font-weight: 500;
  position: absolute;
  left: 348rpx;
  top: 1470rpx;
  pointer-events: none;
}

/* ── 入口点击热区 ── */
.hit-foodlib {
  position: absolute;
  left: 56rpx;
  top: 1320rpx;
  width: 200rpx;
  height: 200rpx;
  z-index: 10;
  color: transparent;
}
.hit-recipelib {
  position: absolute;
  left: 522rpx;
  top: 1320rpx;
  width: 200rpx;
  height: 200rpx;
  z-index: 10;
  color: transparent;
}
.hit-make {
  position: absolute;
  left: 260rpx;
  top: 1222rpx;
  width: 232rpx;
  height: 280rpx;
  z-index: 10;
  color: transparent;
}

/* ── 底部图标 ── */
.ellipse-32 {
  background: #ffffff;
  border-radius: 50%;
  width: 112rpx;
  height: 112rpx;
  position: absolute;
  left: 86rpx;
  top: 1342rpx;
}
.ellipse-22 {
  background: rgba(149, 232, 220, 0.6);
  border-radius: 50%;
  width: 80rpx;
  height: 80rpx;
  position: absolute;
  left: 102rpx;
  top: 1358rpx;
  }
.leaves {
  width: 48rpx;
  height: 48rpx;
  position: absolute;
  left: 118rpx;
  top: 1374rpx;
}
.ellipse-33 {
  background: #ffffff;
  border-radius: 50%;
  width: 112rpx;
  height: 112rpx;
  position: absolute;
  left: 552rpx;
  top: 1342rpx;
}
.ellipse-23 {
  background: rgba(149, 232, 220, 0.6);
  border-radius: 50%;
  width: 80rpx;
  height: 80rpx;
  position: absolute;
  left: 568rpx;
  top: 1358rpx;
  }
.intersect-selection {
  width: 48rpx;
  height: 48rpx;
  position: absolute;
  left: 584rpx;
  top: 1374rpx;
}
</style>
