<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { LoaderCircle, Sparkles } from 'lucide-vue-next'
import ProductCard from '@/components/ProductCard.vue'
import ShareSheet from '@/components/ShareSheet.vue'
import { buildAdvisorGoal, runAdvisor } from '@/api/advisor'
import { listGifts } from '@/api/catalog'
import type { Gift } from '@/types/catalog'

const router = useRouter()

const relationships = ['父母', '伴侣', '朋友', '同事']
const occasions = ['生日', '节日', '纪念日', '感谢']
const budgets = ['300元以内', '300-800元', '800-2000元', '2000元以上']

const relationship = ref('')
const occasion = ref('')
const budget = ref('')
const loading = ref(false)
const answer = ref('')
const error = ref('')
const catalogGifts = ref<Gift[]>([])
const shareOpen = ref(false)

const canSubmit = computed(
  () => Boolean(relationship.value && occasion.value && budget.value),
)

const goal = computed(() => {
  if (!canSubmit.value) return ''
  return buildAdvisorGoal(relationship.value, occasion.value, budget.value)
})

const recommendedGifts = computed(() =>
  catalogGifts.value.filter((gift) => gift.is_active).slice(0, 4),
)

const shareUrl = computed(() =>
  typeof window !== 'undefined' ? window.location.href : '/advisor',
)

onMounted(async () => {
  try {
    const result = await listGifts(1, 20)
    catalogGifts.value = result.items
  } catch {
    catalogGifts.value = []
  }
})

function selectRelationship(value: string) {
  relationship.value = value
}

function selectOccasion(value: string) {
  occasion.value = value
}

function selectBudget(value: string) {
  budget.value = value
}

async function submitAdvisor() {
  if (!canSubmit.value) return
  loading.value = true
  error.value = ''
  answer.value = ''

  try {
    const token = sessionStorage.getItem('gift-ai:token') ?? undefined
    const result = await runAdvisor(goal.value, token)
    if (result.success && result.final_answer) {
      answer.value = result.final_answer
    } else {
      error.value = result.error || '暂时无法生成建议，已为你展示精选礼物。'
    }
  } catch {
    error.value = '暂时无法连接 AI 参谋，已为你展示精选礼物。'
  } finally {
    loading.value = false
  }
}

function openProduct(id: number) {
  router.push(`/products/${id}`)
}
</script>

<template>
  <section class="page advisor-view">
    <div class="hero card">
      <p class="eyebrow">智能咨询</p>
      <h1 class="page-title">告诉我送礼场景</h1>
      <p class="page-subtitle">选择关系、场合和预算，AI 会给出更贴心的礼物建议。</p>
    </div>

    <div class="choice-group">
      <h2>送给谁？</h2>
      <div class="choices">
        <button
          v-for="item in relationships"
          :key="item"
          type="button"
          class="chip"
          :class="{ active: relationship === item }"
          @click="selectRelationship(item)"
        >
          {{ item }}
        </button>
      </div>
    </div>

    <div class="choice-group">
      <h2>什么场合？</h2>
      <div class="choices">
        <button
          v-for="item in occasions"
          :key="item"
          type="button"
          class="chip"
          :class="{ active: occasion === item }"
          @click="selectOccasion(item)"
        >
          {{ item }}
        </button>
      </div>
    </div>

    <div class="choice-group">
      <h2>预算范围？</h2>
      <div class="choices">
        <button
          v-for="item in budgets"
          :key="item"
          type="button"
          class="chip"
          :class="{ active: budget === item }"
          @click="selectBudget(item)"
        >
          {{ item }}
        </button>
      </div>
    </div>

    <p v-if="goal" class="goal-preview" data-testid="goal-preview">{{ goal }}</p>

    <div class="actions">
      <button
        type="button"
        class="btn btn-primary"
        :disabled="!canSubmit || loading"
        @click="submitAdvisor"
      >
        <LoaderCircle v-if="loading" :size="18" class="spin" />
        <Sparkles v-else :size="18" />
        获取礼物建议
      </button>
      <button
        v-if="goal"
        type="button"
        class="btn btn-secondary"
        @click="shareOpen = true"
      >
        分享咨询结果
      </button>
    </div>

    <div v-if="answer" class="answer card">
      <h2>AI 建议</h2>
      <p>{{ answer }}</p>
    </div>

    <p v-if="error" class="notice">{{ error }}</p>

    <div v-if="recommendedGifts.length" class="recommendations">
      <h2>精选礼物</h2>
      <div class="grid-products">
        <ProductCard
          v-for="gift in recommendedGifts"
          :key="gift.id"
          :product="gift"
          @open="openProduct"
        />
      </div>
    </div>

    <ShareSheet
      :open="shareOpen"
      :title="'AI送礼参谋'"
      :text="goal || '发现更贴心的礼物'"
      :url="shareUrl"
      @close="shareOpen = false"
    />
  </section>
</template>

<style scoped>
.hero {
  padding: 24px;
  margin-bottom: 24px;
}

.eyebrow {
  margin: 0 0 8px;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--coral);
}

.choice-group {
  margin-bottom: 20px;
}

.choice-group h2 {
  margin: 0 0 12px;
  font-size: 1rem;
}

.choices {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.goal-preview {
  padding: 12px 16px;
  border-radius: var(--radius-sm);
  background: rgba(255, 98, 95, 0.08);
  color: var(--ink);
}

.actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 24px;
}

.answer {
  padding: 20px;
  margin-bottom: 20px;
}

.answer h2 {
  margin: 0 0 8px;
  font-size: 1rem;
}

.answer p {
  margin: 0;
  line-height: 1.7;
  white-space: pre-wrap;
}

.notice {
  margin: 0 0 20px;
  color: var(--muted);
}

.recommendations h2 {
  margin: 0 0 16px;
  font-size: 1.125rem;
}

.spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
