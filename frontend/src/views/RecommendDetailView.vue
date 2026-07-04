<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useRecommendations } from '@/stores/recommendations'

const route = useRoute()
const router = useRouter()
const { getGift } = useRecommendations()
const saved = ref(false)

const gift = computed(() => getGift(String(route.params.id)))

onMounted(() => {
  if (!gift.value) {
    router.replace('/demand')
  }
})

const priceLabel = computed(() =>
  gift.value ? `¥${(gift.value.price / 100).toFixed(0)}` : '',
)

function buyNow() {
  if (gift.value?.purchase_url) {
    window.open(gift.value.purchase_url, '_blank', 'noopener,noreferrer')
  }
}

function toggleSaved() {
  saved.value = !saved.value
}
</script>

<template>
  <section v-if="gift" class="page detail-page">
    <div class="page-head">
      <button type="button" class="back" @click="router.back()">←</button>
      <span class="title">商品详情</span>
      <button type="button" class="fav" @click="toggleSaved">
        {{ saved ? '❤️' : '🤍' }}
      </button>
    </div>

    <div class="hero-emoji">{{ gift.emoji }}</div>

    <div class="ai-comment">
      <div class="ai-title">AI 参谋点评</div>
      <div v-if="gift.match">★ 匹配度: {{ gift.match }}</div>
      <div v-if="gift.meaning">💡 送礼寓意: "{{ gift.meaning }}"</div>
      <div v-if="gift.tip">✍️ 小贴士: {{ gift.tip }}</div>
    </div>

    <h2>{{ gift.name }}</h2>
    <div class="meta">
      <span class="price">{{ priceLabel }}</span>
      <span v-for="tag in gift.tags" :key="tag" class="tag">{{ tag }}</span>
    </div>
    <p class="reason">"{{ gift.reason }}"</p>

    <div class="actions">
      <button type="button" class="btn btn-outline" @click="toggleSaved">
        加入清单
      </button>
      <button type="button" class="btn btn-primary" @click="buyNow">
        去购买
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

.back,
.fav {
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

.fav {
  margin-left: auto;
}

.hero-emoji {
  width: 100%;
  height: 220px;
  border-radius: 16px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 80px;
  margin-bottom: 16px;
}

.ai-comment {
  background: linear-gradient(135deg, #fff5f5, #fff0f0);
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 16px;
  border-left: 4px solid #ff6b6b;
  font-size: 13px;
  line-height: 1.6;
}

.ai-title {
  font-weight: 600;
  margin-bottom: 8px;
}

h2 {
  margin: 0 0 8px;
}

.meta {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.price {
  font-size: 24px;
  font-weight: 700;
  color: #ff6b6b;
}

.tag {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 11px;
  background: #fff0f0;
  color: #ff6b6b;
}

.reason {
  color: #666;
  margin: 12px 0 20px;
}

.actions {
  display: flex;
  gap: 10px;
}

.btn {
  flex: 1;
  padding: 12px 16px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
}

.btn-outline {
  border: 2px solid #ff6b6b;
  background: #fff;
  color: #ff6b6b;
}

.btn-primary {
  border: none;
  background: linear-gradient(135deg, #ff6b6b, #ff8e53);
  color: #fff;
}
</style>
