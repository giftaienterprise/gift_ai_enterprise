<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import LoadingOverlay from '@/components/LoadingOverlay.vue'
import { recommendGifts } from '@/api/recommend'
import { useRecommendations } from '@/stores/recommendations'

const route = useRoute()
const router = useRouter()
const { saveResult } = useRecommendations()

const relations = ['恋人', '父母', '朋友', '孩子', '同事', '客户']
const scenes = ['生日', '纪念日', '乔迁', '探病', '道歉', '感谢', '新年']
const budgets = [
  { label: '¥200以下', value: '0-200' },
  { label: '¥200-500', value: '200-500' },
  { label: '¥500-1k', value: '500-1000' },
  { label: '¥1k-3k', value: '1000-3000' },
]

const relation = ref('恋人')
const scene = ref('生日')
const budget = ref('200-500')
const note = ref('')
const platform = ref<'taobao' | 'jd'>('taobao')
const loading = ref(false)

const canSubmit = computed(
  () => Boolean(relation.value && scene.value && budget.value),
)

onMounted(() => {
  const preset = route.query.relation
  if (typeof preset === 'string' && relations.includes(preset)) {
    relation.value = preset
  }
})

async function submit() {
  if (!canSubmit.value || loading.value) return
  loading.value = true
  try {
    const result = await recommendGifts({
      relation: relation.value,
      scene: scene.value,
      budget: budget.value,
      note: note.value,
      platform: platform.value,
    })
    saveResult(result)
    router.push('/result')
  } catch {
    window.alert('推荐生成失败，请稍后重试')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <section class="page demand-page">
    <div class="page-head">
      <button type="button" class="back" @click="router.push('/')">←</button>
      <span class="title">描述需求</span>
      <span class="step">步骤 1/3</span>
    </div>

    <h3>1. 选择送礼对象</h3>
    <div class="chip-scroll">
      <button
        v-for="item in relations"
        :key="item"
        type="button"
        class="chip"
        :class="{ selected: relation === item }"
        @click="relation = item"
      >
        {{ item }}
      </button>
    </div>

    <h3>2. 这是什么场合？</h3>
    <div class="chip-group">
      <button
        v-for="item in scenes"
        :key="item"
        type="button"
        class="chip"
        :class="{ selected: scene === item }"
        @click="scene = item"
      >
        {{ item }}
      </button>
    </div>

    <h3>3. 预算大概多少？</h3>
    <div class="segment-group">
      <button
        v-for="item in budgets"
        :key="item.value"
        type="button"
        class="segment-item"
        :class="{ selected: budget === item.value }"
        @click="budget = item.value"
      >
        {{ item.label }}
      </button>
    </div>

    <h3>4. 购买平台</h3>
    <div class="segment-group platform-group">
      <button
        type="button"
        class="segment-item"
        :class="{ selected: platform === 'taobao' }"
        @click="platform = 'taobao'"
      >
        淘宝
      </button>
      <button
        type="button"
        class="segment-item"
        :class="{ selected: platform === 'jd' }"
        @click="platform = 'jd'"
      >
        京东
      </button>
    </div>

    <h3>5. 补充信息（让推荐更准）</h3>
    <textarea
      v-model="note"
      class="input-area"
      rows="3"
      placeholder="例：男友是程序员，喜欢游戏和咖啡"
    />

    <button
      type="button"
      class="btn btn-primary"
      :disabled="!canSubmit || loading"
      @click="submit"
    >
      生成推荐方案
    </button>

    <LoadingOverlay :show="loading" />
  </section>
</template>

<style scoped>
.page-head {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.back {
  border: none;
  background: transparent;
  font-size: 24px;
  cursor: pointer;
}

.title {
  font-size: 18px;
  font-weight: 600;
  margin-left: 12px;
}

.step {
  margin-left: auto;
  color: #ff6b6b;
  font-size: 13px;
}

h3 {
  margin: 0 0 10px;
  font-size: 15px;
}

.chip-scroll,
.chip-group {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 20px;
}

.chip-scroll {
  overflow-x: auto;
  flex-wrap: nowrap;
  padding-bottom: 8px;
}

.chip,
.segment-item {
  border: 2px solid transparent;
  background: #f5f5f5;
  border-radius: 25px;
  padding: 10px 18px;
  font-size: 14px;
  cursor: pointer;
}

.chip.selected {
  background: #fff0f0;
  border-color: #ff6b6b;
  color: #ff6b6b;
  font-weight: 600;
}

.segment-group {
  display: flex;
  border-radius: 12px;
  overflow: hidden;
  border: 2px solid #f0f0f0;
  margin-bottom: 20px;
}

.segment-item {
  flex: 1;
  border-radius: 0;
  border-right: 1px solid #f0f0f0;
}

.segment-item:last-child {
  border-right: none;
}

.segment-item.selected {
  background: #ff6b6b;
  color: #fff;
  font-weight: 600;
}

.input-area {
  width: 100%;
  padding: 14px;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  font-size: 14px;
  resize: none;
  font-family: inherit;
}

.input-area:focus {
  outline: none;
  border-color: #ff6b6b;
}

.btn-primary {
  width: 100%;
  margin-top: 20px;
  padding: 16px;
  border: none;
  border-radius: 50px;
  font-size: 18px;
  font-weight: 600;
  color: #fff;
  background: linear-gradient(135deg, #ff6b6b, #ff8e53);
  cursor: pointer;
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
