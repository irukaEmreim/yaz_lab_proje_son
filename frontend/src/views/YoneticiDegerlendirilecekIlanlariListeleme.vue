<template>
    <div class="degerlendirme-sayfasi">
      <h2 class="text-3xl font-bold mb-8 text-center text-cyan-400">📋 Sonuçlandırılacak Başvurular</h2>
  
      <div v-if="loading" class="text-center text-gray-400">Yükleniyor...</div>
  
      <div v-else>
        <div v-if="basvurular.length === 0" class="text-center text-gray-400">
          Sonuçlandırılacak başvuru bulunamadı.
        </div>
  
        <div v-else class="basvuru-listesi grid grid-cols-1 md:grid-cols-2 gap-6">
          <div v-for="basvuru in basvurular" :key="basvuru.application_id" class="basvuru-kart p-6 border border-cyan-400 rounded-lg bg-[#1f1f1f]">
            <h3 class="text-lg font-semibold mb-2 text-cyan-300">Başvuru Numarası: {{ basvuru.application_id }}</h3>
            <p><strong>İlan Başlığı:</strong> {{ basvuru.announcement_title }}</p>
            <p><strong>Bölüm:</strong> {{ basvuru.department_name }}</p>
            <p><strong>Başvuru Tarihi:</strong> {{ formatDate(basvuru.submitted_at) }}</p>
  
            <button class="sonuclandir-buton" @click="sonuclandir(basvuru.application_id)">✅ Sonuçlandır</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  
  export default {
    data() {
      return {
        basvurular: [],
        loading: true
      }
    },
    async created() {
      const token = localStorage.getItem('token')
  
      try {
        const res = await axios.get('http://localhost:8000/api/sonuclanacak-basvurular/', {
          headers: { Authorization: `Bearer ${token}` }
        })
  
        this.basvurular = res.data
  
      } catch (err) {
        console.error("Başvurular alınamadı:", err)
        alert("Başvurular yüklenirken hata oluştu.")
      } finally {
        this.loading = false
      }
    },
    methods: {
      sonuclandir(applicationId) {
        this.$router.push(`/yonetici/basvuru/${applicationId}/sonuclandir`)
      },
      formatDate(dateString) {
        const options = { year: 'numeric', month: 'long', day: 'numeric' }
        return new Date(dateString).toLocaleDateString('tr-TR', options)
      }
    }
  }
  </script>
  
  <style scoped>
  .degerlendirme-sayfasi {
    background: #121212;
    color: white;
    padding: 40px;
    min-height: 100vh;
  }
  
  .basvuru-listesi {
    margin-top: 20px;
  }
  
  .basvuru-kart {
    background: #1f1f1f;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
  }
  
  .basvuru-kart:hover {
    transform: translateY(-5px);
    box-shadow: 0 0 10px #00bcd4;
  }
  
  .sonuclandir-buton {
    margin-top: 15px;
    padding: 10px 18px;
    background: #00bcd4;
    color: #121212;
    font-weight: bold;
    border: none;
    border-radius: 8px;
    cursor: pointer;
  }
  
  .sonuclandir-buton:hover {
    background: #00acc1;
  }
  </style>
  