<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Heart, Share2, ShoppingBag } from 'lucide-vue-next'
import ContactSheet from '@/components/ContactSheet.vue'
import ShareSheet from '@/components/ShareSheet.vue'
import { formatPriceYuan, getGift, getPublicSettings } from '@/api/catalog'
import { useFavorites } from '@/stores/favorites'
import type { Gift, PublicSettings } from '@/types/catalog'

const route = useRoute()
const router = useRouter()
const { isFavorite, toggle } = useFavorites()

const gift = ref<Gift | null>(null)
const settings = ref<PublicSettings | null>(null)
const loading = ref(true)
const contactOpen = ref(false)
const shareOpen = ref(false)

const giftId = computed(() => Number(route.params.id))

const priceLabel = computed(() =>
  gift.value ? formatPriceYuan(gift.value.price) : '',
)

const favorited = computed(() =>
  gift.value ? isFavorite(gift.value.id) : false,
)

const shareUrl = computed(() =>
  typeof window !== 'undefined'
    ? `${window.location.origin}/products/${giftId.value}`
    : `/products/${giftId.value}`,
)

onMounted(async () => {
  if (!giftId.value || Number.isNaN(giftId.value)) {
    router.replace('/catalog')
    return
  }

  try {
    const [giftData, publicSettings] = await Promise.all([
      getGift(giftId.value),
      getPublicSettings(),
    ])
    if (!giftData.is_active) {
      router.replace('/catalog')
      return
    }
    gift.value = giftData
    settings.value = publicSettings
  } catch {
    router.replace('/catalog')
  } finally {
    loading.value = false
  }
})

function toggleFavorite() {
  if (gift.value) toggle(gift.value.id)
}
</script>

<template>
  <section class="page product-view">
    <p v-if="loading" class="empty-state">加载中…</p>

    <template v-else-if="gift">
      <div class="product-layout">
        <div class="media card">
          <img
            v-if="gift.cover"
            :src="gift.cover"
            :alt="gift.name"
            class="cover"
          />
          <div v-else class="cover cover-placeholder">礼物</div>
        </div>

        <div class="details">
          <p v-if="gift.brand?.name" class="brand">{{ gift.brand.name }}</p>
          <h1 class="page-title">{{ gift.name }}</h1>
          <p v-if="gift.subtitle" class="page-subtitle">{{ gift.subtitle }}</p>
          <p class="price">{{ priceLabel }}</p>

          <p v-if="gift.description" class="description">{{ gift.description }}</p>

          <div class="actions">
            <button type="button" class="btn btn-primary" @click="contactOpen = true">
              <ShoppingBag :size="18" />
              联系购买
            </button>
            <button type="button" class="btn btn-secondary" @click="toggleFavorite">
              <Heart :size="18" :fill="favorited ? 'currentColor' : 'none'" />
              {{ favorited ? '已收藏' : '收藏' }}
            </button>
            <button type="button" class="btn btn-secondary" @click="shareOpen = true">
              <Share2 :size="18" />
              分享
            </button>
          </div>
        </div>
      </div>

      <ContactSheet
        :open="contactOpen"
        :settings="settings"
        @close="contactOpen = false"
      />

      <ShareSheet
        :open="shareOpen"
        :title="gift.name"
        :text="gift.subtitle || settings?.share_description || '发现更贴心的礼物'"
        :url="shareUrl"
        @close="shareOpen = false"
      />
    </template>
  </section>
</template>

<style scoped>
.product-layout {
  display: grid;
  gap: 24px;
}

@media (min-width: 960px) {
  .product-layout {
    grid-template-columns: 1fr 1fr;
    align-items: start;
  }
}

.media {
  overflow: hidden;
}

.cover {
  width: 100%;
  aspect-ratio: 1;
  object-fit: cover;
}

.cover-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  aspect-ratio: 1;
  background: var(--surface-muted);
  color: var(--muted);
  font-size: 2rem;
}

.brand {
  margin: 0 0 4px;
  color: var(--muted);
  font-size: 0.875rem;
}

.price {
  margin: 0 0 16px;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--coral);
}

.description {
  margin: 0 0 24px;
  line-height: 1.7;
  color: var(--ink);
}

.actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
</style>
