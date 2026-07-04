<script setup lang="ts">
import { computed } from 'vue'
import { Heart } from 'lucide-vue-next'
import { formatPriceYuan } from '@/api/catalog'
import { useFavorites } from '@/stores/favorites'
import type { Gift } from '@/types/catalog'

const props = defineProps<{
  product: Gift
}>()

const emit = defineEmits<{
  open: [id: number]
}>()

const { isFavorite, toggle } = useFavorites()

const priceLabel = computed(() => formatPriceYuan(props.product.price))
const favorited = computed(() => isFavorite(props.product.id))

function handleOpen() {
  emit('open', props.product.id)
}

function handleFavorite(event: Event) {
  event.stopPropagation()
  toggle(props.product.id)
}
</script>

<template>
  <article class="product-card card" @click="handleOpen">
    <div class="cover-wrap">
      <img
        v-if="product.cover"
        :src="product.cover"
        :alt="product.name"
        class="cover"
      />
      <div v-else class="cover cover-placeholder">礼物</div>
      <button
        type="button"
        class="favorite-btn"
        :class="{ active: favorited }"
        :aria-label="favorited ? '取消收藏' : '收藏'"
        @click="handleFavorite"
      >
        <Heart :size="18" :fill="favorited ? 'currentColor' : 'none'" />
      </button>
    </div>
    <div class="body">
      <h3 class="name">{{ product.name }}</h3>
      <p v-if="product.subtitle" class="subtitle">{{ product.subtitle }}</p>
      <p class="price">{{ priceLabel }}</p>
    </div>
  </article>
</template>

<style scoped>
.product-card {
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.15s ease;
}

.product-card:active {
  transform: scale(0.98);
}

.cover-wrap {
  position: relative;
  aspect-ratio: 1;
  background: var(--surface-muted);
}

.cover {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.cover-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--muted);
  font-size: 1.25rem;
}

.favorite-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border: none;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.92);
  color: var(--muted);
}

.favorite-btn.active {
  color: var(--coral);
}

.body {
  padding: 12px;
}

.name {
  margin: 0;
  font-size: 0.95rem;
  font-weight: 600;
  line-height: 1.35;
}

.subtitle {
  margin: 4px 0 0;
  font-size: 0.8rem;
  color: var(--muted);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.price {
  margin: 8px 0 0;
  font-size: 1rem;
  font-weight: 700;
  color: var(--coral);
}
</style>
