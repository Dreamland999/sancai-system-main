<template>
  <view class="frame-391">
    <!-- 顶部白色底色 -->
    <view class="top-bar"></view>

    <!-- 假状态栏已移除（真机系统自带） -->

    <!-- 假底部 Home Indicator 已移除（真机系统自带） -->

    <!-- 返回箭头 -->
    <view class="back-hit" @tap="onBack">
      <image class="ico-back" src="/static/figma-frame391/right0.svg" mode="aspectFit" />
    </view>
    <!-- 标题（点击切换三状态） -->
    <view class="txt-title" @tap="onToggleState">自行调整</view>

    <!-- ========== 共享元素：底部按钮（package 状态用自己的独立按钮） ========== -->
    <view v-if="currentAdjustState !== 'package' && currentAdjustState !== 'sprinkle'" class="btn-next" @tap="onNext">
      <view class="btn-next-bg"></view>
      <view class="btn-next-text">下一步</view>
    </view>

    <!-- ============================================================ -->
    <!-- 状态：top（Frame391） / middle（Frame392）                    -->
    <!-- ============================================================ -->
    <template v-if="currentAdjustState === 'top' || currentAdjustState === 'middle'">
      <!-- 顶部胶囊标签 -->
      <view class="tag-capsule" @tap="onToggleState">
        <view class="tag-capsule-bg" :class="{ 'tag-bg-pink': currentAdjustState === 'middle' }"></view>
        <view class="tag-capsule-text">{{ currentAdjustState === 'top' ? '顶盖：' + recipeName : '中层：' + recipeName }}</view>
      </view>

      <!-- 杯子（共用层） -->
      <image class="cup-vector0" src="/static/figma-frame391/vector0.svg" mode="aspectFit" />
      <image class="cup-g13130" src="/static/figma-frame391/group-13130.svg" mode="aspectFit" />
      <image class="cup-g13160" src="/static/figma-frame391/group-13160.svg" mode="aspectFit" />
      <image class="cup-v1" src="/static/figma-frame391/vector1.svg" mode="aspectFit" />

      <!-- top 专属杯层 -->
      <template v-if="currentAdjustState === 'top'">
        <image class="cup-g13170" src="/static/figma-frame391/group-13170.svg" mode="aspectFit" />
        <image class="cup-r1357" src="/static/figma-frame391/rectangle-13570.svg" mode="aspectFit" />
        <image class="cup-v2" src="/static/figma-frame391/vector2.svg" mode="aspectFit" />
        <image class="cup-v3" src="/static/figma-frame391/vector3.svg" mode="aspectFit" />
        <image class="cup-v4" src="/static/figma-frame391/vector4.svg" mode="aspectFit" />
        <image class="cup-union" src="/static/figma-frame391/union0.svg" mode="aspectFit" />
        <image class="cup-v5" src="/static/figma-frame391/vector5.svg" mode="aspectFit" />
      </template>
      <!-- middle 专属杯层 -->
      <template v-if="currentAdjustState === 'middle'">
        <image class="cup-g13960t" src="/static/figma-frame391/group-13960.svg" mode="aspectFit" />
        <image class="cup-g13970" src="/static/figma-frame391/group-13970.svg" mode="aspectFit" />
        <image class="cup-u2" src="/static/figma-frame391/union2.svg" mode="aspectFit" />
      </template>

      <!-- 水果颗粒 -->
      <image
        v-for="(fp, i) in topMidFruit"
        :key="'tpf' + i"
        :src="'/static/figma-frame391/_20260602215953-766-157-' + fp.s + '.png'"
        mode="aspectFill"
        :style="{ width: '42rpx', height: '40rpx', position: 'absolute', left: fp.l + 'rpx', top: fp.t + 'rpx' }"
      />

      <!-- 卡片1：浓度 -->
      <view class="card-conc" @tap="cycleConcentration">
        <view class="card-conc-bg" :class="{ 'card-bg-pink': currentAdjustState === 'middle' }"></view>
        <view class="card-conc-desc">在屏幕任意区域左右滑动以改变注浆浓度~</view>
        <view class="card-conc-label">浓度</view>
        <view class="card-conc-val">{{ config.concentration }}g/L</view>
      </view>

      <!-- 颗粒集群 -->
      <image
        v-for="p in particlesTopMid"
        :key="p.n"
        :src="p.src"
        mode="aspectFill"
        :style="{ width: p.w + 'rpx', height: p.h + 'rpx', left: p.l + 'rpx', top: p.t + 'rpx', position: 'absolute' }"
      />

      <!-- 卡片2：颗粒度 -->
      <view class="card-gran" @tap="cycleParticleSize">
        <view class="card-gran-bg" :class="{ 'card-bg-pink': currentAdjustState === 'middle' }"></view>
        <view class="card-gran-desc">在屏幕任意区域上下滑动以改变注浆颗粒度大小~</view>
        <view class="card-gran-label">颗粒度</view>
        <view class="card-gran-val">{{ config.particle_size }}cm³</view>
        <image class="dot-img" src="/static/figma-frame391/_20260602215953-766-157-91.png" mode="aspectFill" />
      </view>
    </template>

    <!-- ============================================================ -->
    <!-- 状态：iceSugar — 滑块调节冰度/糖度                            -->
    <!-- ============================================================ -->
    <template v-else-if="currentAdjustState === 'iceSugar'">
      <!-- 杯子（居中） -->
      <view class="icecup-area">
        <image class="icecup-v0" src="/static/figma-frame391/vector0.svg" mode="aspectFit" />
        <image class="icecup-g13" src="/static/figma-frame391/group-13130.svg" mode="aspectFit" />
        <image class="icecup-g16" src="/static/figma-frame391/group-13160.svg" mode="aspectFit" />
        <image class="icecup-g17" src="/static/figma-frame391/group-13170.svg" mode="aspectFit" />
        <image class="icecup-g96" src="/static/figma-frame391/group-13960.svg" mode="aspectFit" />
        <image class="icecup-v1" src="/static/figma-frame391/vector1.svg" mode="aspectFit" />
      </view>

      <!-- 卡片1：冰度 -->
      <view class="islider-card">
        <view class="islider-card-bg"></view>
        <view class="islider-row">
          <view class="islider-label">冰度</view>
          <view class="islider-val">{{ iceDisplay }}</view>
        </view>
        <view class="islider-wrap">
          <text class="islider-hint">少冰</text>
          <slider
            class="islider-slider"
            :value="iceLevel"
            :min="0"
            :max="5"
            :step="1"
            activeColor="#85d2c7"
            backgroundColor="rgba(133,210,199,0.2)"
            block-size="22"
            @change="onIceChange"
          />
          <text class="islider-hint">多冰</text>
        </view>
      </view>

      <!-- 卡片2：糖度 -->
      <view class="islider-card islider-card2">
        <view class="islider-card-bg"></view>
        <view class="islider-row">
          <view class="islider-label">糖度</view>
          <view class="islider-val">{{ sugarDisplay }}</view>
        </view>
        <view class="islider-wrap">
          <text class="islider-hint">少糖</text>
          <slider
            class="islider-slider"
            :value="sugarLevel"
            :min="0"
            :max="5"
            :step="1"
            activeColor="#85d2c7"
            backgroundColor="rgba(133,210,199,0.2)"
            block-size="22"
            @change="onSugarChange"
          />
          <text class="islider-hint">多糖</text>
        </view>
      </view>
    </template>

    <!-- ============================================================ -->
    <!-- 状态：package（Component.vue — 装饰插件/包材图案选择）         -->
    <!-- ============================================================ -->
    <template v-else-if="currentAdjustState === 'package'">
      <view class="package-content">
        <!-- component-13 主区域 -->
        <view class="package-main">
          <!-- 上方候选区（2 个槽位，按 index 定位，selectedPackageKey 变化时强制重建） -->
          <view class="package-candidates" :key="'candidates-' + selectedPackageKey">
            <image
              v-for="(option, index) in candidatePackageOptions"
              :key="selectedPackageKey + '-' + option.key + '-' + index"
              :class="['package-candidate-img', index === 0 ? 'candidate-slot-1' : 'candidate-slot-2']"
              :src="option.thumb"
              mode="scaleToFill"
              @tap="selectPackageStyle(option)"
            />
          </view>

          <!-- 杯子底图（group-13450.svg 原属装饰插件2，preview 阶段临时复用） -->
          <image class="package-cup-base" src="/static/figma-frame391/group-13450.svg" mode="scaleToFill" />

          <!-- 左侧杯套（覆盖杯子下半部） -->
          <image v-if="currentSleeve" class="package-sleeve-left" :key="'sleeve-' + selectedPackageKey" :src="currentSleeve" mode="scaleToFill" />
          <image v-if="!currentSleeve" class="package-sleeve-left" :key="'sleeve-default-' + selectedPackageKey" src="/static/figma-frame391/group-13390.svg" mode="scaleToFill" />
          <!-- 右侧横向包装（当前选中展示，不可点击切换） -->
          <view class="package-sleeve-right">
            <image
              class="package-wrap-img"
              :key="'wrap-' + selectedPackageKey"
              :src="currentWrap"
              mode="scaleToFill"
            />
          </view>
        </view>

        <!-- 提示文案 -->
        <view class="package-tip">点击不同图案以更改包材~</view>

        <!-- 底部确定按钮 -->
        <view class="package-btn" @tap="onNext">
          <view class="package-btn-bg"></view>
          <view class="package-btn-text">确定</view>
        </view>
      </view>
    </template>

    <!-- ============================================================ -->
    <!-- 状态：sprinkle（装饰插件2：撒料选择）                          -->
    <!-- ============================================================ -->
    <template v-else-if="currentAdjustState === 'sprinkle'">
      <view class="sprinkle-content">
        <!-- 提示文案 -->
        <view class="sprinkle-tip">滑动以选择想要的撒料~</view>

        <!-- 确定按钮 -->
        <view class="sprinkle-btn" @tap="onNext">
          <view class="sprinkle-btn-bg"></view>
          <view class="sprinkle-btn-text">确定</view>
        </view>

        <!-- component-14：主区域 -->
        <view class="sprinkle-main">
          <!-- 杯子底图（group-13450.svg 原属装饰插件2，preview 阶段临时复用） -->
          <image class="sprinkle-cup-img" src="/static/figma-frame391/group-13450.svg" mode="scaleToFill" />



          <!-- 选项1：星星糖果 -->
          <view class="sprinkle-opt sprinkle-opt-active" @tap="selectSprinkle(sprinkleOptions[0], 0)">
            <view class="sprinkle-opt-circle" :class="selectedSprinkleIdx === 0 ? 'sprinkle-circle-green' : 'sprinkle-opt-circle-inactive'"></view>
            <image class="sprinkle-opt-i1" src="/static/figma-frame391/group-13430.svg" mode="aspectFit" />
            <image class="sprinkle-opt-i2" src="/static/figma-frame391/group-13460.svg" mode="aspectFit" />
            <image class="sprinkle-opt-i3" src="/static/figma-frame391/group-13470.svg" mode="aspectFit" />
            <image class="sprinkle-opt-i4" src="/static/figma-frame391/group-13480.svg" mode="aspectFit" />
            <image class="sprinkle-opt-i5" src="/static/figma-frame391/group-13490.svg" mode="aspectFit" />
            <image class="sprinkle-opt-i6" src="/static/figma-frame391/group-13500.svg" mode="aspectFit" />
          </view>
          <view class="sprinkle-opt-label sprinkle-opt-label-active">星星糖果</view>

          <!-- 选项2：五彩撒粉 -->
          <view class="sprinkle-opt sprinkle-opt-mid" @tap="selectSprinkle(sprinkleOptions[1], 1)">
            <view class="sprinkle-opt-circle" :class="selectedSprinkleIdx === 1 ? 'sprinkle-circle-pink' : 'sprinkle-opt-circle-inactive'"></view>
            <view class="sprinkle-dot sprinkle-dot-1"></view>
            <view class="sprinkle-dot sprinkle-dot-2"></view>
            <view class="sprinkle-dot sprinkle-dot-3"></view>
            <view class="sprinkle-dot sprinkle-dot-4"></view>
            <view class="sprinkle-dot sprinkle-dot-5"></view>
            <view class="sprinkle-dot sprinkle-dot-6"></view>
            <view class="sprinkle-dot sprinkle-dot-7"></view>
            <view class="sprinkle-dot sprinkle-dot-8"></view>
          </view>
          <view class="sprinkle-opt-label sprinkle-opt-label-mid">五彩撒粉</view>

          <!-- 选项3：三角小饼干 -->
          <view class="sprinkle-opt sprinkle-opt-bot" @tap="selectSprinkle(sprinkleOptions[2], 2)">
            <view class="sprinkle-opt-circle" :class="selectedSprinkleIdx === 2 ? 'sprinkle-circle-orange' : 'sprinkle-opt-circle-inactive'"></view>
            <image class="sprinkle-bis-i1" src="/static/figma-frame391/group-13550.svg" mode="aspectFit" />
            <image class="sprinkle-bis-i2" src="/static/figma-frame391/group-13570.svg" mode="aspectFit" />
            <image class="sprinkle-bis-i3" src="/static/figma-frame391/group-13560.svg" mode="aspectFit" />
            <image class="sprinkle-bis-i4" src="/static/figma-frame391/group-13580.svg" mode="aspectFit" />
          </view>
          <view class="sprinkle-opt-label sprinkle-opt-label-bot">三角小饼干</view>
        </view>
      </view>
    </template>
  </view>
</template>

<script>
import { sendFeedback } from '@/api/feedback.js';
const BASE = "/static/figma-frame391/_20260602215953-766-157-";

const PARTICLE_SET_TOP_MID = [
  { n: "21",  src: BASE + "21.png",  w: 14, h: 14, l: 516, t: 724 },
  { n: "110", src: BASE + "110.png", w: 20, h: 18, l: 520, t: 716 },
  { n: "120", src: BASE + "120.png", w: 20, h: 18, l: 510, t: 720 },
  { n: "130", src: BASE + "130.png", w: 20, h: 18, l: 498, t: 730 },
  { n: "140", src: BASE + "140.png", w: 20, h: 18, l: 488, t: 738 },
  { n: "150", src: BASE + "150.png", w: 20, h: 18, l: 510, t: 732 },
  { n: "160", src: BASE + "160.png", w: 20, h: 18, l: 522, t: 736 },
  { n: "170", src: BASE + "170.png", w: 20, h: 18, l: 534, t: 726 },
  { n: "31",  src: BASE + "31.png",  w: 14, h: 14, l: 516, t: 710 },
  { n: "40",  src: BASE + "40.png",  w: 14, h: 14, l: 534, t: 718 },
  { n: "50",  src: BASE + "50.png",  w: 14, h: 14, l: 508, t: 726 },
  { n: "60",  src: BASE + "60.png",  w: 10, h: 10, l: 522, t: 740 },
  { n: "70",  src: BASE + "70.png",  w: 10, h: 10, l: 542, t: 738 },
  { n: "180", src: BASE + "180.png", w: 10, h: 10, l: 484, t: 742 },
  { n: "190", src: BASE + "190.png", w: 10, h: 10, l: 508, t: 744 },
  { n: "200", src: BASE + "200.png", w: 10, h: 10, l: 544, t: 744 },
  { n: "210", src: BASE + "210.png", w: 10, h: 10, l: 556, t: 740 },
  { n: "220", src: BASE + "220.png", w: 10, h: 10, l: 566, t: 738 },
  { n: "230", src: BASE + "230.png", w: 10, h: 10, l: 554, t: 732 },
  { n: "240", src: BASE + "240.png", w: 10, h: 10, l: 550, t: 736 },
  { n: "250", src: BASE + "250.png", w: 10, h: 10, l: 548, t: 732 },
  { n: "80",  src: BASE + "80.png",  w: 10, h: 10, l: 528, t: 732 },
  { n: "90",  src: BASE + "90.png",  w: 14, h: 14, l: 510, t: 736 },
  { n: "100", src: BASE + "100.png", w: 14, h: 14, l: 492, t: 728 },
];

function getCurrentRecipe() {
  try { return uni.getStorageSync('current_recipe') || {}; } catch (e) { return {}; }
}

function initConfig(recipe) {
  return {
    recipe_id: recipe.recipe_id || '',
    recipe_name: recipe.name || '',
    concentration: 23,
    particle_size: 0.1,
    ice: 200,
    sugar: 200,
    package_style: null,
    sprinkle: null,
    adjust_state: 'top',
  };
}

export default {
  name: "FigmaFrame391Preview",
  data() {
    const recipe = getCurrentRecipe();
    const savedConfig = uni.getStorageSync('custom_recipe_config') || {};
    return {
      currentAdjustState: "top",
      particlesTopMid: PARTICLE_SET_TOP_MID,
      currentRecipe: recipe,
      config: initConfig(recipe),
      iceLevel: savedConfig.iceLevel != null ? savedConfig.iceLevel : 4,
      sugarLevel: savedConfig.sugarLevel != null ? savedConfig.sugarLevel : 4,
      lastIceLevel: savedConfig.iceLevel != null ? savedConfig.iceLevel : 4,
      lastSugarLevel: savedConfig.sugarLevel != null ? savedConfig.sugarLevel : 4,
      packageOptions: [
        {
          key: 'default_green', label: '原色',
          thumb: '/static/figma-frame391/package-thumb-default.png',
          sleeve: '',
          wrap: '/static/figma-frame391/package-wrap-default.png',
        },
        {
          key: 'blue_geometry', label: '蓝色',
          thumb: '/static/figma-frame391/package-thumb-blue.png',
          sleeve: '/static/figma-frame391/sleeve-blue.png',
          wrap: '/static/figma-frame391/package-wrap-blue.png',
        },
        {
          key: 'color_wave', label: '多彩',
          thumb: '/static/figma-frame391/package-thumb-color.png',
          sleeve: '/static/figma-frame391/sleeve-color.png',
          wrap: '/static/figma-frame391/package-wrap-color.png',
        },
      ],
      selectedPackageKey: 'default_green',
      selectedSprinkleIdx: 0,
      sprinkleOptions: [
        { key: 'star_candy', label: '星星糖果' },
        { key: 'color_powder', label: '五彩撒粉' },
        { key: 'triangle_biscuit', label: '三角小饼干' },
      ],
    };
  },
  mounted() {
    const savedConfig = uni.getStorageSync('custom_recipe_config') || {};
    const savedKey = savedConfig.packageKey;
    if (savedKey && this.packageOptions.some(item => item.key === savedKey)) {
      this.selectedPackageKey = savedKey;
    }
  },
  computed: {
    currentPackageOption() {
      return this.packageOptions.find(item => item.key === this.selectedPackageKey)
        || this.packageOptions.find(item => item.key === 'default_green');
    },
    currentSleeve() {
      return this.currentPackageOption ? this.currentPackageOption.sleeve : '';
    },
    currentWrap() {
      return this.currentPackageOption ? this.currentPackageOption.wrap : '';
    },
    topMidFruit() {
      if (this.currentAdjustState === "top") {
        return [{ s: "10", l: 6, t: 630 }, { s: "20", l: 70, t: 596 }, { s: "30", l: 160, t: 616 }];
      }
      return [{ s: "10", l: 32, t: 822 }, { s: "20", l: 96, t: 788 }, { s: "30", l: 186, t: 808 }];
    },
    recipeName() {
      return this.currentRecipe.name || '茉莉+抹茶奶昔';
    },
    iceDisplay() {
      return (this.iceLevel * 50) + 'g/L';
    },
    sugarDisplay() {
      return (this.sugarLevel * 50) + 'g/L';
    },
    candidatePackageOptions() {
      return this.packageOptions.filter(item => item.key !== this.selectedPackageKey);
    },
  },
  methods: {
    onBack() {
      const adjustStateOrder = ['top', 'middle', 'iceSugar', 'package', 'sprinkle'];
      const idx = adjustStateOrder.indexOf(this.currentAdjustState);
      console.log('[Frame391] back from state:', this.currentAdjustState);
      if (idx > 0) {
        this.currentAdjustState = adjustStateOrder[idx - 1];
      } else {
        const pages = getCurrentPages();
        if (pages.length > 1) {
          uni.navigateBack({
            fail(err) { console.error('[Frame391] navigateBack failed', err); }
          });
        } else {
          uni.redirectTo({
            url: '/pages/figma-frame400-preview/figma-frame400-preview',
            fail(err) { console.error('[Frame391] redirectTo failed', err); }
          });
        }
      }
    },
    onNext() {
      const chain = { top: 'middle', middle: 'iceSugar', iceSugar: 'package', package: 'sprinkle' };
      if (chain[this.currentAdjustState]) {
        this.currentAdjustState = chain[this.currentAdjustState];
      } else if (this.currentAdjustState === 'sprinkle') {
        this.config.adjust_state = 'sprinkle';
        uni.setStorageSync('custom_recipe_config', this.config);
        console.log('[Frame391] final custom_recipe_config saved', this.config);
        sendFeedback('enter_payment', { adjust_state: 'sprinkle', custom_recipe_config: this.config });
        uni.redirectTo({ url: '/pages/figma-frame391-animation/figma-frame391-animation' });
      } else {
        uni.showToast({ title: '确定', icon: 'none' });
      }
    },
    onIceChange(e) {
      const v = e.detail.value;
      if (v !== this.lastIceLevel) {
        this.lastIceLevel = v;
        this.triggerLightHaptic();
      }
      this.iceLevel = v;
      this.config.ice = v * 50;
      this.syncConfig();
    },
    onSugarChange(e) {
      const v = e.detail.value;
      if (v !== this.lastSugarLevel) {
        this.lastSugarLevel = v;
        this.triggerLightHaptic();
      }
      this.sugarLevel = v;
      this.config.sugar = v * 50;
      this.syncConfig();
    },
    triggerLightHaptic() {
      try {
        uni.vibrateShort({
          type: 'light',
          fail: () => {}
        });
      } catch (e) {}
    },
    resetSleeve() {
      this.selectedPackageKey = 'default_green';
      this.savePackageConfig();
    },
    selectPackageStyle(option) {
      if (!option || !option.key) return;
      this.selectedPackageKey = option.key;
      this.savePackageConfig();
      console.log('[Frame391] package selected:', option);
    },
    selectSprinkle(option, idx) {
      this.config.sprinkle = option.key;
      this.config.sprinkle_label = option.label;
      this.selectedSprinkleIdx = idx;
      this.syncConfig();
      console.log('[Frame391] sprinkle selected:', option);
      uni.showToast({ title: '已选择：' + option.label, icon: 'none' });
    },
    cycleConcentration() {
      const vals = [18, 23, 28];
      const cur = this.config.concentration || 23;
      const idx = vals.indexOf(cur);
      this.config.concentration = vals[(idx + 1) % vals.length];
      this.syncConfig();
    },
    cycleParticleSize() {
      const vals = [0.1, 0.2, 0.3];
      const cur = this.config.particle_size || 0.1;
      const idx = vals.indexOf(cur);
      this.config.particle_size = vals[(idx + 1) % vals.length];
      this.syncConfig();
    },
    savePackageConfig() {
      const current = this.currentPackageOption;
      if (!current) return;
      const oldConfig = uni.getStorageSync('custom_recipe_config') || {};
      const nextConfig = {
        ...oldConfig,
        packageKey: current.key,
        sleeve: current.sleeve,
        wrap: current.wrap,
      };
      uni.setStorageSync('custom_recipe_config', nextConfig);
      this.config = { ...this.config, ...nextConfig };
      console.log('[Frame391] package config saved', nextConfig);
    },
    syncConfig() {
      const current = this.currentPackageOption || {};
      this.config.adjust_state = this.currentAdjustState;
      this.config.iceLevel = this.iceLevel;
      this.config.sugarLevel = this.sugarLevel;
      this.config.ice = this.iceLevel * 50;
      this.config.sugar = this.sugarLevel * 50;
      this.config.packageKey = this.selectedPackageKey;
      this.config.sleeve = current.sleeve || '';
      this.config.wrap = current.wrap || '';
      uni.setStorageSync('custom_recipe_config', this.config);
      console.log('[Frame391] custom_recipe_config updated', this.config);
    },
    onToggleState() {
      const states = ["top", "middle", "iceSugar", "package", "sprinkle"];
      const idx = states.indexOf(this.currentAdjustState);
      this.currentAdjustState = states[(idx + 1) % 5];
      this.syncConfig();
    },
  },
};
</script>

<style scoped>
.frame-391 {
  width: 750rpx; height: 100vh; background: #ffffff;
  position: relative; overflow: hidden;
  padding-bottom: env(safe-area-inset-bottom); box-sizing: border-box;
}
.top-bar { background: #ffffff; width: 750rpx; height: 176rpx; position: absolute; left: 0; top: 0; }
.status-bar { display: flex; flex-direction: row; align-items: center; justify-content: space-between; width: 780rpx; position: absolute; left: -14rpx; top: 0; padding: 36rpx 52rpx 28rpx 54rpx; box-sizing: border-box; }
.time-wrap { flex-shrink: 0; width: 108rpx; height: 42rpx; position: relative; }
.time { color: #000; text-align: center; font-family: "SfProText-Semibold", sans-serif; font-size: 34rpx; line-height: 44rpx; letter-spacing: -0.82rpx; font-weight: 600; position: absolute; left: 0; top: 50%; transform: translateY(-50%); width: 108rpx; }
.icons-wrap { flex-shrink: 0; width: 156rpx; height: 26rpx; position: relative; }
.icon-battery { width: 54rpx; height: 26rpx; position: absolute; right: 0; top: 0; }
.icon-wifi { width: 34rpx; height: 24rpx; position: absolute; left: 53rpx; top: 1rpx; }
.icon-cellular { width: 38rpx; height: 24rpx; position: absolute; left: 0; top: 1rpx; }
.home-bar { width: 780rpx; height: 38rpx; position: absolute; left: -14rpx; top: 1586rpx; }
.home-bar-inner { background: #000; border-radius: 200rpx; width: 268rpx; height: 10rpx; position: absolute; left: 50%; transform: translateX(-50%); bottom: 16rpx; }
.back-hit { position: absolute; left: 70rpx; top: 88rpx; width: 80rpx; height: 80rpx; z-index: 5; display: flex; align-items: center; justify-content: center; }
.ico-back { width: 48rpx; height: 48rpx; }
.txt-title { color: #333; text-align: center; font-family: "PingFangSc-Medium", sans-serif; font-size: 32rpx; font-weight: 500; position: absolute; left: 312rpx; top: 108rpx; }

/* 胶囊 */
.tag-capsule { position: absolute; left: 156rpx; top: 270rpx; width: 440rpx; height: 68rpx; }
.tag-capsule-bg { background: rgba(59,189,170,0.4); border-radius: 60rpx; border: 2rpx solid #fff; width: 440rpx; height: 68rpx; position: absolute; left: 0; top: 0; }
.tag-bg-pink { background: rgba(255,137,126,0.4) !important; }
.tag-capsule-text { color: #666; text-align: center; font-family: "PingFangSc-Medium", sans-serif; font-size: 28rpx; font-weight: 500; position: absolute; left: 0; top: 50%; transform: translateY(-50%); width: 440rpx; }

/* top/middle 杯子 */
.cup-vector0 { width: 395rpx; height: 143rpx; position: absolute; left: -115rpx; top: 1208rpx; }
.cup-g13130  { width: 488rpx; height: 506rpx; position: absolute; left: -162rpx; top: 787rpx; }
.cup-g13160  { width: 543rpx; height: 317rpx; position: absolute; left: -188rpx; top: 542rpx; }
.cup-v1      { width: 548rpx; height: 156rpx; position: absolute; left: -188rpx; top: 412rpx; }
.cup-g13170  { width: 540rpx; height: 300rpx; position: absolute; left: -188rpx; top: 630rpx; }
.cup-r1357   { width: 576rpx; height: 155rpx; position: absolute; left: -208rpx; top: 496rpx; }
.cup-v2      { width: 562rpx; height: 168rpx; position: absolute; left: -199rpx; top: 456rpx; }
.cup-v3      { width: 543rpx; height: 168rpx; position: absolute; left: -188rpx; top: 542rpx; }
.cup-v4      { width: 571rpx; height: 168rpx; position: absolute; left: -204rpx; top: 410rpx; }
.cup-union   { width: 576rpx; height: 296rpx; position: absolute; left: -208rpx; top: 414rpx; }
.cup-v5      { width: 68rpx;  height: 621rpx; position: absolute; left: 241rpx;  top: 587rpx; }
.cup-g13960t { width: 576rpx; height: 300rpx; position: absolute; left: -208rpx; top: 410rpx; }
.cup-g13970  { width: 540rpx; height: 300rpx; position: absolute; left: -188rpx; top: 630rpx; }
.cup-u2      { width: 577rpx; height: 300rpx; position: absolute; left: -226rpx; top: 636rpx; }

/* top/middle 卡片 */
.card-conc { position: absolute; left: 398rpx; top: 598rpx; width: 316rpx; height: 200rpx; }
.card-conc-bg { background: rgba(133,210,199,0.2); border-radius: 16rpx; width: 316rpx; height: 200rpx; position: absolute; left: 0; top: 0; }
.card-bg-pink { background: rgba(255,137,126,0.2) !important; }
.card-conc-desc { color: #666; font-family: "PingFangSc-Regular", sans-serif; font-size: 24rpx; font-weight: 400; line-height: 34rpx; position: absolute; left: 20rpx; top: 18rpx; width: 276rpx; }
.card-conc-label { color: #666; font-family: "PingFangSc-Regular", sans-serif; font-size: 28rpx; font-weight: 400; position: absolute; left: 20rpx; top: 118rpx; }
.card-conc-val { color: #333; font-family: "PingFangSc-Heavy", sans-serif; font-size: 28rpx; font-weight: 400; position: absolute; left: 208rpx; top: 114rpx; }
.card-gran { position: absolute; left: 398rpx; top: 878rpx; width: 316rpx; height: 200rpx; }
.card-gran-bg { background: rgba(133,210,199,0.2); border-radius: 16rpx; width: 316rpx; height: 200rpx; position: absolute; left: 0; top: 0; }
.card-gran-desc { color: #666; font-family: "PingFangSc-Regular", sans-serif; font-size: 24rpx; font-weight: 400; line-height: 34rpx; position: absolute; left: 20rpx; top: 18rpx; width: 276rpx; }
.card-gran-label { color: #666; font-family: "PingFangSc-Regular", sans-serif; font-size: 28rpx; font-weight: 400; position: absolute; left: 20rpx; top: 118rpx; }
.card-gran-val { color: #333; font-family: "PingFangSc-Heavy", sans-serif; font-size: 28rpx; font-weight: 400; position: absolute; left: 200rpx; top: 118rpx; }
.dot-img { width: 36rpx; height: 34rpx; position: absolute; left: 130rpx; top: 120rpx; }

/* ===== iceSugar 杯子（居中） ===== */
.icecup-area { position: absolute; left: 170rpx; top: 260rpx; width: 411rpx; height: 480rpx; }
.icecup-v0  { width: 155rpx; height: 56rpx;  position: absolute; left: 127rpx; top: 236rpx; }
.icecup-g13 { width: 189rpx; height: 196rpx; position: absolute; left: 108rpx; top: 112rpx; }
.icecup-g16 { width: 210rpx; height: 123rpx; position: absolute; left: 99rpx;  top: 39rpx; }
.icecup-g17 { width: 209rpx; height: 116rpx; position: absolute; left: 99rpx;  top: 65rpx; }
.icecup-g96 { width: 223rpx; height: 116rpx; position: absolute; left: 90rpx;  top: 0; }
.icecup-v1  { width: 26rpx;  height: 240rpx; position: absolute; left: 266rpx; top: 52rpx; }

/* ===== iceSugar 滑块卡片（共用） ===== */
.islider-card { position: absolute; left: 60rpx; right: 60rpx; width: 630rpx; height: 170rpx; top: 760rpx; }
.islider-card2 { top: 950rpx; }
.islider-card-bg { background: rgba(133,210,199,0.12); border-radius: 16rpx; width: 100%; height: 100%; position: absolute; left: 0; top: 0; }
.islider-row { position: absolute; left: 28rpx; right: 28rpx; top: 16rpx; display: flex; flex-direction: row; justify-content: space-between; align-items: baseline; }
.islider-label { color: #666; font-family: "PingFangSc-Medium", sans-serif; font-size: 28rpx; font-weight: 500; }
.islider-val { color: #333; font-family: "PingFangSc-Heavy", sans-serif; font-size: 28rpx; font-weight: 400; }
.islider-wrap { position: absolute; left: 20rpx; right: 20rpx; top: 60rpx; display: flex; flex-direction: row; align-items: center; gap: 12rpx; }
.islider-slider { flex: 1; margin: 0 4rpx; }
.islider-hint { color: #aaa; font-family: "PingFangSc-Regular", sans-serif; font-size: 22rpx; white-space: nowrap; min-width: 56rpx; text-align: center; }

/* ===== package 状态 ===== */
.package-content { width: 750rpx; min-height: 1624rpx; background: #fff; position: relative; overflow: hidden; }

/* ===== package 手调区：只改 left/top/width/height ===== */

/* -- 主容器 -- */
.package-main {    left: 0;     top: 390rpx; width: 750rpx; height: 670rpx; z-index: auto; }

/* -- 杯子底图（group-13450.svg，原属装饰插件2，preview 阶段临时复用） -- */
.package-cup-base     { left: 30rpx;  top: 200rpx; width: 300rpx; height: 360rpx; z-index: 0; }

/* -- 杯套左侧 -- */
.package-sleeve-left  { left: 75rpx;  top: 380rpx; width: 210rpx; height: 188rpx; z-index: 2; }

/* -- 右侧横向包装（仅布局，无装饰） -- */
.package-sleeve-right {
  position: absolute;
  left: 220rpx; top: 375rpx;
  width: 450rpx; height: 190rpx;
  z-index: 1;
}
.package-wrap-img {
  width: 100%;
  height: 100%;
  display: block;
}

/* -- 上方候选区（2 个显式槽位，按 index 定位，仅布局无装饰） -- */
.package-candidates { position: absolute; left: 0; top: 0; z-index: 10; }
.package-candidate-img { position: absolute; width: 350rpx; height: 160rpx; }
.candidate-slot-1 { left: 310rpx; top: -5rpx; }
.candidate-slot-2 { left: 310rpx; top: 185rpx; }

/* -- 提示文案 -- */
.package-tip          { left: 214rpx; top: 1178rpx; }

/* -- 确定按钮 -- */
.package-btn          { left: 156rpx; top: 1412rpx; width: 440rpx; height: 80rpx; }

/* ===== package 固定样式（不要改以下数值）===== */

.package-main,
.package-cup-base,
.package-sleeve-left,
.package-candidates,
.package-tip,
.package-btn { position: absolute; }

/* 提示文案 */
.package-tip { color: #666; text-align: center; font-family: "PingFangSc-Regular", sans-serif; font-size: 28rpx; font-weight: 400; }

/* 确定按钮 */
.package-btn-bg { background: #56bfb0; border-radius: 60rpx; border: 2rpx solid #fff; width: 100%; height: 100%; position: absolute; left: 0; top: 0; }
.package-btn-text { color: #fff; text-align: center; font-family: "PingFangSc-Medium", sans-serif; font-size: 32rpx; font-weight: 500; position: absolute; left: 0; top: 50%; transform: translateY(-50%); width: 100%; }

/* ===== sprinkle 状态（装饰插件2：撒料选择）===== */
.sprinkle-content { width: 750rpx; min-height: 1624rpx; background: #fff; position: relative; overflow: hidden; }

.sprinkle-tip { color: #666; text-align: center; font-family: "PingFangSc-Regular", sans-serif; font-size: 28rpx; font-weight: 400; position: absolute; left: 228rpx; top: 1220rpx; }

.sprinkle-btn { position: absolute; left: 156rpx; top: 1380rpx; width: 440rpx; height: 80rpx; }
.sprinkle-btn-bg { background: #56bfb0; border-radius: 60rpx; border: 2rpx solid #fff; width: 440rpx; height: 80rpx; position: absolute; left: 0; top: 0; }
.sprinkle-btn-text { color: #fff; text-align: center; font-family: "PingFangSc-Medium", sans-serif; font-size: 32rpx; font-weight: 500; position: absolute; left: 0; top: 50%; transform: translateY(-50%); width: 440rpx; }

/* component-14 容器 */
.sprinkle-main { position: absolute; left: 74rpx; top: 400rpx; width: 590rpx; height: 650rpx; }

/* 杯子底图（group-13450.svg 原属装饰插件2，preview 阶段临时复用） */
.sprinkle-cup-img { position: absolute; left: 0; top: 136rpx; width: 186rpx; height: 339rpx; z-index: 1; }

/* 三角箭头 */


/* 选项圆 — 统一 110rpx */
.sprinkle-opt { position: absolute; width: 110rpx; height: 110rpx; }
.sprinkle-opt-circle { border-radius: 50%; width: 110rpx; height: 110rpx; position: absolute; left: 0; top: 0; }
.sprinkle-opt-circle-active { background: #feffef; border: 4rpx solid #85d2c7; }
.sprinkle-opt-circle-inactive { background: rgba(255,255,248,0.93); border: 4rpx solid #ccc; }
.sprinkle-circle-green { background: #feffef; border: 4rpx solid #85d2c7; }
.sprinkle-circle-pink { background: #fff5f5; border: 4rpx solid #ffb3a7; }
.sprinkle-circle-orange { background: #fffdf5; border: 4rpx solid #f0c060; }

/* 选项文字 — 加宽到 150rpx，nowrap */
.sprinkle-opt-label { font-family: "PingFangSc-Medium", sans-serif; font-size: 24rpx; font-weight: 500; position: absolute; text-align: center; width: 150rpx; white-space: nowrap; }
.sprinkle-opt-label-active { color: #333; left: 420rpx; top: 260rpx; font-size: 28rpx; }
.sprinkle-opt-label-mid    { color: #999; left: 420rpx; top: 68rpx; }
.sprinkle-opt-label-bot    { color: #999; left: 420rpx; top: 440rpx; }

/* 选项1：星星糖果（绿色激活） */
.sprinkle-opt-active { left: 256rpx; top: 200rpx; }
.sprinkle-opt-i1 { width: 22rpx; height: 24rpx; position: absolute; left: 30rpx; top: 72rpx; }
.sprinkle-opt-i2 { width: 36rpx; height: 40rpx; position: absolute; left: 72rpx; top: 38rpx; }
.sprinkle-opt-i3 { width: 26rpx; height: 28rpx; position: absolute; left: 46rpx; top: 26rpx; }
.sprinkle-opt-i4 { width: 26rpx; height: 28rpx; position: absolute; left: 62rpx; top: 22rpx; }
.sprinkle-opt-i5 { width: 44rpx; height: 48rpx; position: absolute; left: 4rpx;  top: 42rpx; }
.sprinkle-opt-i6 { width: 44rpx; height: 48rpx; position: absolute; left: 48rpx; top: 72rpx; }

/* 选项2：五彩撒粉 */
.sprinkle-opt-mid { left: 268rpx; top: 40rpx; }
.sprinkle-dot { border-radius: 50%; width: 12rpx; height: 12rpx; position: absolute; }
.sprinkle-dot-1 { background: #ffacac; left: 36rpx; top: 50rpx; }
.sprinkle-dot-2 { background: #ffacac; left: 52rpx; top: 40rpx; }
.sprinkle-dot-3 { background: #acb3ff; left: 24rpx; top: 24rpx; }
.sprinkle-dot-4 { background: #acb3ff; left: 66rpx; top: 40rpx; }
.sprinkle-dot-5 { background: #acffc7; left: 16rpx; top: 78rpx; }
.sprinkle-dot-6 { background: #acffc7; left: 72rpx; top: 20rpx; }
.sprinkle-dot-7 { background: #fff7ac; left: 40rpx; top: 26rpx; }
.sprinkle-dot-8 { background: #fff7ac; left: 66rpx; top: 64rpx; }

/* 选项3：三角小饼干 */
.sprinkle-opt-bot { left: 272rpx; top: 380rpx; }
.sprinkle-bis-i1 { width: 32rpx; height: 32rpx; position: absolute; left: 26rpx; top: 28rpx; }
.sprinkle-bis-i2 { width: 38rpx; height: 38rpx; position: absolute; left: 56rpx; top: 26rpx; }
.sprinkle-bis-i3 { width: 32rpx; height: 32rpx; position: absolute; left: 46rpx; top: 80rpx; }
.sprinkle-bis-i4 { width: 24rpx; height: 24rpx; position: absolute; left: 22rpx; top: 58rpx; }

/* 下一步按钮 */
.btn-next { position: absolute; left: 145rpx; top: 1412rpx; width: 460rpx; height: 80rpx; }
.btn-next-bg { background: #56bfb0; border-radius: 60rpx; border: 2rpx solid #fff; width: 460rpx; height: 80rpx; position: absolute; left: 0; top: 0; }
.btn-next-text { color: #fff; text-align: center; font-family: "PingFangSc-Medium", sans-serif; font-size: 32rpx; font-weight: 500; position: absolute; left: 0; top: 50%; transform: translateY(-50%); width: 460rpx; }
</style>
