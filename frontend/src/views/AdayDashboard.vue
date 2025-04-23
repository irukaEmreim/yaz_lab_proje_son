<template>
  <div class="aday-dashboard">
    <!-- ÜST MENÜ -->
    <div class="ust-menu">
      <button @click="$router.push('/aday/basvurularim')">📄 Başvurularım</button>
      <button @click="$router.push('/aday/profilim')">👤 Profilim</button>
    </div>

    <h2 class="baslik">📢 Aktif Akademik İlanlar</h2>

    <div v-if="announcements.length === 0" class="bos">
      Şu anda aktif ilan bulunmamaktadır.
    </div>

    <!-- İLANLAR -->
    <div v-for="ilan in announcements" :key="ilan.id" class="ilan-karti">
      <h3>{{ ilan.title }}</h3>
      <p><strong>Pozisyon:</strong> {{ ilan.position_type }}</p>
      <p><strong>Tarih:</strong> {{ ilan.start_date }} - {{ ilan.end_date }}</p>
      <p class="aciklama">{{ ilan.description }}</p>

      <div class="butonlar">
        <button @click="goToDetay(ilan.id)">🔍 Detay</button>
        <button @click="goToBasvuru(ilan.id)">📝 Başvur</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      announcements: []
    }
  },
  mounted() {
    const token = localStorage.getItem('token')
    axios.get('http://localhost:8000/api/announcements/', {
      headers: { Authorization: `Bearer ${token}` }
    })
      .then(res => {
        const today = new Date().toISOString().split("T")[0]
        this.announcements = res.data.filter(a => a.end_date >= today)
      })
      .catch(err => {
        console.error("İlanlar yüklenemedi:", err)
      })
  },
  methods: {
    goToDetay(id) {
      this.$router.push(`/aday/ilan/${id}/detay`)
    },
    goToBasvuru(id) {
      this.$router.push(`/aday/ilan/${id}/basvur`)
    }
  }
}
</script>

<style scoped>
.aday-dashboard {
  padding: 40px;
  background-color: #121212;
  color: white;
}

.ust-menu {
  display: flex;
  gap: 16px;
  margin-bottom: 30px;
}

.ust-menu button {
  background-color: #00bcd4;
  color: #121212;
  font-weight: bold;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  cursor: pointer;
}

.baslik {
  font-size: 24px;
  margin-bottom: 20px;
}

.bos {
  padding: 20px;
  background-color: #1f1f1f;
  border-radius: 8px;
  text-align: center;
  font-style: italic;
}

.ilan-karti {
  background-color: #1e1e1e;
  padding: 20px;
  border-radius: 10px;
  margin-bottom: 20px;
  box-shadow: 0 0 5px rgba(255, 255, 255, 0.05);
}

.aciklama {
  margin-top: 8px;
  font-size: 14px;
  color: #ccc;
}

.butonlar {
  display: flex;
  gap: 10px;
  margin-top: 12px;
}

button {
  padding: 10px 16px;
  border: none;
  border-radius: 6px;
  font-weight: bold;
  cursor: pointer;
}

button:hover {
  opacity: 0.9;
}
</style>