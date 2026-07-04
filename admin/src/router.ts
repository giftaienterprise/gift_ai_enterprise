import { createRouter, createWebHistory } from 'vue-router'

import { auth } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory('/admin/'),
  routes: [
    {
      path: '/login',
      component: () => import('./views/LoginView.vue'),
      meta: { guest: true },
    },
    {
      path: '/403',
      component: () => import('./views/ForbiddenView.vue'),
      meta: { guest: true },
    },
    {
      path: '/',
      component: () => import('./layouts/AdminLayout.vue'),
      meta: { admin: true },
      children: [
        { path: '', component: () => import('./views/DashboardView.vue') },
        { path: 'products', component: () => import('./views/ProductsView.vue') },
        { path: 'products/new', component: () => import('./views/ProductEditorView.vue') },
        { path: 'products/:id', component: () => import('./views/ProductEditorView.vue') },
        { path: 'categories', component: () => import('./views/CategoriesView.vue') },
        { path: 'brands', component: () => import('./views/BrandsView.vue') },
        { path: 'settings', component: () => import('./views/SettingsView.vue') },
      ],
    },
  ],
})

router.beforeEach(async (to) => {
  if (!auth.ready.value) {
    try {
      await auth.restore()
    } catch {
      // State cleared in restore; guard below handles redirects.
    }
  }

  if (to.meta.admin) {
    if (!auth.isAdmin.value) {
      if (auth.token.value) {
        return '/403'
      }
      return { path: '/login', query: { redirect: to.fullPath } }
    }
    return true
  }

  if (to.path === '/login' && auth.isAdmin.value) {
    return '/'
  }

  return true
})

export default router
