import { apiRequest } from './http'
import type {
  Brand,
  Category,
  Gift,
  PaginatedResult,
  PublicSettings,
} from '@/types/catalog'

export function listGifts(page = 1, size = 50) {
  return apiRequest<PaginatedResult<Gift>>(`/gifts/?page=${page}&size=${size}`)
}

export function getGift(id: number) {
  return apiRequest<Gift>(`/gifts/${id}`)
}

export function listCategories(page = 1, size = 50) {
  return apiRequest<PaginatedResult<Category>>(
    `/categories/?page=${page}&size=${size}`,
  )
}

export function listBrands(page = 1, size = 50) {
  return apiRequest<PaginatedResult<Brand>>(`/brands/?page=${page}&size=${size}`)
}

export function getPublicSettings() {
  return apiRequest<PublicSettings>('/settings/public')
}

export function formatPriceYuan(cents: number): string {
  const yuan = cents / 100
  return yuan % 1 === 0 ? `¥${yuan.toFixed(0)}` : `¥${yuan.toFixed(2)}`
}
