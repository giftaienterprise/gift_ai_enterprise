<script setup lang="ts">
defineProps<{
  show: boolean
}>()
</script>

<template>
  <div class="loading-overlay" :class="{ show }">
    <div class="spinner" />
    <div class="loading-steps">
      <div class="loading-step active">正在分析偏好...</div>
      <div class="loading-step">匹配礼物库...</div>
      <div class="loading-step">生成心意语...</div>
    </div>
  </div>
</template>

<style scoped>
.loading-overlay {
  position: fixed;
  inset: 0;
  background: rgba(255, 255, 255, 0.95);
  display: none;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.loading-overlay.show {
  display: flex;
}

.spinner {
  width: 60px;
  height: 60px;
  border: 4px solid #f0f0f0;
  border-top-color: #ff6b6b;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 20px;
}

.loading-steps {
  text-align: center;
}

.loading-step {
  padding: 8px 0;
  color: #999;
  font-size: 14px;
}

.loading-step.active {
  color: #ff6b6b;
  font-weight: 600;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
