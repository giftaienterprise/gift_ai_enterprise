import { flushPromises, mount } from '@vue/test-utils'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { defineComponent } from 'vue'

import SettingsView from './SettingsView.vue'

const settings = {
  id: 1,
  wechat_id: 'gift-ai',
  wechat_qr_url: '/uploads/qr.png',
  phone: '400-800-1234',
  share_title: 'AI送礼参谋',
  share_description: '发现更贴心的礼物',
  share_image_url: '/uploads/share.png',
}

vi.mock('@/api/admin', () => ({
  adminApi: {
    settings: vi.fn(),
    updateSettings: vi.fn(),
    upload: vi.fn(),
  },
}))

vi.mock('@/components/ImageUploader.vue', () => ({
  default: defineComponent({
    props: ['modelValue'],
    emits: ['update:modelValue'],
    template: '<div />',
  }),
}))

describe('SettingsView', () => {
  afterEach(() => {
    vi.clearAllMocks()
  })

  it('loads existing settings on mount', async () => {
    const { adminApi } = await import('@/api/admin')
    vi.mocked(adminApi.settings).mockResolvedValue(settings)

    const wrapper = mount(SettingsView)
    await flushPromises()

    expect(adminApi.settings).toHaveBeenCalled()
    expect((wrapper.get('input[placeholder="企业或客服微信号"]').element as HTMLInputElement).value).toBe(
      'gift-ai',
    )
    expect((wrapper.get('input[placeholder="例如 400-800-1234"]').element as HTMLInputElement).value).toBe(
      '400-800-1234',
    )
  })

  it('saves settings and shows success feedback', async () => {
    const { adminApi } = await import('@/api/admin')
    vi.mocked(adminApi.settings).mockResolvedValue(settings)
    vi.mocked(adminApi.updateSettings).mockResolvedValue({
      ...settings,
      phone: '400-800-5678',
    })

    const wrapper = mount(SettingsView)
    await flushPromises()

    await wrapper.get('input[placeholder="例如 400-800-1234"]').setValue('400-800-5678')
    await wrapper.find('form').trigger('submit.prevent')
    await flushPromises()

    expect(adminApi.updateSettings).toHaveBeenCalledWith(
      expect.objectContaining({
        wechat_id: 'gift-ai',
        phone: '400-800-5678',
        share_title: 'AI送礼参谋',
      }),
    )
    expect(wrapper.get('[role="status"]').text()).toContain('设置已保存')
  })

  it('retains values and shows error when save fails', async () => {
    const { adminApi } = await import('@/api/admin')
    vi.mocked(adminApi.settings).mockResolvedValue(settings)
    vi.mocked(adminApi.updateSettings).mockRejectedValue(new Error('SERVER_ERROR'))

    const wrapper = mount(SettingsView)
    await flushPromises()

    await wrapper.get('input[placeholder="例如 400-800-1234"]').setValue('400-800-5678')
    await wrapper.find('form').trigger('submit.prevent')
    await flushPromises()

    expect(wrapper.text()).toContain('保存失败，请稍后重试')
    expect((wrapper.get('input[placeholder="例如 400-800-1234"]').element as HTMLInputElement).value).toBe(
      '400-800-5678',
    )
  })
})
