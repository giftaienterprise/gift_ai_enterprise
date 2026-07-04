export type RecommendedGift = {
  id: string
  name: string
  price: number
  emoji: string
  reason: string
  match: string
  meaning: string
  tip: string
  tags: string[]
  purchase_url: string
  platform: string
  platform_links: Record<string, string>
}

export type RecommendResult = {
  success: boolean
  combo_title: string
  relation: string
  scene: string
  budget: string
  gifts: RecommendedGift[]
  source: string
  error?: string | null
}

export type RecommendRequest = {
  relation: string
  scene: string
  budget: string
  note?: string
  platform?: 'taobao' | 'jd'
}

export type RecommendSession = RecommendResult & {
  created_at: string
}
