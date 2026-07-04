<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useRecommendHistory } from '@/stores/recommendations'

const router = useRouter()
const history = useRecommendHistory()

function quickStart(relation: string) {
  router.push({ path: '/demand', query: { relation } })
}

function startRecommend() {
  router.push('/demand')
}
</script>

<template>
  <section class="page home-page">
    <div class="hero-copy">
      <h1>不知道该送什么？</h1>
      <p>问问你的 AI 参谋</p>
    </div>

    <button type="button" class="card card-gradient" @click="quickStart('恋人')">
      <div class="card-icon">💝</div>
      <div class="card-title">为恋人挑选</div>
      <div class="card-desc">纪念日、生日的浪漫惊喜</div>
    </button>

    <button type="button" class="card card-outline" @click="quickStart('父母')">
      <div class="card-icon">🧧</div>
      <div class="card-title">给长辈送心意</div>
      <div class="card-desc">逢年过节表达孝心</div>
    </button>

    <button type="button" class="card card-outline blue" @click="quickStart('朋友')">
      <div class="card-icon">🎁</div>
      <div class="card-title">朋友间的惊喜</div>
      <div class="card-desc">乔迁、生日聚会心意</div>
    </button>

    <button type="button" class="btn btn-primary" @click="startRecommend">
      开始智能推荐
    </button>

    <div v-if="history.length" class="history">
      <h3>历史推荐</h3>
      <div v-for="(item, index) in history.slice(0, 3)" :key="index" class="history-item card">
        为 {{ item.relation }} 的 {{ item.scene }} 方案
      </div>
    </div>
  </section>
</template>

<style scoped>
.home-page {
  padding-bottom: 24px;
}

.hero-copy {
  text-align: center;
  padding: 20px 0;
}

.hero-copy h1 {
  margin: 0 0 4px;
  font-size: 26px;
}

.hero-copy p {
  margin: 0;
  color: #999;
  font-size: 15px;
}

.card {
  width: 100%;
  text-align: left;
  border: none;
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 10px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  cursor: pointer;
  background: #fff;
}

.card-gradient {
  background: linear-gradient(135deg, #ff6b6b, #ff8e53);
  color: #fff;
}

.card-outline {
  border: 2px solid #ffe0e0;
}

.card-outline.blue {
  border-color: #e0f0ff;
}

.card-icon {
  font-size: 32px;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  margin-top: 4px;
}

.card-desc {
  font-size: 13px;
  opacity: 0.85;
  color: inherit;
}

.card-outline .card-desc {
  color: #999;
}

.btn-primary {
  width: 100%;
  margin-top: 10px;
  padding: 16px;
  border: none;
  border-radius: 50px;
  font-size: 18px;
  font-weight: 600;
  color: #fff;
  background: linear-gradient(135deg, #ff6b6b, #ff8e53);
  box-shadow: 0 8px 25px rgba(255, 107, 107, 0.4);
  cursor: pointer;
}

.history {
  margin-top: 24px;
}

.history h3 {
  font-size: 15px;
  color: #666;
  margin-bottom: 12px;
}

.history-item {
  padding: 14px;
  font-size: 14px;
}
</style>
