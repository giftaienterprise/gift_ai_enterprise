<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import {
  FolderOpen,
  Gift,
  LayoutDashboard,
  LogOut,
  Menu,
  Settings,
  Tag,
  X,
} from 'lucide-vue-next'

import { auth } from '@/stores/auth'

const router = useRouter()
const drawerOpen = ref(false)

const navItems = [
  { to: '/', label: '仪表盘', icon: LayoutDashboard },
  { to: '/products', label: '商品管理', icon: Gift },
  { to: '/categories', label: '分类管理', icon: FolderOpen },
  { to: '/brands', label: '品牌管理', icon: Tag },
  { to: '/settings', label: '联系与分享', icon: Settings },
]

const closeDrawer = () => {
  drawerOpen.value = false
}

const logout = async () => {
  auth.logout()
  await router.push('/login')
}
</script>

<template>
  <div class="admin-shell">
    <button
      type="button"
      class="mobile-menu-button"
      aria-label="打开导航"
      @click="drawerOpen = true"
    >
      <Menu :size="22" />
    </button>

    <div
      class="drawer-backdrop"
      :class="{ open: drawerOpen }"
      @click="closeDrawer"
    />

    <aside class="admin-sidebar" :class="{ open: drawerOpen }">
      <div class="sidebar-header">
        <div class="admin-brand">
          AI送礼参谋
          <small>管理后台</small>
        </div>
        <button
          type="button"
          class="drawer-close"
          aria-label="关闭导航"
          @click="closeDrawer"
        >
          <X :size="20" />
        </button>
      </div>

      <nav>
        <RouterLink
          v-for="item in navItems"
          :key="item.to"
          :to="item.to"
          @click="closeDrawer"
        >
          <component :is="item.icon" :size="18" />
          <span>{{ item.label }}</span>
        </RouterLink>
      </nav>

      <button type="button" class="logout-button" @click="logout">
        <LogOut :size="18" />
        <span>退出登录</span>
      </button>
    </aside>

    <section class="admin-content">
      <header>
        <div>
          <strong>你好，{{ auth.user.value?.nickname || auth.user.value?.username }}</strong>
          <span>今天也把礼物整理得更贴心一点。</span>
        </div>
      </header>
      <RouterView />
    </section>
  </div>
</template>
