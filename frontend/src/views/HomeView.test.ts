import { mount } from '@vue/test-utils'
import { createRouter, createWebHistory } from 'vue-router'
import { describe, expect, it } from 'vitest'
import HomeView from '@/views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [{ path: '/', component: HomeView }],
})

describe('HomeView', () => {
  it('shows the template hero heading', async () => {
    router.push('/')
    await router.isReady()
    const wrapper = mount(HomeView, {
      global: { plugins: [router] },
    })
    expect(wrapper.text()).toContain('不知道该送什么？')
  })
})
