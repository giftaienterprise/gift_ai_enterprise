import { apiRequest } from './http'
import type { RecommendRequest, RecommendResult } from '@/types/advisor'

export function recommendGifts(payload: RecommendRequest) {
  return apiRequest<RecommendResult>('/advisor/recommend', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}
