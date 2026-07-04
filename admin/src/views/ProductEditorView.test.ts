import { flushPromises, mount } from '@vue/test-utils'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { defineComponent } from 'vue'

import ProductEditorView from './ProductEditorView.vue'

const push = vi.fn()

vi.mock('vue-router', () => ({
  useRoute: () => ({ params: {} }),
  useRouter: () => ({ push }),
}))

vi.mock('@/api/admin', () => ({
  adminApi: {
    categories: vi.fn().mockResolvedValue({
      items: [{ id: 1, name: '香氛', sort: 0, is_active: true }],
    }),
    brands: vi.fn().mockResolvedValue({
      items: [{ id: 2, name: '暖心', sort: 0, is_active: true }],
    }),
    createGift: vi.fn(),
    updateGift: vi.fn(),
    gift: vi.fn(),
  },
}))

vi.mock('@/components/ImageUploader.vue', () => ({
  default: defineComponent({
    props: ['modelValue'],
    emits: ['update:modelValue'],
    template: '<div />',
  }),
}))

describe('ProductEditorView', () => {
  afterEach(() => {
    vi.clearAllMocks()
  })

  it('shows required field error when name is empty', async () => {
    const wrapper = mount(ProductEditorView)
    await flushPromises()

    await wrapper.find('form').trigger('submit.prevent')
    await flushPromises()

    expect(wrapper.text()).toContain('请输入商品名称')
    const { adminApi } = await import('@/api/admin')
    expect(adminApi.createGift).not.toHaveBeenCalled()
  })

  it('converts yuan display to integer cents for API writes', async () => {
    const { adminApi } = await import('@/api/admin')

    const wrapper = mount(ProductEditorView)
    await flushPromises()

    await wrapper.get('input[required]').setValue('暖心香氛')
    const selects = wrapper.findAll('select')
    await selects[0].setValue('1')
    await selects[1].setValue('2')
    await wrapper.get('input[step="0.01"]').setValue('199.50')
    await wrapper.find('form').trigger('submit.prevent')
    await flushPromises()

    expect(adminApi.createGift).toHaveBeenCalledWith(
      expect.objectContaining({
        name: '暖心香氛',
        category_id: 1,
        brand_id: 2,
        price: 19950,
      }),
    )
    expect(push).toHaveBeenCalledWith('/products')
  })
})
