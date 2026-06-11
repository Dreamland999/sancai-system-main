/**
 * 食材 / 配方 / 食养局 相关接口
 *
 * 当前为 mock 模式。
 */

import { isMock, mock } from '@/utils/request.js'

// ─── 食材库 ────────────────────────────────────────

// 获取食材列表（可按匣/品类筛选）
export async function getIngredients(category) {
  if (isMock()) {
    const base = [
      { id: 'jasmine', name: '茉莉花茶', category: '安神匣' },
      { id: 'mint', name: '薄荷叶', category: '安神匣' },
      { id: 'rose', name: '玫瑰花', category: '舒愉匣' },
      { id: 'oolong', name: '乌龙茶叶', category: '百料匣' },
      { id: 'chrysanthemum', name: '菊花', category: '解郁匣' },
    ]
    return mock(category ? base.filter(i => i.category === category) : base)()
  }
  // TODO: get('/api/ingredients', { category })
}

// ─── 配方详情 ──────────────────────────────────────

// 获取配方详情
export async function getRecipeDetail(recipeId) {
  if (isMock()) {
    return mock({
      id: 'mock-recipe-001',
      name: '桃气西瓜冰沙',
      ingredients: ['西瓜', '桃子', '茉莉花茶'],
      effects: ['清热解暑', '平复烦躁'],
      suitable: ['烦躁', '湿热上火', '想放松'],
      steps: ['选择基底：茉莉花茶', '加入西瓜汁', '加入桃子泥'],
    })()
  }
  // TODO: get('/api/recipes/' + recipeId)
}

// 获取推荐配方列表
export async function getRecipeList(filter) {
  if (isMock()) {
    return mock([
      { id: 'r001', name: '桃气西瓜冰沙', category: '安神' },
      { id: 'r002', name: '薄荷柠檬茶', category: '解郁' },
      { id: 'r003', name: '玫瑰乌龙奶茶', category: '舒愉' },
    ])()
  }
  // TODO: get('/api/recipes', filter)
}

// ─── 自定义配方 ────────────────────────────────────

// 提交用户调整后的配方参数
export async function submitCustomRecipe(params) {
  if (isMock()) return mock({ ok: true, recipe_id: 'custom-001' })()
  // TODO: post('/api/recipes/custom', params)
}
