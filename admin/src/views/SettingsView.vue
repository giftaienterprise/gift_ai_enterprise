<script setup lang="ts">
import { onMounted, ref } from 'vue'

import { adminApi, type SiteSettings } from '@/api/admin'
import ImageUploader from '@/components/ImageUploader.vue'
import { validateSettings } from '@/utils/settingsForm'

const form = ref<SiteSettings>({
  wechat_id: '',
  wechat_qr_url: '',
  phone: '',
  share_title: 'AI送礼参谋',
  share_description: '发现更贴心的礼物',
  share_image_url: '',
})

const status = ref('')
const error = ref('')
const busy = ref(false)

onMounted(async () => {
  form.value = await adminApi.settings()
})

const save = async () => {
  busy.value = true
  status.value = ''
  error.value = ''

  try {
    validateSettings(form.value)
    form.value = await adminApi.updateSettings(form.value)
    status.value = '设置已保存，商城会立即读取新内容'
  } catch (reason) {
    error.value =
      reason instanceof Error && reason.message === 'INVALID_PHONE'
        ? '请输入有效联系电话'
        : '保存失败，请稍后重试'
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <main>
    <p class="eyebrow">商城配置</p>
    <h1>联系与分享</h1>

    <form class="editor-form settings-form" @submit.prevent="save">
      <h2>联系购买</h2>
      <label>
        微信号
        <input v-model="form.wechat_id" placeholder="企业或客服微信号" />
      </label>
      <label>
        微信二维码
        <ImageUploader v-model="form.wechat_qr_url" />
      </label>
      <label>
        联系电话
        <input v-model="form.phone" placeholder="例如 400-800-1234" />
      </label>

      <h2>分享内容</h2>
      <label>
        分享标题
        <input v-model="form.share_title" maxlength="150" />
      </label>
      <label>
        分享说明
        <textarea v-model="form.share_description" rows="4" maxlength="500" />
      </label>
      <label>
        默认分享封面
        <ImageUploader v-model="form.share_image_url" />
      </label>

      <p v-if="error" class="form-error">{{ error }}</p>
      <p v-if="status" class="form-success" role="status">{{ status }}</p>

      <button type="submit" :disabled="busy">
        {{ busy ? '保存中…' : '保存设置' }}
      </button>
    </form>
  </main>
</template>
