<template>
    <div class="basvurularim">
      <h2 class="text-2xl font-bold mb-6">📄 Başvurularım</h2>
  
      <div v-if="basvurular.length === 0">
        Henüz hiç başvuru yapmadınız.
      </div>
  
      <div v-else>
        <div v-for="basvuru in basvurular" :key="basvuru.id" class="basvuru-kart">
            <p><strong>İlan Başlığı:</strong> {{ basvuru.announcement_title }}</p>
            <p><strong>Durum:</strong> {{ basvuru.status }}</p>
          <p><strong>Başvuru Tarihi:</strong> {{ formatDate(basvuru.submitted_at) }}</p>
            <router-link :to="`/aday/basvuru/${basvuru.id}`">
            <button class="detay-buton">🔍 Detaya Git</button>
            </router-link>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  
  export default {
    data() {
      return {
        basvurular: []
      }
    },
    async created() {
      const token = localStorage.getItem("token");
      try {
        const res = await axios.get("http://localhost:8000/api/basvurularim/", {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.basvurular = res.data;
      } catch (err) {
        console.error("Başvurular alınamadı:", err);
        alert("Başvurular yüklenirken bir hata oluştu.");
      }
    },
    methods: {
      formatDate(dateString) {
        const options = { year: 'numeric', month: 'long', day: 'numeric' };
        return new Date(dateString).toLocaleDateString('tr-TR', options);
      }
    }
  }
  </script>
  
  <style scoped>
  .basvurularim {
    background: #121212;
    color: white;
    padding: 40px;
  }
  .basvuru-kart {
    background: #1f1f1f;
    padding: 20px;
    margin-bottom: 20px;
    border-radius: 8px;
  }
  .detay-buton {
  margin-top: 10px;
  padding: 8px 16px;
  background: #00bcd4;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

  </style>
  