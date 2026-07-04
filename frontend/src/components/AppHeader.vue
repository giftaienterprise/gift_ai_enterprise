<script setup lang="ts">
import { Gift } from 'lucide-vue-next'
</script>

<template>
  <header class="app-header">
    <div class="brand">
      <span class="brand-icon">
        <Gift :size="20" />
      </span>
      <div>
        <p class="brand-title">AI送礼参谋</p>
        <p class="brand-tagline">发现更贴心的礼物</p>
      </div>
    </div>
  </header>
</template>

<style scoped>
.app-header {
  position: sticky;
  top: 0;
  z-index: 10;
  display: flex;
  align-items: center;
  min-height: var(--header-height);
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border);
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
}

.brand-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 14px;
  background: var(--gradient-brand);
  color: #fff;
}

.brand-title {
  margin: 0;
  font-size: 1rem;
  font-weight: 700;
}

.brand-tagline {
  margin: 2px 0 0;
  font-size: 0.75rem;
  color: var(--muted);
}
</style>
