<template>
  <view class="frame-396">
    <view class="rectangle-1325"></view>

    <!-- 假状态栏已移除（真机系统自带） -->

    <!-- 假底部 Home Indicator 已移除（真机系统自带） -->

    <!-- 导航 -->
    <image class="right" src="/static/figma-home/right0.svg" />
    <view class="nav-history">历史</view>
    <view class="nav-body">身体状况</view>

    <!-- 下一步 -->
    <view class="rect-next"></view>
    <view class="text-next">下一步</view>

    <!-- 左侧色条：身体能量 -->
    <view class="bar-energy"></view>
    <view class="label-energy">身<br />体<br />能<br />量</view>

    <!-- 身体能量标签 -->
    <view class="tag tag-1"><view class="tag-text">睡眠不足</view></view>
    <view class="tag tag-2"><view class="tag-text">午后困倦</view></view>
    <view class="tag tag-3"><view class="tag-text">长期熬夜</view></view>
    <view class="tag tag-4"><view class="tag-text">晨起疲劳</view></view>
    <view class="tag tag-5"><view class="tag-text">精力不济</view></view>
    <view class="tag tag-6"><view class="tag-text">失眠</view></view>
    <view class="tag tag-7"><view class="tag-text">困倦</view></view>
    <view class="tag tag-8"><view class="tag-text">嗜睡</view></view>
    <view class="tag tag-9"><view class="tag-text">疲惫</view></view>

    <!-- 左侧色条：身体疼痛 -->
    <view class="bar-pain"></view>
    <view class="label-pain">身<br />体<br />疼<br />痛</view>

    <!-- 身体疼痛标签 -->
    <view class="tag tag-10"><view class="tag-text">头晕头痛</view></view>
    <view class="tag tag-11"><view class="tag-text">肌肉酸痛</view></view>
    <view class="tag tag-12"><view class="tag-text">腰背酸痛</view></view>
    <view class="tag tag-13"><view class="tag-text">紧张性头痛</view></view>
    <view class="tag tag-14"><view class="tag-text">颈源性头痛</view></view>
    <view class="tag tag-15"><view class="tag-text">痛经</view></view>
    <view class="tag tag-16"><view class="tag-text">关节痛</view></view>
    <view class="tag tag-17"><view class="tag-text">偏头痛</view></view>

    <!-- 左侧色条：消化敏感 -->
    <view class="bar-digest"></view>
    <view class="label-digest">消<br />化<br />敏<br />感</view>

    <!-- 消化敏感标签 -->
    <view class="tag tag-18"><view class="tag-text">乳糖不耐</view></view>
    <view class="tag tag-19"><view class="tag-text">消化不良</view></view>
    <view class="tag tag-20"><view class="tag-text">胃酸反流</view></view>
    <view class="tag tag-21"><view class="tag-text">胃敏感</view></view>
    <view class="tag tag-22"><view class="tag-text">腹胀</view></view>
    <view class="tag tag-23"><view class="tag-text">腹泻</view></view>
    <view class="tag tag-24"><view class="tag-text">腹痛</view></view>

    <!-- 过敏勾选 -->
    <view class="check-allergy"></view>
    <view class="text-allergy">过敏反应：______</view>

    <!-- ── 隐私弹窗遮罩 ── -->
    <view class="overlay"></view>
    <view class="modal-bg"></view>
    <view class="modal-title">信息采集隐私弹窗</view>
    <view class="modal-desc">为精准识别您的身体与情绪状态，需要采集以下信息：</view>
    <view class="modal-list">
      <view class="modal-item">面部影像信息</view>
      <view class="modal-item" style="top:44rpx">身体佩戴仪器数据</view>
      <view class="modal-item" style="top:88rpx">AI对话数据信息</view>
    </view>
    <view class="modal-check">
      <view class="modal-checkbox"></view>
      <view class="modal-agree-text">同意数据搜集所需的《隐私搜集协议》</view>
    </view>
    <view class="modal-btn-confirm">
      <view class="modal-btn-text">确定</view>
    </view>
    <view class="modal-btn-skip">
      <view class="modal-btn-skip-text">跳过</view>
    </view>
  </view>
</template>

<script>
export default {
  name: "FigmaBodySurvey",
  methods: {
    onTagTap(label) {
      uni.showToast({ title: label, icon: "none" });
    },
  },
};
</script>

<style scoped>
.frame-396 {
  background: #ffffff;
  height: 1624rpx;
  position: relative;
  overflow: hidden;
}
.rectangle-1325 {
  background: #ffffff;
  width: 750rpx;
  height: 176rpx;
  position: absolute;
  left: 0;
  top: 0;
}

/* 状态栏 */
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

/* 底部指示条 */
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

/* 导航 */
.right {
  width: 48rpx;
  height: 48rpx;
  position: absolute;
  left: 44rpx;
  top: 106rpx;
  transform: translate(-48rpx, 0);
}
.nav-history {
  color: #333333;
  font-size: 32rpx;
  font-weight: 500;
  position: absolute;
  left: 646rpx;
  top: 108rpx;
}
.nav-body {
  color: #333333;
  font-size: 32rpx;
  font-weight: 500;
  position: absolute;
  left: 308rpx;
  top: 108rpx;
}

/* 下一步按钮 */
.rect-next {
  background: #cccccc;
  border-radius: 60rpx;
  border: 2rpx solid #ffffff;
  width: 440rpx;
  height: 80rpx;
  position: absolute;
  left: 156rpx;
  top: 1412rpx;
}
.text-next {
  color: #ffffff;
  text-align: center;
  font-size: 32rpx;
  font-weight: 500;
  position: absolute;
  left: 328rpx;
  top: 1430rpx;
}

/* 左侧色条 */
.bar-energy {
  background: #ff9ebe;
  border-radius: 100rpx;
  width: 120rpx;
  height: 260rpx;
  position: absolute;
  left: 48rpx;
  top: 240rpx;
}
.label-energy {
  color: #ffffff;
  font-family: "ZCOOL XiaoWei", serif;
  font-size: 40rpx;
  line-height: 1.5;
  position: absolute;
  left: 90rpx;
  top: 290rpx;
  width: 38rpx;
}
.bar-pain {
  background: #bbefb0;
  border-radius: 100rpx;
  width: 120rpx;
  height: 260rpx;
  position: absolute;
  left: 48rpx;
  top: 880rpx;
}
.label-pain {
  color: #ffffff;
  font-family: "ZCOOL XiaoWei", serif;
  font-size: 40rpx;
  line-height: 1.5;
  position: absolute;
  left: 90rpx;
  top: 930rpx;
  width: 38rpx;
}
.bar-digest {
  background: rgba(246, 133, 80, 0.6);
  border-radius: 100rpx;
  width: 120rpx;
  height: 260rpx;
  position: absolute;
  left: 170rpx;
  top: 564rpx;
}
.label-digest {
  color: #ffffff;
  font-family: "ZCOOL XiaoWei", serif;
  font-size: 40rpx;
  line-height: 1.5;
  position: absolute;
  left: 90rpx;
  top: 614rpx;
  width: 38rpx;
}

/* 标签通用 */
.tag {
  background: rgba(85, 85, 85, 0.1);
  border-radius: 100rpx;
  border: 2rpx solid transparent;
  position: absolute;
  display: flex;
  align-items: center;
  justify-content: center;
}
.tag-text {
  color: #666666;
  font-size: 24rpx;
  text-align: center;
}

/* 身体能量标签 */
.tag-1 { width:140rpx; height:48rpx; left:202rpx; top:276rpx; }
.tag-2 { width:140rpx; height:48rpx; left:202rpx; top:412rpx; }
.tag-3 { width:140rpx; height:48rpx; left:358rpx; top:412rpx; }
.tag-4 { width:140rpx; height:48rpx; left:358rpx; top:276rpx; }
.tag-5 { width:140rpx; height:48rpx; left:514rpx; top:344rpx; }
.tag-6 { width:88rpx;  height:48rpx; left:514rpx; top:276rpx; }
.tag-7 { width:88rpx;  height:48rpx; left:202rpx; top:344rpx; }
.tag-8 { width:88rpx;  height:48rpx; left:306rpx; top:344rpx; }
.tag-9 { width:88rpx;  height:48rpx; left:410rpx; top:344rpx; }

/* 身体疼痛标签 */
.tag-10 { width:140rpx; height:48rpx; left:202rpx; top:916rpx; }
.tag-11 { width:140rpx; height:48rpx; left:358rpx; top:916rpx; }
.tag-12 { width:140rpx; height:48rpx; left:474rpx; top:984rpx; }
.tag-13 { width:164rpx; height:48rpx; left:202rpx; top:1052rpx; }
.tag-14 { width:164rpx; height:48rpx; left:382rpx; top:1052rpx; }
.tag-15 { width:88rpx;  height:48rpx; left:514rpx; top:916rpx; }
.tag-16 { width:120rpx; height:48rpx; left:202rpx; top:984rpx; }
.tag-17 { width:120rpx; height:48rpx; left:338rpx; top:984rpx; }

/* 消化敏感标签 */
.tag-18 { width:140rpx; height:48rpx; left:202rpx; top:604rpx; }
.tag-19 { width:140rpx; height:48rpx; left:494rpx; top:604rpx; }
.tag-20 { width:140rpx; height:48rpx; left:202rpx; top:670rpx; }
.tag-21 { width:120rpx; height:48rpx; left:358rpx; top:604rpx; }
.tag-22 { width:88rpx;  height:48rpx; left:358rpx; top:670rpx; }
.tag-23 { width:88rpx;  height:48rpx; left:462rpx; top:670rpx; }
.tag-24 { width:88rpx;  height:48rpx; left:566rpx; top:670rpx; }

/* 过敏勾选 */
.check-allergy {
  border-radius: 40rpx;
  border: 2rpx solid #999999;
  width: 32rpx;
  height: 32rpx;
  position: absolute;
  left: 202rpx;
  top: 746rpx;
}
.text-allergy {
  color: #666666;
  font-size: 24rpx;
  position: absolute;
  left: 246rpx;
  top: 744rpx;
}

/* ── 隐私弹窗 ── */
.overlay {
  background: rgba(0, 0, 0, 0.2);
  width: 750rpx;
  height: 1624rpx;
  position: absolute;
  left: 0;
  top: 0;
}
.modal-bg {
  background: #ffffff;
  border-radius: 16rpx;
  width: 560rpx;
  height: 566rpx;
  position: absolute;
  left: 96rpx;
  top: 530rpx;
}
.modal-title {
  color: #000000;
  text-align: center;
  font-size: 32rpx;
  font-weight: 500;
  position: absolute;
  left: 238rpx;
  top: 558rpx;
}
.modal-desc {
  color: #333333;
  font-size: 28rpx;
  font-weight: 500;
  position: absolute;
  left: 132rpx;
  top: 626rpx;
  width: 490rpx;
}
.modal-list {
  color: #666666;
  font-size: 28rpx;
  line-height: 44rpx;
  position: absolute;
  left: 156rpx;
  top: 734rpx;
  width: 490rpx;
}
.modal-item {
  position: absolute;
  left: 20rpx;
}
.modal-check {
  position: absolute;
  left: 156rpx;
  top: 916rpx;
}
.modal-checkbox {
  border-radius: 50%;
  border: 2rpx solid #666666;
  width: 26rpx;
  height: 26rpx;
  display: inline-block;
  vertical-align: middle;
}
.modal-agree-text {
  color: #333333;
  font-size: 24rpx;
  font-weight: 300;
  display: inline-block;
  vertical-align: middle;
  margin-left: 16rpx;
  width: 420rpx;
}
.modal-btn-confirm {
  background: #cccccc;
  border-radius: 42rpx;
  border: 2rpx solid transparent;
  width: 204rpx;
  height: 56rpx;
  position: absolute;
  left: 386rpx;
  top: 986rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}
.modal-btn-text {
  color: #ffffff;
  font-size: 28rpx;
  font-weight: 500;
}
.modal-btn-skip {
  background: #ffffff;
  border-radius: 42rpx;
  border: 2rpx solid #85d2c7;
  width: 204rpx;
  height: 56rpx;
  position: absolute;
  left: 152rpx;
  top: 986rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}
.modal-btn-skip-text {
  color: #85d2c7;
  font-size: 28rpx;
  font-weight: 500;
}
</style>
