import { computed, ref } from 'vue'

import { apiRequest } from '@/api/http'

export interface AdminUser {
  id: number
  username: string
  nickname?: string | null
  is_active: boolean
  is_admin: boolean
}

interface LoginResponse {
  access_token: string
  token_type: string
  user: AdminUser
}

const TOKEN_KEY = 'gift-ai:admin-token'

export function createAuthStore() {
  const token = ref(sessionStorage.getItem(TOKEN_KEY) ?? '')
  const user = ref<AdminUser | null>(null)
  const ready = ref(false)

  const clear = () => {
    token.value = ''
    user.value = null
    sessionStorage.removeItem(TOKEN_KEY)
  }

  const logout = () => {
    clear()
    ready.value = true
  }

  const restore = async () => {
    if (!token.value) {
      user.value = null
      ready.value = true
      return
    }

    try {
      const current = await apiRequest<AdminUser>('/auth/me', { token: token.value })
      if (!current.is_admin) {
        clear()
        throw new Error('ADMIN_REQUIRED')
      }
      user.value = current
    } catch (error) {
      clear()
      throw error
    } finally {
      ready.value = true
    }
  }

  const login = async (username: string, password: string) => {
    const result = await apiRequest<LoginResponse>('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    })

    if (!result.user.is_admin) {
      clear()
      throw new Error('ADMIN_REQUIRED')
    }

    token.value = result.access_token
    sessionStorage.setItem(TOKEN_KEY, token.value)
    ready.value = false
    await restore()
  }

  const isAdmin = computed(() => Boolean(user.value?.is_admin))

  return { token, user, ready, isAdmin, login, logout, restore, clear }
}

export const auth = createAuthStore()
