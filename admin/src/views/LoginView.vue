<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

import { auth } from '@/stores/auth'

const router = useRouter()
const username = ref('')
const password = ref('')
const error = ref('')
const busy = ref(false)

const submit = async () => {
  busy.value = true
  error.value = ''

  try {
    await auth.login(username.value, password.value)
    await router.push('/')
  } catch (reason) {
    error.value =
      reason instanceof Error && reason.message === 'ADMIN_REQUIRED'
        ? '该账号不是管理员'
        : '用户名或密码错误'
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <main class="login-page">
    <section class="login-panel">
      <p class="brand-mark">AI送礼参谋</p>
      <h1>管理后台</h1>
      <p>登录后维护商品、联系方式和分享内容。</p>
      <form @submit.prevent="submit">
        <label>
          用户名
          <input v-model="username" required autocomplete="username" />
        </label>
        <label>
          密码
          <input
            v-model="password"
            required
            type="password"
            autocomplete="current-password"
          />
        </label>
        <p v-if="error" class="form-error">{{ error }}</p>
        <button :disabled="busy" type="submit">
          {{ busy ? '正在登录…' : '登录' }}
        </button>
      </form>
    </section>
  </main>
</template>
