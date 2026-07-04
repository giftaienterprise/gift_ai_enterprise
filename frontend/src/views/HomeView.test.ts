import { describe, expect, it, vi } from 'vitest'
import { render, screen } from '@testing-library/vue'
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from './HomeView.vue'

vi.mock('@/api/catalog', () => ({
  listGifts: vi.fn().mockResolvedValue({ items: [] }),
  formatPriceYuan: (cents: number) => `¥${cents / 100}`,
}))

const router = createRouter({
  history: createWebHistory(),
  routes: [{ path: '/', component: { template: '<div />' } }],
})

describe('HomeView', () => {
  it('renders the home heading', () => {
    render(HomeView, {
      global: {
        plugins: [router],
        stubs: {
          ProductCard: true,
        },
      },
    })

    expect(screen.getByRole('heading', { level: 1 }).textContent).toBe(
      '今天想为谁准备心意？',
    )
  })
})
