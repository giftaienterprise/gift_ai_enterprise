<script setup lang="ts">
import type { RecommendedGift } from '@/types/advisor'

defineProps<{
  gift: RecommendedGift
}>()

defineEmits<{
  open: [id: string]
}>()

function formatPrice(price: number) {
  return `¥${(price / 100).toFixed(0)}`
}
</script>

<template>
  <article class="gift-card" @click="$emit('open', gift.id)">
    <div class="gift-img">{{ gift.emoji }}</div>
    <div class="gift-info">
      <div class="gift-name">{{ gift.name }}</div>
      <div class="gift-reason">"{{ gift.reason }}"</div>
      <div class="gift-meta">
        <span class="gift-price">{{ formatPrice(gift.price) }}</span>
        <span class="tag">查看详情</span>
      </div>
    </div>
  </article>
</template>

<style scoped>
.gift-card {
  border: 1px solid #f0f0f0;
  border-radius: 12px;
  padding: 12px;
  margin-bottom: 8px;
  display: flex;
  gap: 12px;
  cursor: pointer;
  background: #fff;
}

.gift-img {
  width: 80px;
  height: 80px;
  border-radius: 10px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 36px;
  flex-shrink: 0;
}

.gift-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.gift-name {
  font-weight: 600;
  font-size: 15px;
}

.gift-reason {
  font-size: 12px;
  color: #999;
  line-height: 1.4;
}

.gift-meta {
  display: flex;
  align-items: center;
  gap: 8px;
}

.gift-price {
  font-weight: 700;
  color: #ff6b6b;
  font-size: 16px;
}

.tag {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 11px;
  background: #fff0f0;
  color: #ff6b6b;
}
</style>
