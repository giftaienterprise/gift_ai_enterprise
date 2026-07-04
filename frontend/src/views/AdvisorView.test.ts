import { describe, expect, it, vi } from 'vitest'
import { fireEvent, render, screen } from '@testing-library/vue'
import { createRouter, createWebHistory } from 'vue-router'
import AdvisorView from './AdvisorView.vue'
import { buildAdvisorGoal } from '@/api/advisor'

vi.mock('@/api/catalog', () => ({
  listGifts: vi.fn().mockResolvedValue({ items: [] }),
}))

vi.mock('@/api/advisor', async () => {
  const actual = await vi.importActual<typeof import('@/api/advisor')>('@/api/advisor')
  return {
    ...actual,
    runAdvisor: vi.fn(),
  }
})

const router = createRouter({
  history: createWebHistory(),
  routes: [{ path: '/advisor', component: { template: '<div />' } }],
})

describe('AdvisorView', () => {
  it('builds goal from relationship, occasion, and budget selections', async () => {
    await router.push('/advisor')
    render(AdvisorView, {
      global: {
        plugins: [router],
        stubs: {
          ProductCard: true,
          ShareSheet: true,
        },
      },
    })

    await fireEvent.click(screen.getByRole('button', { name: '父母' }))
    await fireEvent.click(screen.getByRole('button', { name: '生日' }))
    await fireEvent.click(screen.getByRole('button', { name: '300-800元' }))

    const expected = buildAdvisorGoal('父母', '生日', '300-800元')
    expect(screen.getByTestId('goal-preview').textContent).toBe(expected)
    expect(expected).toContain('父母')
    expect(expected).toContain('生日')
    expect(expected).toContain('300-800元')
  })
})
