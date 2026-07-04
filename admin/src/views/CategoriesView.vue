<script setup lang="ts">
import { onMounted, ref } from 'vue'

import { adminApi, type Category } from '@/api/admin'
import DataTable from '@/components/DataTable.vue'

const items = ref<Category[]>([])
const name = ref('')
const error = ref('')

const load = async () => {
  items.value = (await adminApi.categories()).items
}

const add = async () => {
  if (!name.value.trim()) {
    return
  }

  error.value = ''
  try {
    await adminApi.createCategory({
      name: name.value.trim(),
      sort: 0,
      is_active: true,
    })
    name.value = ''
    await load()
  } catch (reason) {
    error.value = reason instanceof Error ? reason.message : '创建失败'
  }
}

const toggle = async (item: Category) => {
  await adminApi.updateCategory(item.id, { is_active: !item.is_active })
  await load()
}

const remove = async (item: Category) => {
  if (!confirm(`确定删除“${item.name}”吗？`)) {
    return
  }

  try {
    await adminApi.deleteCategory(item.id)
    await load()
  } catch (reason) {
    error.value = reason instanceof Error ? reason.message : '删除失败，可能仍有关联商品'
  }
}

onMounted(load)
</script>

<template>
  <main>
    <p class="eyebrow">内容管理</p>
    <h1>分类管理</h1>

    <form class="inline-form" @submit.prevent="add">
      <input v-model="name" placeholder="新分类名称" />
      <button type="submit">新增分类</button>
    </form>

    <p v-if="error" class="form-error">{{ error }}</p>

    <DataTable :headers="['名称', '排序', '状态', '操作']">
      <tr v-for="item in items" :key="item.id">
        <td>{{ item.name }}</td>
        <td>{{ item.sort }}</td>
        <td>{{ item.is_active ? '启用' : '停用' }}</td>
        <td>
          <button type="button" @click="toggle(item)">
            {{ item.is_active ? '停用' : '启用' }}
          </button>
          <button class="text-danger" type="button" @click="remove(item)">删除</button>
        </td>
      </tr>
    </DataTable>
  </main>
</template>
