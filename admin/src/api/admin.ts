import { apiRequest } from './http'
import { auth } from '@/stores/auth'

export interface PageResult<T> {
  items: T[]
  total: number
  page: number
  size: number
}

export interface Gift {
  id: number
  name: string
  subtitle: string
  category_id: number
  brand_id: number
  price: number
  cover: string
  description: string
  is_active: boolean
  sort: number
}

export interface Category {
  id: number
  name: string
  icon?: string | null
  sort: number
  is_active: boolean
}

export interface Brand {
  id: number
  name: string
  logo?: string | null
  website?: string | null
  description?: string | null
  sort: number
  is_active: boolean
}

export interface AdminSummary {
  gift_count: number
  active_gift_count: number
  category_count: number
  brand_count: number
  recent_gifts: Gift[]
}

export interface SiteSettings {
  id?: number
  wechat_id: string
  wechat_qr_url: string
  phone: string
  share_title: string
  share_description: string
  share_image_url: string
}

function withToken() {
  return { token: auth.token.value }
}

export const adminApi = {
  summary: () => apiRequest<AdminSummary>('/admin/summary', withToken()),
  gifts: () => apiRequest<PageResult<Gift>>('/gifts/?page=1&size=100', withToken()),
  gift: (id: number) => apiRequest<Gift>(`/gifts/${id}`, withToken()),
  createGift: (data: unknown) =>
    apiRequest<Gift>('/gifts/', { method: 'POST', body: JSON.stringify(data), ...withToken() }),
  updateGift: (id: number, data: unknown) =>
    apiRequest<Gift>(`/gifts/${id}`, { method: 'PUT', body: JSON.stringify(data), ...withToken() }),
  deleteGift: (id: number) => apiRequest(`/gifts/${id}`, { method: 'DELETE', ...withToken() }),
  attachGiftImage: (id: number, imageUrl: string) =>
    apiRequest(`/gifts/${id}/images`, {
      method: 'POST',
      body: JSON.stringify({ image_url: imageUrl }),
      ...withToken(),
    }),
  categories: () => apiRequest<PageResult<Category>>('/categories/?page=1&size=100', withToken()),
  createCategory: (data: unknown) =>
    apiRequest<Category>('/categories/', { method: 'POST', body: JSON.stringify(data), ...withToken() }),
  updateCategory: (id: number, data: unknown) =>
    apiRequest<Category>(`/categories/${id}`, { method: 'PUT', body: JSON.stringify(data), ...withToken() }),
  deleteCategory: (id: number) => apiRequest(`/categories/${id}`, { method: 'DELETE', ...withToken() }),
  brands: () => apiRequest<PageResult<Brand>>('/brands/?page=1&size=100', withToken()),
  createBrand: (data: unknown) =>
    apiRequest<Brand>('/brands/', { method: 'POST', body: JSON.stringify(data), ...withToken() }),
  updateBrand: (id: number, data: unknown) =>
    apiRequest<Brand>(`/brands/${id}`, { method: 'PUT', body: JSON.stringify(data), ...withToken() }),
  deleteBrand: (id: number) => apiRequest(`/brands/${id}`, { method: 'DELETE', ...withToken() }),
  upload: async (file: File) => {
    const body = new FormData()
    body.append('file', file)
    return apiRequest<{ image_url: string }>('/upload/image', { method: 'POST', body, ...withToken() })
  },
  settings: () => apiRequest<SiteSettings>('/settings', withToken()),
  updateSettings: (data: unknown) =>
    apiRequest<SiteSettings>('/settings', { method: 'PUT', body: JSON.stringify(data), ...withToken() }),
}
