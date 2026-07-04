import { computed, ref } from 'vue'
import type { RecommendResult, RecommendedGift } from '@/types/advisor'

const STORAGE_KEY = 'gift-ai:recommendations:v1'
const HISTORY_KEY = 'gift-ai:recommend-history:v1'

const current = ref<RecommendResult | null>(loadCurrent())

function loadCurrent(): RecommendResult | null {
  try {
    const raw = sessionStorage.getItem(STORAGE_KEY)
    return raw ? (JSON.parse(raw) as RecommendResult) : null
  } catch {
    return null
  }
}

export function useRecommendations() {
  const gifts = computed(() => current.value?.gifts ?? [])

  function saveResult(result: RecommendResult) {
    current.value = result
    sessionStorage.setItem(STORAGE_KEY, JSON.stringify(result))
    appendHistory(result)
  }

  function getGift(id: string): RecommendedGift | undefined {
    return gifts.value.find((gift) => gift.id === id)
  }

  function clearCurrent() {
    current.value = null
    sessionStorage.removeItem(STORAGE_KEY)
  }

  return {
    current,
    gifts,
    saveResult,
    getGift,
    clearCurrent,
  }
}

function appendHistory(result: RecommendResult) {
  try {
    const history = JSON.parse(localStorage.getItem(HISTORY_KEY) || '[]') as Array<{
      title: string
      relation: string
      scene: string
      created_at: string
    }>
    history.unshift({
      title: result.combo_title,
      relation: result.relation,
      scene: result.scene,
      created_at: new Date().toISOString(),
    })
    localStorage.setItem(HISTORY_KEY, JSON.stringify(history.slice(0, 10)))
  } catch {
    /* ignore */
  }
}

export function useRecommendHistory() {
  try {
    return JSON.parse(localStorage.getItem(HISTORY_KEY) || '[]') as Array<{
      title: string
      relation: string
      scene: string
      created_at: string
    }>
  } catch {
    return []
  }
}
