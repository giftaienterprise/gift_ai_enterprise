import { afterEach, describe, expect, it, vi } from 'vitest'
import { apiRequest, ApiError } from './http'

afterEach(() => {
  vi.unstubAllGlobals()
})

describe('apiRequest', () => {
  it('unwraps the backend success envelope', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue(
        new Response(
          JSON.stringify({ code: 200, message: 'success', data: { id: 1 } }),
          { status: 200, headers: { 'Content-Type': 'application/json' } },
        ),
      ),
    )

    await expect(apiRequest<{ id: number }>('/gifts/1')).resolves.toEqual({ id: 1 })
    expect(fetch).toHaveBeenCalledWith('/api/gifts/1', expect.any(Object))
  })

  it('throws ApiError for non-2xx responses', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue(
        new Response(JSON.stringify({ message: 'not found' }), {
          status: 404,
          headers: { 'Content-Type': 'application/json' },
        }),
      ),
    )

    await expect(apiRequest('/missing')).rejects.toBeInstanceOf(ApiError)
  })

  it('adds bearer token when provided', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue(
        new Response(
          JSON.stringify({ code: 200, message: 'success', data: {} }),
          { status: 200, headers: { 'Content-Type': 'application/json' } },
        ),
      ),
    )

    await apiRequest('/auth/me', { token: 'secret-token' })

    const [, options] = vi.mocked(fetch).mock.calls[0]
    expect(new Headers(options?.headers).get('Authorization')).toBe(
      'Bearer secret-token',
    )
  })
})
