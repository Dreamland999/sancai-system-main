<template>
  <view class="frame-396">
    <!-- 白色导航栏 -->
    <view class="rectangle-1325"></view>

    <!-- 假状态栏已移除（真机系统自带） -->

    <!-- 假底部 Home Indicator 已移除（真机系统自带） -->

    <!-- 返回箭头 + 标题 -->
    <image class="right" src="/static/figma-frame396/right0.svg" />
    <view class="div-title">历史</view>
    <view class="div2">身体状况</view>

    <!-- 下一步按钮 -->
    <view class="rectangle-1292"></view>
    <view class="div3">下一步</view>

    <!-- === 身体能量 === -->
    <view class="rectangle-1335"></view>
    <view class="div4">身体能量</view>
    <view class="rectangle-12922"></view><view class="div5">睡眠不足</view>
    <view class="rectangle-12923"></view><view class="div6">午后困倦</view>
    <view class="rectangle-12924"></view><view class="div7">长期熬夜</view>
    <view class="rectangle-12925"></view><view class="div8">晨起疲劳</view>
    <view class="rectangle-12926"></view><view class="div9">精力不济</view>
    <view class="rectangle-12927"></view><view class="div10">失眠</view>
    <view class="rectangle-12928"></view><view class="div11">困倦</view>
    <view class="rectangle-12929"></view><view class="div12">嗜睡</view>
    <view class="rectangle-129210"></view><view class="div13">疲惫</view>

    <!-- === 身体疼痛 === -->
    <view class="rectangle-13352"></view>
    <view class="div14">身体疼痛</view>
    <view class="rectangle-129211"></view><view class="div15">头晕头痛</view>
    <view class="rectangle-129212"></view><view class="div16">肌肉酸痛</view>
    <view class="rectangle-129213"></view><view class="div17">腰背酸痛</view>
    <view class="rectangle-129214"></view><view class="div18">紧张性头痛</view>
    <view class="rectangle-129215"></view><view class="div19">颈源性头痛</view>
    <view class="rectangle-129216"></view><view class="div20">痛经</view>
    <view class="rectangle-129217"></view><view class="div21">关节痛</view>
    <view class="rectangle-129218"></view><view class="div22">偏头痛</view>

    <!-- === 消化敏感 === -->
    <view class="rectangle-13353"></view>
    <view class="div23">消化敏感</view>
    <view class="rectangle-129219"></view><view class="div24">乳糖不耐</view>
    <view class="rectangle-129220"></view><view class="div25">消化不良</view>
    <view class="rectangle-129221"></view><view class="div26">胃酸反流</view>
    <view class="rectangle-129222"></view><view class="div27">过敏反应：______</view>
    <view class="rectangle-129223"></view><view class="div28">胃敏感</view>
    <view class="rectangle-129224"></view><view class="div29">腹胀</view>
    <view class="rectangle-129225"></view><view class="div30">腹泻</view>
    <view class="rectangle-129226"></view><view class="div31">腹痛</view>

    <!-- === 隐私弹窗遮罩 === -->
    <view class="rectangle-1307"></view>

    <!-- === 白色弹窗 === -->
    <view class="rectangle-1308"></view>
    <view class="div32">信息采集隐私弹窗</view>
    <view class="div33">为精准识别您的身体与情绪状态，需要采集以下信息：</view>
    <view class="ai">
      <view class="ai-item">· 面部影像信息</view>
      <view class="ai-item">· 身体佩戴仪器数据</view>
      <view class="ai-item">· AI对话数据信息</view>
    </view>

    <!-- 协议勾选 -->
    <view class="group-1265" @tap="toggleCheck">
      <view class="div34">同意数据搜集所需的《隐私搜集协议》</view>
      <view class="ellipse-33" :class="{ checked: agreed }">
        <view v-if="agreed" class="check-mark">✓</view>
      </view>
    </view>

    <!-- 按钮 -->
    <view class="group-12052" @tap="onConfirm">
      <view class="rectangle-129227" :class="{ active: agreed }"></view>
      <view class="div35" :class="{ active: agreed }">确定</view>
    </view>
    <view class="group-1266" @tap="onSkip">
      <view class="rectangle-129228"></view>
      <view class="div36">跳过</view>
    </view>
  </view>
</template>

<script>
import { safeNavigateTo } from '@/utils/nav.js';

export default {
  name: "FigmaFrame396Preview",
  data() {
    return { agreed: false };
  },
  methods: {
    toggleCheck() {
      this.agreed = !this.agreed;
    },
    onSkip() {
      console.log('[Frame396] click 跳过 → Frame394');
      uni.showToast({ title: "已跳过", icon: "none" });
      setTimeout(() => {
        safeNavigateTo('/pages/figma-frame394-preview/figma-frame394-preview');
      }, 300);
    },
    onConfirm() {
      console.log('[Frame396] click 确定');
      if (!this.agreed) {
        uni.showToast({ title: "请先同意协议", icon: "none" });
      } else {
        safeNavigateTo('/pages/figma-frame398-preview/figma-frame398-preview');
      }
    },
  },
};
</script>

<style scoped>
.frame-396 {
  background: linear-gradient(179.99deg, rgba(255, 255, 255, 1) 100%);
  height: 100vh;
  position: relative;
  overflow: hidden;
}

/* ── 白色导航栏 ── */
.rectangle-1325 {
  background: #ffffff;
  width: 750rpx;
  height: 176rpx;
  position: absolute;
  left: 0;
  top: 0;
}

/* ── 状态栏 ── */
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
.time-i-phone { flex-shrink: 0; width: 108rpx; height: 42rpx; position: relative; }
.time {
  color: #000000; text-align: center;
  font-family: "SF Pro Text", sans-serif;
  font-size: 34rpx; line-height: 44rpx; font-weight: 600;
  position: absolute; left: 0; top: 50%; transform: translateY(-50%); width: 108rpx;
}
.cellular-wifi-battery-i-phone { flex-shrink: 0; width: 157rpx; height: 26rpx; position: relative; }
.battery { width: 35%; height: 100%; position: absolute; right: 0; }
.wifi { width: 34rpx; height: 24rpx; position: absolute; left: 53rpx; top: 2rpx; }
.cellular-connection { width: 38rpx; height: 24rpx; position: absolute; left: 0; top: 2rpx; }

/* ── 底部指示条 ── */
.home-indicator-i-phone { width: 780rpx; height: 38rpx; position: absolute; left: -14rpx; top: 1586rpx; }
.home-indicator { background: #000000; border-radius: 200rpx; width: 268rpx; height: 10rpx; position: absolute; left: 50%; transform: translateX(-50%); bottom: 16rpx; }

/* ── 返回箭头 + 标题 ── */
.right { width: 48rpx; height: 48rpx; position: absolute; left: 44rpx; top: 106rpx; transform: translate(-48rpx, 0); }
.div-title { color: #333333; font-size: 32rpx; font-weight: 500; position: absolute; left: 646rpx; top: 108rpx; }
.div2 { color: #333333; font-size: 32rpx; font-weight: 500; position: absolute; left: 308rpx; top: 108rpx; }

/* ── 下一步按钮 ── */
.rectangle-1292 { background: #cccccc; border-radius: 60rpx; border: 2rpx solid #ffffff; width: 440rpx; height: 80rpx; position: absolute; left: 156rpx; top: 1412rpx; }
.div3 { color: #ffffff; text-align: center; font-size: 32rpx; font-weight: 500; position: absolute; left: 328rpx; top: 1430rpx; }

/* ── 身体能量 (粉色侧边) ── */
.rectangle-1335 { background: #ff9ebe; border-radius: 100rpx; width: 120rpx; height: 260rpx; position: absolute; left: 48rpx; top: 240rpx; }
.div4 { color: #ffffff; font-family: "ZCOOL XiaoWei", serif; font-size: 40rpx; font-weight: 400; position: absolute; left: 90rpx; top: 290rpx; width: 38rpx; }

/* 标签通用 */
.tag-sm { background: rgba(85, 85, 85, 0.1); border-radius: 100rpx; border: 2rpx solid transparent; height: 48rpx; position: absolute; }
.tag-txt { color: #666666; text-align: center; font-size: 24rpx; position: absolute; }

/* 身体能量标签 */
.rectangle-12922 { background: rgba(85,85,85,0.1); border-radius: 100rpx; border: 2rpx solid transparent; width: 140rpx; height: 48rpx; position: absolute; left: 202rpx; top: 276rpx; }
.div5 { color: #666666; text-align: center; font-size: 24rpx; position: absolute; left: 224rpx; top: 282rpx; }
.rectangle-12923 { background: rgba(85,85,85,0.1); border-radius: 100rpx; border: 2rpx solid transparent; width: 140rpx; height: 48rpx; position: absolute; left: 202rpx; top: 412rpx; }
.div6 { color: #666666; text-align: center; font-size: 24rpx; position: absolute; left: 224rpx; top: 418rpx; }
.rectangle-12924 { background: rgba(85,85,85,0.1); border-radius: 100rpx; border: 2rpx solid transparent; width: 140rpx; height: 48rpx; position: absolute; left: 358rpx; top: 412rpx; }
.div7 { color: #666666; text-align: center; font-size: 24rpx; position: absolute; left: 380rpx; top: 418rpx; }
.rectangle-12925 { background: rgba(85,85,85,0.1); border-radius: 100rpx; border: 2rpx solid transparent; width: 140rpx; height: 48rpx; position: absolute; left: 358rpx; top: 276rpx; }
.div8 { color: #666666; text-align: center; font-size: 24rpx; position: absolute; left: 380rpx; top: 282rpx; }
.rectangle-12926 { background: rgba(85,85,85,0.1); border-radius: 100rpx; border: 2rpx solid transparent; width: 140rpx; height: 48rpx; position: absolute; left: 514rpx; top: 344rpx; }
.div9 { color: #666666; text-align: center; font-size: 24rpx; position: absolute; left: 536rpx; top: 350rpx; }
.rectangle-12927 { background: rgba(85,85,85,0.1); border-radius: 100rpx; border: 2rpx solid transparent; width: 88rpx; height: 48rpx; position: absolute; left: 514rpx; top: 276rpx; }
.div10 { color: #666666; text-align: center; font-size: 24rpx; position: absolute; left: 534rpx; top: 282rpx; }
.rectangle-12928 { background: rgba(85,85,85,0.1); border-radius: 100rpx; border: 2rpx solid transparent; width: 88rpx; height: 48rpx; position: absolute; left: 202rpx; top: 344rpx; }
.div11 { color: #666666; text-align: center; font-size: 24rpx; position: absolute; left: 222rpx; top: 350rpx; }
.rectangle-12929 { background: rgba(85,85,85,0.1); border-radius: 100rpx; border: 2rpx solid transparent; width: 88rpx; height: 48rpx; position: absolute; left: 306rpx; top: 344rpx; }
.div12 { color: #666666; text-align: center; font-size: 24rpx; position: absolute; left: 326rpx; top: 350rpx; }
.rectangle-129210 { background: rgba(85,85,85,0.1); border-radius: 100rpx; border: 2rpx solid transparent; width: 88rpx; height: 48rpx; position: absolute; left: 410rpx; top: 344rpx; }
.div13 { color: #666666; text-align: center; font-size: 24rpx; position: absolute; left: 430rpx; top: 350rpx; }

/* ── 身体疼痛 (绿色侧边) ── */
.rectangle-13352 { background: #bbefb0; border-radius: 100rpx; width: 120rpx; height: 260rpx; position: absolute; left: 48rpx; top: 880rpx; }
.div14 { color: #ffffff; font-family: "ZCOOL XiaoWei", serif; font-size: 40rpx; font-weight: 400; position: absolute; left: 90rpx; top: 930rpx; width: 38rpx; }
.rectangle-129211 { background: rgba(85,85,85,0.1); border-radius: 100rpx; border: 2rpx solid transparent; width: 140rpx; height: 48rpx; position: absolute; left: 202rpx; top: 916rpx; }
.div15 { color: #666666; text-align: center; font-size: 24rpx; position: absolute; left: 224rpx; top: 922rpx; }
.rectangle-129212 { background: rgba(85,85,85,0.1); border-radius: 100rpx; border: 2rpx solid transparent; width: 140rpx; height: 48rpx; position: absolute; left: 358rpx; top: 916rpx; }
.div16 { color: #666666; text-align: center; font-size: 24rpx; position: absolute; left: 380rpx; top: 922rpx; }
.rectangle-129213 { background: rgba(85,85,85,0.1); border-radius: 100rpx; border: 2rpx solid transparent; width: 140rpx; height: 48rpx; position: absolute; left: 474rpx; top: 984rpx; }
.div17 { color: #666666; text-align: center; font-size: 24rpx; position: absolute; left: 496rpx; top: 990rpx; }
.rectangle-129214 { background: rgba(85,85,85,0.1); border-radius: 100rpx; border: 2rpx solid transparent; width: 164rpx; height: 48rpx; position: absolute; left: 202rpx; top: 1052rpx; }
.div18 { color: #666666; text-align: center; font-size: 24rpx; position: absolute; left: 224rpx; top: 1058rpx; }
.rectangle-129215 { background: rgba(85,85,85,0.1); border-radius: 100rpx; border: 2rpx solid transparent; width: 164rpx; height: 48rpx; position: absolute; left: 382rpx; top: 1052rpx; }
.div19 { color: #666666; text-align: center; font-size: 24rpx; position: absolute; left: 404rpx; top: 1058rpx; }
.rectangle-129216 { background: rgba(85,85,85,0.1); border-radius: 100rpx; border: 2rpx solid transparent; width: 88rpx; height: 48rpx; position: absolute; left: 514rpx; top: 916rpx; }
.div20 { color: #666666; text-align: center; font-size: 24rpx; position: absolute; left: 534rpx; top: 922rpx; }
.rectangle-129217 { background: rgba(85,85,85,0.1); border-radius: 100rpx; border: 2rpx solid transparent; width: 120rpx; height: 48rpx; position: absolute; left: 202rpx; top: 984rpx; }
.div21 { color: #666666; text-align: center; font-size: 24rpx; position: absolute; left: 226rpx; top: 990rpx; }
.rectangle-129218 { background: rgba(85,85,85,0.1); border-radius: 100rpx; border: 2rpx solid transparent; width: 120rpx; height: 48rpx; position: absolute; left: 338rpx; top: 984rpx; }
.div22 { color: #666666; text-align: center; font-size: 24rpx; position: absolute; left: 362rpx; top: 990rpx; }

/* ── 消化敏感 (橙色侧边) ── */
.rectangle-13353 { background: rgba(246, 133, 80, 0.6); border-radius: 100rpx; width: 120rpx; height: 260rpx; position: absolute; left: 170rpx; top: 564rpx; transform: rotate(0deg); }
.div23 { color: #ffffff; font-family: "ZCOOL XiaoWei", serif; font-size: 40rpx; font-weight: 400; position: absolute; left: 90rpx; top: 614rpx; width: 38rpx; }
.rectangle-129219 { background: rgba(85,85,85,0.1); border-radius: 20rpx; border: 2rpx solid transparent; width: 140rpx; height: 48rpx; position: absolute; left: 202rpx; top: 604rpx; }
.div24 { color: #666666; text-align: center; font-size: 24rpx; position: absolute; left: 224rpx; top: 610rpx; }
.rectangle-129220 { background: rgba(85,85,85,0.1); border-radius: 20rpx; border: 2rpx solid transparent; width: 140rpx; height: 48rpx; position: absolute; left: 494rpx; top: 604rpx; }
.div25 { color: #666666; text-align: center; font-size: 24rpx; position: absolute; left: 516rpx; top: 610rpx; }
.rectangle-129221 { background: rgba(85,85,85,0.1); border-radius: 20rpx; border: 2rpx solid transparent; width: 140rpx; height: 48rpx; position: absolute; left: 202rpx; top: 670rpx; }
.div26 { color: #666666; text-align: center; font-size: 24rpx; position: absolute; left: 224rpx; top: 676rpx; }
.rectangle-129222 { background: rgba(85,85,85,0.1); border-radius: 40rpx; border: 2rpx solid #999999; width: 32rpx; height: 32rpx; position: absolute; left: 202rpx; top: 746rpx; }
.div27 { color: #666666; font-size: 24rpx; position: absolute; left: 246rpx; top: 744rpx; }
.rectangle-129223 { background: rgba(85,85,85,0.1); border-radius: 20rpx; border: 2rpx solid transparent; width: 120rpx; height: 48rpx; position: absolute; left: 358rpx; top: 604rpx; }
.div28 { color: #666666; text-align: center; font-size: 24rpx; position: absolute; left: 382rpx; top: 610rpx; }
.rectangle-129224 { background: rgba(85,85,85,0.1); border-radius: 20rpx; border: 2rpx solid transparent; width: 88rpx; height: 48rpx; position: absolute; left: 358rpx; top: 670rpx; }
.div29 { color: #666666; text-align: center; font-size: 24rpx; position: absolute; left: 378rpx; top: 676rpx; }
.rectangle-129225 { background: rgba(85,85,85,0.1); border-radius: 20rpx; border: 2rpx solid transparent; width: 88rpx; height: 48rpx; position: absolute; left: 462rpx; top: 670rpx; }
.div30 { color: #666666; text-align: center; font-size: 24rpx; position: absolute; left: 482rpx; top: 676rpx; }
.rectangle-129226 { background: rgba(85,85,85,0.1); border-radius: 20rpx; border: 2rpx solid transparent; width: 88rpx; height: 48rpx; position: absolute; left: 566rpx; top: 670rpx; }
.div31 { color: #666666; text-align: center; font-size: 24rpx; position: absolute; left: 586rpx; top: 676rpx; }

/* ── 隐私弹窗遮罩 ── */
.rectangle-1307 { background: rgba(0, 0, 0, 0.2); width: 750rpx; height: 1624rpx; position: absolute; left: 0; top: 0; }

/* ── 白色弹窗 ── */
.rectangle-1308 { background: #ffffff; border-radius: 16rpx; width: 560rpx; height: 566rpx; position: absolute; left: 96rpx; top: 530rpx; }
.div32 { color: #000000; text-align: center; font-size: 32rpx; font-weight: 500; position: absolute; left: 238rpx; top: 558rpx; }
.div33 { color: #333333; font-size: 28rpx; font-weight: 500; position: absolute; left: 132rpx; top: 626rpx; width: 490rpx; }
.ai { color: #666666; font-size: 28rpx; line-height: 150%; position: absolute; left: 156rpx; top: 734rpx; width: 490rpx; }
.ai-item { margin-bottom: 4rpx; }

/* 协议勾选 */
.group-1265 { position: absolute; left: 156rpx; top: 916rpx; width: 458rpx; height: 34rpx; }
.div34 { color: #333333; font-size: 24rpx; font-weight: 300; position: absolute; left: 38rpx; top: 0; width: 420rpx; }
.ellipse-33 { border-radius: 50%; border: 2rpx solid #666666; width: 26rpx; height: 26rpx; position: absolute; left: 0; top: 4rpx; display: flex; align-items: center; justify-content: center; }
.ellipse-33.checked { border-color: #85d2c7; background: #85d2c7; }
.check-mark { color: #ffffff; font-size: 18rpx; }

/* 按钮 */
.group-12052 { position: absolute; left: 386rpx; top: 986rpx; width: 204rpx; height: 56rpx; }
.rectangle-129227 { background: #cccccc; border-radius: 42rpx; border: 2rpx solid transparent; width: 204rpx; height: 56rpx; }
.rectangle-129227.active { background: #85d2c7; }
.div35 { color: #ffffff; font-size: 28rpx; font-weight: 500; position: absolute; left: 74rpx; top: 10rpx; }
.div35.active { color: #ffffff; }

.group-1266 { position: absolute; left: 152rpx; top: 986rpx; width: 204rpx; height: 56rpx; }
.rectangle-129228 { background: #ffffff; border-radius: 42rpx; border: 2rpx solid #85d2c7; width: 204rpx; height: 56rpx; }
.div36 { color: #85d2c7; font-size: 28rpx; font-weight: 500; position: absolute; left: 74rpx; top: 10rpx; }
</style>
