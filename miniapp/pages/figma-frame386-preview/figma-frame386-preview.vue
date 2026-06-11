<template>
  <view class="frame-386">
    <!-- 假状态栏已移除（真机系统自带） -->

    <!-- 假底部 Home Indicator 已移除（真机系统自带） -->

    <!-- 返回 + 标题 -->
    <view class="back-hit" @tap="onBack">
      <image class="ico-back" src="/static/figma-frame386/right0.svg" mode="aspectFit" />
    </view>
    <view class="txt-title">完成订单</view>

    <!-- 描述文案 -->
    <view class="desc-text">
      <view>您的订单已完成~</view>
      <view>欢迎填写订单评价，领取会员积分~</view>
    </view>

    <!-- 使用体验感 -->
    <view class="row-label row-label-1">使用体验感：</view>
    <view class="star-row star-row-1">
      <image v-for="i in 5" :key="'a'+i" class="star-icon" :src="starSrc(ratingUse, i)" mode="aspectFit" @tap="onStar('use', i)" />
    </view>

    <!-- 饮用体验感 -->
    <view class="row-label row-label-2">饮用体验感：</view>
    <view class="star-row star-row-2">
      <image v-for="i in 5" :key="'b'+i" class="star-icon" :src="starSrc(ratingDrink, i)" mode="aspectFit" @tap="onStar('drink', i)" />
    </view>

    <!-- 评价区域 -->
    <view class="review-label">评价：</view>
    <textarea class="review-input" placeholder="请输入您的评价…" />

    <!-- 按钮 -->
    <view class="btn-cancel" @tap="onCancel">
      <view class="btn-cancel-bg"></view>
      <view class="btn-cancel-text">取消</view>
    </view>
    <view class="btn-confirm" @tap="onConfirm">
      <view class="btn-confirm-bg"></view>
      <view class="btn-confirm-text">完成</view>
    </view>
  </view>
</template>

<script>
import { goBack } from '@/utils/nav.js';
import { sendFeedback } from '@/api/feedback.js';

const HOME = '/pages/figma-frame400-preview/figma-frame400-preview';
const S = "/static/figma-frame386/";
export default {
  name: "FigmaFrame386Preview",
  data() {
    return {
      ratingUse: 5,
      ratingDrink: 5,
    };
  },
  methods: {
    starSrc(rating, i) {
      // i 是 1~5，rating 是 0~5
      // i <= rating → 亮星（青绿色）；i > rating → 灰星
      return S + (i <= rating ? "star4.svg" : "star0.svg");
    },
    onBack() { goBack(); },
    onStar(type, i) {
      if (type === 'use') {
        this.ratingUse = i;
      } else if (type === 'drink') {
        this.ratingDrink = i;
      }
    },
    onCancel() {
      console.log('[Frame386] cancel -> home');
      uni.redirectTo({
        url: HOME,
        fail(err) { console.error('[Frame386] go home failed', err); }
      });
    },
    onConfirm() {
      console.log('[Frame386] finish -> home', { ratingUse: this.ratingUse, ratingDrink: this.ratingDrink });
      const config = uni.getStorageSync('custom_recipe_config') || {};
      const recipe = uni.getStorageSync('current_recipe') || {};
      sendFeedback('submit_review', {
        rating: this.ratingUse,
        rating_use: this.ratingUse,
        rating_drink: this.ratingDrink,
        recipe_id: recipe.recipe_id,
        recipe_name: recipe.name,
        custom_recipe_config: config,
      });
      uni.redirectTo({
        url: HOME,
        fail(err) { console.error('[Frame386] go home failed', err); }
      });
    },
  },
};
</script>

<style scoped>
.frame-386 { width: 750rpx; height: 100vh; background: #fff; position: relative; overflow: hidden; padding-bottom: env(safe-area-inset-bottom); box-sizing: border-box; }

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

.desc-text { color: #666; text-align: center; font-family: "PingFangSc-Regular", sans-serif; font-size: 28rpx; font-weight: 400; line-height: 42rpx; position: absolute; left: 158rpx; top: 266rpx; }

.row-label { color: #333; font-family: "PingFangSc-Medium", sans-serif; font-size: 28rpx; font-weight: 500; position: absolute; left: 74rpx; }
.row-label-1 { top: 490rpx; }
.row-label-2 { top: 584rpx; }

.star-row { position: absolute; left: 262rpx; display: flex; flex-direction: row; gap: 36rpx; }
.star-row-1 { top: 486rpx; }
.star-row-2 { top: 580rpx; }
.star-icon { width: 48rpx; height: 48rpx; }

.review-label { color: #333; font-family: "PingFangSc-Medium", sans-serif; font-size: 28rpx; font-weight: 500; position: absolute; left: 158rpx; top: 674rpx; }

/* uni-app textarea */
textarea { position: absolute; left: 264rpx; top: 674rpx; width: 400rpx; height: 300rpx; background: #fff; border: 2rpx solid #ccc; border-radius: 16rpx; padding: 16rpx; font-size: 26rpx; color: #333; box-sizing: border-box; }

.btn-cancel { position: absolute; left: 40rpx; top: 1446rpx; width: 320rpx; height: 80rpx; }
.btn-cancel-bg { background: rgba(204,204,204,0.2); border-radius: 60rpx; border: 2rpx solid #ccc; width: 320rpx; height: 80rpx; position: absolute; left: 0; top: 0; }
.btn-cancel-text { color: #999; text-align: center; font-family: "PingFangSc-Medium", sans-serif; font-size: 32rpx; font-weight: 500; position: absolute; left: 0; top: 50%; transform: translateY(-50%); width: 320rpx; }

.btn-confirm { position: absolute; left: 390rpx; top: 1446rpx; width: 320rpx; height: 80rpx; }
.btn-confirm-bg { background: #56bfb0; border-radius: 60rpx; border: 2rpx solid transparent; width: 320rpx; height: 80rpx; position: absolute; left: 0; top: 0; }
.btn-confirm-text { color: #fff; text-align: center; font-family: "PingFangSc-Medium", sans-serif; font-size: 32rpx; font-weight: 500; position: absolute; left: 0; top: 50%; transform: translateY(-50%); width: 320rpx; }
</style>
