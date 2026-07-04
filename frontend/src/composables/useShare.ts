export type SharePayload = {
  title: string
  text: string
  url: string
}

export type ShareResult = 'shared' | 'copied' | 'failed'

export async function shareContent(payload: SharePayload): Promise<ShareResult> {
  const shareData = {
    title: payload.title,
    text: payload.text,
    url: payload.url,
  }

  if (typeof navigator !== 'undefined' && typeof navigator.share === 'function') {
    try {
      await navigator.share(shareData)
      return 'shared'
    } catch (error) {
      if (error instanceof DOMException && error.name === 'AbortError') {
        return 'failed'
      }
    }
  }

  if (typeof navigator !== 'undefined' && navigator.clipboard?.writeText) {
    try {
      await navigator.clipboard.writeText(payload.url)
      return 'copied'
    } catch {
      return 'failed'
    }
  }

  return 'failed'
}

export function useShare() {
  return { shareContent }
}
