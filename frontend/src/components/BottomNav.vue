<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Home, MessageCircle, List, User } from 'lucide-vue-next'

const route = useRoute()
const router = useRouter()

const items = [
  { label: '首页', path: '/', icon: Home },
  { label: '咨询', path: '/advisor', icon: MessageCircle },
  { label: '清单', path: '/catalog', icon: List },
  { label: '我的', path: '/saved', icon: User },
] as const

const activePath = computed(() => route.path)

function navigate(path: string) {
  if (route.path !== path) {
    router.push(path)
  }
}
</script>

<template>
  <nav class="bottom-nav" aria-label="主导航">
    <button
      v-for="item in items"
      :key="item.path"
      type="button"
      class="nav-item"
      :class="{ active: activePath === item.path || (item.path !== '/' && activePath.startsWith(item.path)) }"
      @click="navigate(item.path)"
    >
      <component :is="item.icon" :size="22" />
      <span>{{ item.label }}</span>
    </button>
  </nav>

  <nav class="sidebar-nav" aria-label="侧边导航">
    <button
      v-for="item in items"
      :key="item.path"
      type="button"
      class="sidebar-item"
      :class="{ active: activePath === item.path || (item.path !== '/' && activePath.startsWith(item.path)) }"
      @click="navigate(item.path)"
    >
      <component :is="item.icon" :size="20" />
      <span>{{ item.label }}</span>
    </button>
  </nav>
</template>

<style scoped>
.bottom-nav {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 20;
  display: flex;
  align-items: stretch;
  min-height: var(--nav-height);
  padding: 8px 8px calc(8px + env(safe-area-inset-bottom, 0px));
  background: rgba(255, 255, 255, 0.96);
  border-top: 1px solid var(--border);
  backdrop-filter: blur(12px);
}

.nav-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  border: none;
  background: transparent;
  color: var(--muted);
  font-size: 0.75rem;
}

.nav-item.active {
  color: var(--coral);
}

.sidebar-nav {
  display: none;
  flex-direction: column;
  gap: 8px;
  padding: 24px 16px;
  background: var(--surface);
  border-right: 1px solid var(--border);
}

.sidebar-item {
  display: flex;
  align-items: center;
  gap: 12px;
  border: none;
  border-radius: var(--radius-sm);
  padding: 12px 16px;
  background: transparent;
  color: var(--muted);
  text-align: left;
}

.sidebar-item.active {
  background: rgba(255, 98, 95, 0.1);
  color: var(--coral);
  font-weight: 600;
}
</style>
