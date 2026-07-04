<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import GiftRecommendCard from '@/components/GiftRecommendCard.vue'
import { useRecommendations } from '@/stores/recommendations'
import { useShare } from '@/composables/useShare'

const router = useRouter()
const { current } = useRecommendations()
const { shareContent } = useShare()

const result = computed(() => current.value)

onMounted(() => {
  if (!result.value) {
    router.replace('/demand')
  }
})

async function shareList() {
  if (!result.value) return
  const text = `${result.value.combo_title}\n${result.value.gifts
    .map((gift) => `${gift.name} ${gift.reason}`)
    .join('\n')}`
  await shareContent({
    title: result.value.combo_title,
    text,
    url: window.location.href,
  })
}

function openGift(id: string) {
  router.push(`/recommend/${id}`)
}
</script>

<template>
  <section v-if="result" class="page result-page">
    <div class="page-head">
      <button type="button" class="back" @click="router.push('/demand')">←</button>
      <span class="title">推荐结果</span>
    </div>

    <div class="summary card">
      <div>
        为 <b>{{ result.relation }}</b> 在 <b>{{ result.scene }}</b> 的推荐方案
      </div>
      <div class="muted">预算范围：¥{{ result.budget }}</div>
    </div>

    <div class="combo-title">{{ result.combo_title }}</div>

    <GiftRecommendCard
      v-for="gift in result.gifts"
      :key="gift.id"
      :gift="gift"
      @open="openGift"
    />

    <div class="actions-row">
      <button type="button" class="btn btn-outline" @click="router.push('/demand')">
        调整需求
      </button>
      <button type="button" class="btn btn-outline" @click="shareList">
        分享清单
      </button>
    </div>
  </section>
</template>

<style scoped>
.page-head {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
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

.summary {
  background: linear-gradient(135deg, #fff5f5, #fff0f0);
  border: 2px solid #ffe0e0;
  border-radius: 16px;
  padding: 16px;
  margin-bottom: 16px;
}

.muted {
  margin-top: 4px;
  color: #999;
  font-size: 13px;
}

.combo-title {
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 12px;
}

.actions-row {
  display: flex;
  gap: 10px;
  margin-top: 16px;
}

.btn-outline {
  flex: 1;
  padding: 10px 16px;
  border-radius: 20px;
  border: 2px solid #ff6b6b;
  background: #fff;
  color: #ff6b6b;
  cursor: pointer;
}
</style>
