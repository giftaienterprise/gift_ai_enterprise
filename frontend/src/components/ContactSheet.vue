<script setup lang="ts">
import { computed } from 'vue'
import { Copy, Phone, X } from 'lucide-vue-next'
import type { PublicSettings } from '@/types/catalog'

const props = defineProps<{
  open: boolean
  settings: PublicSettings | null
}>()

const emit = defineEmits<{
  close: []
}>()

const hasPhone = computed(() => Boolean(props.settings?.phone?.trim()))
const hasWechat = computed(
  () =>
    Boolean(props.settings?.wechat_id?.trim()) ||
    Boolean(props.settings?.wechat_qr_url?.trim()),
)

async function copyWechatId() {
  if (!props.settings?.wechat_id) return
  try {
    await navigator.clipboard.writeText(props.settings.wechat_id)
  } catch {
    /* ignore */
  }
}
</script>

<template>
  <div v-if="open" class="contact-sheet">
    <div class="sheet-backdrop" @click="emit('close')" />
    <div class="sheet-panel">
      <div class="sheet-header">
        <h2>联系购买</h2>
        <button type="button" class="icon-btn" aria-label="关闭" @click="emit('close')">
          <X :size="20" />
        </button>
      </div>

      <p class="hint">如需下单或咨询，可通过以下方式联系我们。</p>

      <a
        v-if="hasPhone"
        :href="`tel:${settings?.phone}`"
        class="contact-action"
      >
        <Phone :size="20" />
        <span>拨打电话 {{ settings?.phone }}</span>
      </a>

      <div v-if="hasWechat" class="wechat-block">
        <img
          v-if="settings?.wechat_qr_url"
          :src="settings.wechat_qr_url"
          alt="微信二维码"
          class="qr-image"
        />
        <button
          v-if="settings?.wechat_id"
          type="button"
          class="contact-action"
          @click="copyWechatId"
        >
          <Copy :size="20" />
          <span>复制微信号：{{ settings.wechat_id }}</span>
        </button>
      </div>

      <p v-if="!hasPhone && !hasWechat" class="empty-state">
        暂未配置联系方式
      </p>
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
  color: var(--ink);
}

.hint {
  margin: 0 0 16px;
  color: var(--muted);
  font-size: 0.9rem;
}

.contact-action {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
  margin-bottom: 12px;
  padding: 14px 16px;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  background: #fff;
  color: var(--ink);
  text-decoration: none;
}

.wechat-block {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.qr-image {
  width: 180px;
  height: 180px;
  margin: 0 auto;
  object-fit: contain;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border);
}
</style>
