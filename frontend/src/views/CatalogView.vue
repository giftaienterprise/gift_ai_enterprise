<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import ProductCard from '@/components/ProductCard.vue'
import { listCategories, listGifts } from '@/api/catalog'
import type { Category, Gift } from '@/types/catalog'

const route = useRoute()
const router = useRouter()

const gifts = ref<Gift[]>([])
const categories = ref<Category[]>([])
const loading = ref(true)
const selectedCategory = ref<number | null>(null)

const activeGifts = computed(() =>
  gifts.value.filter((gift) => gift.is_active),
)

const filteredGifts = computed(() => {
  if (!selectedCategory.value) return activeGifts.value
  return activeGifts.value.filter(
    (gift) => gift.category_id === selectedCategory.value,
  )
})

onMounted(async () => {
  const categoryParam = route.query.category
  if (typeof categoryParam === 'string' && categoryParam) {
    selectedCategory.value = Number(categoryParam)
  }

  try {
    const [giftResult, categoryResult] = await Promise.all([
      listGifts(1, 100),
      listCategories(1, 100),
    ])
    gifts.value = giftResult.items
    categories.value = categoryResult.items.filter((item) => item.is_active)
  } catch {
    gifts.value = []
    categories.value = []
  } finally {
    loading.value = false
  }
})

function selectCategory(id: number | null) {
  selectedCategory.value = id
  router.replace({
    path: '/catalog',
    query: id ? { category: String(id) } : {},
  })
}

function openProduct(id: number) {
  router.push(`/products/${id}`)
}
</script>

<template>
  <section class="page catalog-view">
    <h1 class="page-title">礼物清单</h1>
    <p class="page-subtitle">浏览精选礼物，按分类快速筛选。</p>

    <div v-if="categories.length" class="filters">
      <button
        type="button"
        class="chip"
        :class="{ active: selectedCategory === null }"
        @click="selectCategory(null)"
      >
        全部
      </button>
      <button
        v-for="category in categories"
        :key="category.id"
        type="button"
        class="chip"
        :class="{ active: selectedCategory === category.id }"
        @click="selectCategory(category.id)"
      >
        {{ category.name }}
      </button>
    </div>

    <p v-if="loading" class="empty-state">加载中…</p>
    <div v-else-if="filteredGifts.length" class="grid-products">
      <ProductCard
        v-for="gift in filteredGifts"
        :key="gift.id"
        :product="gift"
        @open="openProduct"
      />
    </div>
    <p v-else class="empty-state">该分类暂无礼物。</p>
  </section>
</template>

<style scoped>
.filters {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 20px;
}
</style>
