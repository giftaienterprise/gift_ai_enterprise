export type Category = {
  id: number
  name: string
  icon: string | null
  sort: number
  is_active: boolean
}

export type Brand = {
  id: number
  name: string
  logo: string | null
  website: string | null
  description: string | null
  sort: number
  is_active: boolean
}

export type GiftImage = {
  id: number
  gift_id: number
  image_url: string
  sort: number
}

export type Gift = {
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
  category?: Category | null
  brand?: Brand | null
  images?: GiftImage[]
  purchase_url?: string
  platform?: string
  platform_links?: Record<string, string>
}

export type PaginatedResult<T> = {
  items: T[]
  total: number
  page: number
  size: number
  pages: number
}

export type PublicSettings = {
  wechat_id: string
  wechat_qr_url: string
  phone: string
  share_title: string
  share_description: string
  share_image_url: string
}
