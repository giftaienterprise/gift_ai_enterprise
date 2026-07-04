import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/HomeView.vue'),
    },
    {
      path: '/demand',
      name: 'demand',
      component: () => import('@/views/DemandView.vue'),
    },
    {
      path: '/result',
      name: 'result',
      component: () => import('@/views/ResultView.vue'),
    },
    {
      path: '/recommend/:id',
      name: 'recommend-detail',
      component: () => import('@/views/RecommendDetailView.vue'),
    },
    {
      path: '/advisor',
      redirect: '/demand',
    },
    {
      path: '/catalog',
      name: 'catalog',
      component: () => import('@/views/CatalogView.vue'),
    },
    {
      path: '/saved',
      name: 'saved',
      component: () => import('@/views/SavedView.vue'),
    },
    {
      path: '/products/:id',
      name: 'product',
      component: () => import('@/views/ProductView.vue'),
    },
  ],
  scrollBehavior() {
    return { top: 0 }
  },
})

export default router
