<script setup lang="ts">
import { ref } from 'vue'

import { adminApi } from '@/api/admin'

defineProps<{
  modelValue: string
}>()

const emit = defineEmits<{
  (event: 'update:modelValue', value: string): void
}>()

const busy = ref(false)
const error = ref('')

const upload = async (event: Event) => {
  const file = (event.target as HTMLInputElement).files?.[0]
  if (!file) {
    return
  }

  busy.value = true
  error.value = ''

  try {
    const result = await adminApi.upload(file)
    emit('update:modelValue', result.image_url)
  } catch {
    error.value = '上传失败，请检查图片格式和大小'
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <div class="image-uploader">
    <img v-if="modelValue" :src="modelValue" alt="当前图片" />
    <label>
      {{ busy ? '上传中…' : '上传图片' }}
      <input
        type="file"
        accept="image/jpeg,image/png,image/webp"
        :disabled="busy"
        @change="upload"
      />
    </label>
    <small v-if="error">{{ error }}</small>
  </div>
</template>
