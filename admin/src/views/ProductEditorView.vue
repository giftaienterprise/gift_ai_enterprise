<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { adminApi, type Brand, type Category } from '@/api/admin'
import ImageUploader from '@/components/ImageUploader.vue'
import { centsToYuan, toGiftPayload, type ProductForm } from '@/utils/productForm'

const route = useRoute()
const router = useRouter()
const id = Number(route.params.id || 0)
const categories = ref<Category[]>([])
const brands = ref<Brand[]>([])
const error = ref('')
const busy = ref(false)

const form = ref<ProductForm>({
  name: '',
  subtitle: '',
  category_id: 0,
  brand_id: 0,
  priceYuan: '0',
  cover: '',
  description: '',
  is_active: true,
  sort: 0,
})

onMounted(async () => {
  const [categoryResult, brandResult] = await Promise.all([
    adminApi.categories(),
    adminApi.brands(),
  ])
  categories.value = categoryResult.items
  brands.value = brandResult.items

  if (id) {
    const gift = await adminApi.gift(id)
    form.value = {
      name: gift.name,
      subtitle: gift.subtitle,
      category_id: gift.category_id,
      brand_id: gift.brand_id,
      priceYuan: centsToYuan(gift.price),
      cover: gift.cover,
      description: gift.description,
      is_active: gift.is_active,
      sort: gift.sort,
    }
  }
})

const save = async () => {
  busy.value = true
  error.value = ''

  try {
    const payload = toGiftPayload(form.value)
    if (id) {
      await adminApi.updateGift(id, payload)
    } else {
      await adminApi.createGift(payload)
    }
    await router.push('/products')
  } catch (reason) {
    error.value =
      reason instanceof Error && reason.message === 'PRODUCT_NAME_REQUIRED'
        ? '请输入商品名称'
        : '保存失败，请检查表单'
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <main>
    <p class="eyebrow">商品管理</p>
    <h1>{{ id ? '编辑商品' : '新增商品' }}</h1>

    <form class="editor-form" @submit.prevent="save">
      <label>
        商品名称
        <input v-model="form.name" required />
      </label>
      <label>
        副标题
        <input v-model="form.subtitle" />
      </label>

      <div class="form-row">
        <label>
          分类
          <select v-model.number="form.category_id" required>
            <option :value="0">请选择</option>
            <option v-for="item in categories" :key="item.id" :value="item.id">
              {{ item.name }}
            </option>
          </select>
        </label>
        <label>
          品牌
          <select v-model.number="form.brand_id" required>
            <option :value="0">请选择</option>
            <option v-for="item in brands" :key="item.id" :value="item.id">
              {{ item.name }}
            </option>
          </select>
        </label>
      </div>

      <div class="form-row">
        <label>
          价格（元）
          <input v-model="form.priceYuan" type="number" min="0" step="0.01" />
        </label>
        <label>
          排序
          <input v-model.number="form.sort" type="number" />
        </label>
      </div>

      <label>
        商品封面
        <ImageUploader v-model="form.cover" />
      </label>

      <label>
        商品说明
        <textarea v-model="form.description" rows="6" />
      </label>

      <label class="check-label">
        <input v-model="form.is_active" type="checkbox" />
        立即上架
      </label>

      <p v-if="error" class="form-error">{{ error }}</p>

      <button type="submit" :disabled="busy">
        {{ busy ? '保存中…' : '保存商品' }}
      </button>
    </form>
  </main>
</template>
