<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { Sparkles } from 'lucide-vue-next'
import ProductCard from '@/components/ProductCard.vue'
import { listGifts } from '@/api/catalog'
import type { Gift } from '@/types/catalog'

const router = useRouter()
const gifts = ref<Gift[]>([])
const loading = ref(true)

onMounted(async () => {
  try {
    const result = await listGifts(1, 6)
    gifts.value = result.items.filter((item) => item.is_active)
  } catch {
    gifts.value = []
  } finally {
    loading.value = false
  }
})

function openProduct(id: number) {
  router.push(`/products/${id}`)
}

function goAdvisor() {
  router.push('/advisor')
}

function goCatalog() {
  router.push('/catalog')
}
</script>

<template>
  <section class="page home-view">
    <div class="hero card">
      <p class="eyebrow">AI 送礼参谋</p>
      <h1 class="page-title">今天想为谁准备心意？</h1>
      <p class="page-subtitle">
        告诉我关系、场合和预算，我会帮你从精选礼物中找到更贴心的选择。
      </p>
      <button type="button" class="btn btn-primary hero-cta" @click="goAdvisor">
        <Sparkles :size="18" />
        开始咨询
      </button>
    </div>

    <div class="section-head">
      <h2>精选礼物</h2>
      <button type="button" class="btn btn-ghost" @click="goCatalog">查看全部</button>
    </div>

    <p v-if="loading" class="empty-state">加载中…</p>
    <div v-else-if="gifts.length" class="grid-products">
      <ProductCard
        v-for="gift in gifts"
        :key="gift.id"
        :product="gift"
        @open="openProduct"
      />
    </div>
    <p v-else class="empty-state">暂无礼物，稍后再来看看吧。</p>
  </section>
</template>

<style scoped>
.hero {
  padding: 28px 24px;
  margin-bottom: 24px;
  background:
    radial-gradient(circle at top right, rgba(255, 135, 77, 0.18), transparent 55%),
    #fff;
}

.eyebrow {
  margin: 0 0 8px;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--coral);
}

.hero-cta {
  margin-top: 8px;
}

.section-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.section-head h2 {
  margin: 0;
  font-size: 1.125rem;
}
</style>
