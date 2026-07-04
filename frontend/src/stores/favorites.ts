import { ref, computed, watch } from 'vue'
import type { Gift } from '@/types/catalog'

const STORAGE_KEY = 'gift-ai:favorites:v1'

function readIds(): number[] {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return []
    const parsed = JSON.parse(raw)
    return Array.isArray(parsed) ? parsed.filter((id) => typeof id === 'number') : []
  } catch {
    return []
  }
}

function writeIds(ids: number[]) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(ids))
}

const favoriteIds = ref<number[]>(readIds())

watch(
  favoriteIds,
  (ids) => {
    writeIds(ids)
  },
  { deep: true },
)

export function useFavorites() {
  const ids = computed(() => favoriteIds.value)

  function isFavorite(id: number) {
    return favoriteIds.value.includes(id)
  }

  function toggle(id: number) {
    if (isFavorite(id)) {
      favoriteIds.value = favoriteIds.value.filter((item) => item !== id)
    } else {
      favoriteIds.value = [...favoriteIds.value, id]
    }
  }

  function remove(id: number) {
    favoriteIds.value = favoriteIds.value.filter((item) => item !== id)
  }

  function filterGifts(gifts: Gift[]) {
    const idSet = new Set(favoriteIds.value)
    return gifts.filter((gift) => idSet.has(gift.id))
  }

  return {
    ids,
    isFavorite,
    toggle,
    remove,
    filterGifts,
  }
}

export { STORAGE_KEY }
