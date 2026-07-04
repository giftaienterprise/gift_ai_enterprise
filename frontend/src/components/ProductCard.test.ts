import { describe, expect, it } from 'vitest'
import { render, screen } from '@testing-library/vue'
import ProductCard from './ProductCard.vue'
import type { Gift } from '@/types/catalog'

const product: Gift = {
  id: 1,
  name: '手工香薰礼盒',
  subtitle: '放松身心',
  category_id: 1,
  brand_id: 1,
  price: 29900,
  cover: '',
  description: '',
  is_active: true,
  sort: 0,
}

describe('ProductCard', () => {
  it('shows name and price', () => {
    render(ProductCard, {
      props: { product },
    })

    expect(screen.getByText('手工香薰礼盒')).toBeTruthy()
    expect(screen.getByText('¥299')).toBeTruthy()
  })
})
