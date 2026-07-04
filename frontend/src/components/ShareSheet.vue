<script setup lang="ts">
import { ref, watch } from 'vue'
import QRCode from 'qrcode'
import { Copy, Share2, X } from 'lucide-vue-next'
import { shareContent } from '@/composables/useShare'

const props = defineProps<{
  open: boolean
  title: string
  text: string
  url: string
}>()

const emit = defineEmits<{
  close: []
  shared: [result: 'shared' | 'copied' | 'failed']
}>()

const qrDataUrl = ref('')
const statusMessage = ref('')

watch(
  () => [props.open, props.url] as const,
  async ([open, url]) => {
    if (!open || !url) {
      qrDataUrl.value = ''
      return
    }
    try {
      qrDataUrl.value = await QRCode.toDataURL(url, { margin: 1, width: 180 })
    } catch {
      qrDataUrl.value = ''
    }
  },
  { immediate: true },
)

async function handleShare() {
  const result = await shareContent({
    title: props.title,
    text: props.text,
    url: props.url,
  })
  statusMessage.value =
    result === 'shared'
      ? '已唤起系统分享'
      : result === 'copied'
        ? '链接已复制到剪贴板'
        : '分享失败，请手动复制链接'
  emit('shared', result)
}

async function copyLink() {
  try {
    await navigator.clipboard.writeText(props.url)
    statusMessage.value = '链接已复制'
  } catch {
    statusMessage.value = '复制失败'
  }
}
</script>

<template>
  <div v-if="open" class="share-sheet">
    <div class="sheet-backdrop" @click="emit('close')" />
    <div class="sheet-panel">
      <div class="sheet-header">
        <h2>分享</h2>
        <button type="button" class="icon-btn" aria-label="关闭" @click="emit('close')">
          <X :size="20" />
        </button>
      </div>

      <p class="share-title">{{ title }}</p>
      <p class="share-text">{{ text }}</p>

      <img v-if="qrDataUrl" :src="qrDataUrl" alt="分享二维码" class="qr-image" />

      <div class="actions">
        <button type="button" class="btn btn-primary" @click="handleShare">
          <Share2 :size="18" />
          分享链接
        </button>
        <button type="button" class="btn btn-secondary" @click="copyLink">
          <Copy :size="18" />
          复制链接
        </button>
      </div>

      <p v-if="statusMessage" class="status">{{ statusMessage }}</p>
    </div>
  </div>
</template>

<style scoped>
.sheet-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}

.sheet-header h2 {
  margin: 0;
  font-size: 1.125rem;
}

.icon-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border: none;
  border-radius: 50%;
  background: var(--surface-muted);
}

.share-title {
  margin: 0 0 4px;
  font-weight: 700;
}

.share-text {
  margin: 0 0 16px;
  color: var(--muted);
  font-size: 0.9rem;
}

.qr-image {
  display: block;
  width: 180px;
  height: 180px;
  margin: 0 auto 16px;
}

.actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.status {
  margin: 12px 0 0;
  text-align: center;
  color: var(--coral);
  font-size: 0.875rem;
}
</style>
