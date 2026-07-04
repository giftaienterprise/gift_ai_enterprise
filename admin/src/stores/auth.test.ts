import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

import { createAuthStore } from './auth'

describe('admin auth store', () => {
  beforeEach(() => {
    sessionStorage.clear()
  })

  afterEach(() => {
    vi.unstubAllGlobals()
    sessionStorage.clear()
  })

  it('login stores token and verifies administrator identity', async () => {
    const fetch = vi
      .fn()
      .mockResolvedValueOnce(
        new Response(
          JSON.stringify({
            access_token: 'token',
            token_type: 'bearer',
            user: { id: 1, username: 'admin', is_active: true, is_admin: true },
          }),
          { status: 200, headers: { 'Content-Type': 'application/json' } },
        ),
      )
      .mockResolvedValueOnce(
        new Response(
          JSON.stringify({
            id: 1,
            username: 'admin',
            is_active: true,
            is_admin: true,
          }),
          { status: 200, headers: { 'Content-Type': 'application/json' } },
        ),
      )

    vi.stubGlobal('fetch', fetch)
    const store = createAuthStore()

    await store.login('admin', 'secret')

    expect(store.token.value).toBe('token')
    expect(sessionStorage.getItem('gift-ai:admin-token')).toBe('token')
    expect(store.user.value?.is_admin).toBe(true)
  })

  it('rejects an authenticated non-administrator', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue(
        new Response(
          JSON.stringify({
            access_token: 'token',
            token_type: 'bearer',
            user: { id: 2, username: 'member', is_active: true, is_admin: false },
          }),
          { status: 200, headers: { 'Content-Type': 'application/json' } },
        ),
      ),
    )

    const store = createAuthStore()

    await expect(store.login('member', 'secret')).rejects.toThrow('ADMIN_REQUIRED')
    expect(store.token.value).toBe('')
    expect(sessionStorage.getItem('gift-ai:admin-token')).toBeNull()
  })

  it('clears session on 401 from /auth/me', async () => {
    sessionStorage.setItem('gift-ai:admin-token', 'stale-token')

    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue(
        new Response(JSON.stringify({ detail: 'Unauthorized' }), {
          status: 401,
          headers: { 'Content-Type': 'application/json' },
        }),
      ),
    )

    const store = createAuthStore()
    store.token.value = 'stale-token'

    await expect(store.restore()).rejects.toThrow()
    expect(store.token.value).toBe('')
    expect(sessionStorage.getItem('gift-ai:admin-token')).toBeNull()
  })
})
