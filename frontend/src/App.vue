<script setup lang="ts">
import AppHeader from '@/components/AppHeader.vue'
import BottomNav from '@/components/BottomNav.vue'
</script>

<template>
  <div class="app-shell">
    <BottomNav />
    <div class="main-column">
      <AppHeader />
      <main>
        <RouterView />
      </main>
    </div>
  </div>
</template>

<style scoped>
.main-column {
  min-width: 0;
}
</style>
