import { afterEach, describe, expect, it, vi } from 'vitest'
import { shareContent } from './useShare'

afterEach(() => {
  vi.unstubAllGlobals()
  vi.restoreAllMocks()
})

describe('useShare', () => {
  it('uses navigator.share when available', async () => {
    const share = vi.fn().mockResolvedValue(undefined)
    vi.stubGlobal('navigator', {
      share,
      clipboard: { writeText: vi.fn() },
    })

    const result = await shareContent({
      title: '礼物推荐',
      text: '看看这个',
      url: 'https://example.com/gift/1',
    })

    expect(result).toBe('shared')
    expect(share).toHaveBeenCalledWith({
      title: '礼物推荐',
      text: '看看这个',
      url: 'https://example.com/gift/1',
    })
  })

  it('falls back to clipboard when share is unavailable', async () => {
    const writeText = vi.fn().mockResolvedValue(undefined)
    vi.stubGlobal('navigator', {
      clipboard: { writeText },
    })

    const result = await shareContent({
      title: '礼物推荐',
      text: '看看这个',
      url: 'https://example.com/gift/1',
    })

    expect(result).toBe('copied')
    expect(writeText).toHaveBeenCalledWith('https://example.com/gift/1')
  })

  it('falls back to clipboard when share throws', async () => {
    const writeText = vi.fn().mockResolvedValue(undefined)
    vi.stubGlobal('navigator', {
      share: vi.fn().mockRejectedValue(new Error('share failed')),
      clipboard: { writeText },
    })

    const result = await shareContent({
      title: '礼物推荐',
      text: '看看这个',
      url: 'https://example.com/gift/1',
    })

    expect(result).toBe('copied')
    expect(writeText).toHaveBeenCalledWith('https://example.com/gift/1')
  })
})
