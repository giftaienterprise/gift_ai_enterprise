<script setup lang="ts">
import { onMounted, ref } from 'vue'

import { adminApi, type AdminSummary } from '@/api/admin'

const data = ref<AdminSummary | null>(null)

onMounted(async () => {
  data.value = await adminApi.summary()
})
</script>

<template>
  <main>
    <p class="eyebrow">概览</p>
    <h1>仪表盘</h1>

    <div v-if="data" class="stat-grid">
      <article>
        <span>全部商品</span>
        <strong>{{ data.gift_count }}</strong>
      </article>
      <article>
        <span>上架商品</span>
        <strong>{{ data.active_gift_count }}</strong>
      </article>
      <article>
        <span>分类</span>
        <strong>{{ data.category_count }}</strong>
      </article>
      <article>
        <span>品牌</span>
        <strong>{{ data.brand_count }}</strong>
      </article>
    </div>

    <section class="panel">
      <h2>最近更新</h2>
      <ul v-if="data">
        <li v-for="gift in data.recent_gifts" :key="gift.id">
          {{ gift.name }}
          <span>{{ gift.is_active ? '已上架' : '已下架' }}</span>
        </li>
      </ul>
    </section>
  </main>
</template>
