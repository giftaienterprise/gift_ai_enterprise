<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import ProductCard from '@/components/ProductCard.vue'
import { listGifts } from '@/api/catalog'
import { useFavorites } from '@/stores/favorites'
import type { Gift } from '@/types/catalog'

const router = useRouter()
const { ids, filterGifts } = useFavorites()

const gifts = ref<Gift[]>([])
const loading = ref(true)
const compareIds = ref<number[]>([])

const savedGifts = computed(() => filterGifts(gifts.value))

const compareGifts = computed(() =>
  savedGifts.value.filter((gift) => compareIds.value.includes(gift.id)),
)

onMounted(async () => {
  try {
    const result = await listGifts(1, 200)
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

function toggleCompare(id: number) {
  if (compareIds.value.includes(id)) {
    compareIds.value = compareIds.value.filter((item) => item !== id)
    return
  }
  if (compareIds.value.length >= 4) return
  compareIds.value = [...compareIds.value, id]
}
</script>

<template>
  <section class="page saved-view">
    <h1 class="page-title">我的收藏</h1>
    <p class="page-subtitle">
      已收藏 {{ ids.length }} 件礼物，最多可选 4 件进行对比。
    </p>

    <div v-if="compareIds.length" class="compare-bar card">
      <p>对比中：{{ compareIds.length }}/4</p>
      <ul class="compare-list">
        <li v-for="gift in compareGifts" :key="gift.id">{{ gift.name }}</li>
      </ul>
    </div>

    <p v-if="loading" class="empty-state">加载中…</p>
    <div v-else-if="savedGifts.length" class="saved-grid">
      <div v-for="gift in savedGifts" :key="gift.id" class="saved-item">
        <ProductCard :product="gift" @open="openProduct" />
        <label class="compare-toggle">
          <input
            type="checkbox"
            :checked="compareIds.includes(gift.id)"
            :disabled="!compareIds.includes(gift.id) && compareIds.length >= 4"
            @change="toggleCompare(gift.id)"
          />
          加入对比
        </label>
      </div>
    </div>
    <p v-else class="empty-state">还没有收藏，去清单页逛逛吧。</p>
  </section>
</template>

<style scoped>
.compare-bar {
  padding: 16px;
  margin-bottom: 20px;
}

.compare-bar p {
  margin: 0 0 8px;
  font-weight: 600;
}

.compare-list {
  margin: 0;
  padding-left: 18px;
  color: var(--muted);
}

.saved-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}

.saved-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.compare-toggle {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.875rem;
  color: var(--muted);
}

@media (min-width: 960px) {
  .saved-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}
</style>
