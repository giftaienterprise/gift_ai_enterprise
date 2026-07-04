export interface ProductForm {
  name: string
  subtitle: string
  category_id: number
  brand_id: number
  priceYuan: string
  cover: string
  description: string
  is_active: boolean
  sort: number
}

export interface GiftPayload {
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

export function toGiftPayload(form: ProductForm): GiftPayload {
  if (!form.name.trim()) {
    throw new Error('PRODUCT_NAME_REQUIRED')
  }
  if (!form.category_id) {
    throw new Error('CATEGORY_REQUIRED')
  }
  if (!form.brand_id) {
    throw new Error('BRAND_REQUIRED')
  }

  const price = Math.round(Number(form.priceYuan || 0) * 100)
  if (!Number.isFinite(price) || price < 0) {
    throw new Error('INVALID_PRICE')
  }

  return {
    name: form.name.trim(),
    subtitle: form.subtitle,
    category_id: form.category_id,
    brand_id: form.brand_id,
    price,
    cover: form.cover,
    description: form.description,
    is_active: form.is_active,
    sort: form.sort,
  }
}

export function centsToYuan(cents: number): string {
  return (cents / 100).toFixed(2)
}
