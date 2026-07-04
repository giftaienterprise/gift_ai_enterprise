<script setup lang="ts">
import { onMounted, ref } from 'vue'

import { adminApi, type Gift } from '@/api/admin'
import DataTable from '@/components/DataTable.vue'

const items = ref<Gift[]>([])

const load = async () => {
  items.value = (await adminApi.gifts()).items
}

const remove = async (gift: Gift) => {
  if (!confirm(`确定删除“${gift.name}”吗？`)) {
    return
  }
  await adminApi.deleteGift(gift.id)
  await load()
}

onMounted(load)
</script>

<template>
  <main>
    <div class="page-title">
      <div>
        <p class="eyebrow">内容管理</p>
        <h1>商品管理</h1>
      </div>
      <RouterLink class="primary-button button-link" to="/products/new">
        新增商品
      </RouterLink>
    </div>

    <DataTable :headers="['商品', '价格', '状态', '排序', '操作']">
      <tr v-for="gift in items" :key="gift.id">
        <td>
          <div class="item-cell">
            <img :src="gift.cover || '/admin/assets/placeholder.png'" alt="" />
            <strong>{{ gift.name }}</strong>
          </div>
        </td>
        <td>¥{{ (gift.price / 100).toFixed(2) }}</td>
        <td>
          <span class="status" :class="{ off: !gift.is_active }">
            {{ gift.is_active ? '已上架' : '已下架' }}
          </span>
        </td>
        <td>{{ gift.sort }}</td>
        <td>
          <RouterLink :to="`/products/${gift.id}`">编辑</RouterLink>
          <button class="text-danger" type="button" @click="remove(gift)">删除</button>
        </td>
      </tr>
    </DataTable>
  </main>
</template>
