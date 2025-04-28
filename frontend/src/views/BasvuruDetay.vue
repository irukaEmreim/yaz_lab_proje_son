<template>
    <div class="basvuru-detay">
      <h2 class="text-2xl font-bold mb-4">📄 Başvuru Detayı</h2>
  
      <div v-if="loading">Yükleniyor...</div>
      <div v-else>
        <!-- BURASI YENİ: Başvuru Durumu -->
        <div class="durum-blok">
          <h1>{{ basvuru.status }}</h1>
        </div>
  
        <h3 class="text-lg font-semibold mb-2">🧾 Faaliyetler</h3>
        <ul>
          <li v-for="faaliyet in faaliyetler" :key="faaliyet.id">
            {{ faaliyet.faaliyet_kodu }} - {{ faaliyet.adet }} adet
          </li>
        </ul>
  
        <h3 class="text-lg font-semibold mt-4 mb-2">📎 Belgeler</h3>
        <ul>
          <li v-for="belge in belgeler" :key="belge.id">
            {{ belge.file_path }} - {{ formatDate(belge.uploaded_at) }}
          </li>
        </ul>
      </div>
      <div v-if="basvuru.tablo5_pdf_path" class="mt-6">
  <a :href="getPdfUrl(basvuru.tablo5_pdf_path)" target="_blank" class="pdf-link">
    📄 Tablo 5 PDF'ini Görüntüle
  </a>
</div>
<div v-else class="mt-6 text-gray-400">
  Tablo 5 henüz oluşturulmamış.
</div>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  
  export default {
    data() {
      return {
        basvuru: {},
        belgeler: [],
        faaliyetler: [],
        loading: true
      }
    },
    async created() {
      const token = localStorage.getItem('token');
      const appId = this.$route.params.id;
  
      try {
        const [basvuruRes, belgelerRes, faaliyetlerRes] = await Promise.all([
          axios.get(`http://localhost:8000/api/basvuru-detay/${appId}/`, {
            headers: { Authorization: `Bearer ${token}` }
          }),
          axios.get(`http://localhost:8000/api/belgeler/${appId}/`, {
            headers: { Authorization: `Bearer ${token}` }
          }),
          axios.get(`http://localhost:8000/api/faaliyetler/${appId}/`, {
            headers: { Authorization: `Bearer ${token}` }
          }),
        ])
  
        this.basvuru = basvuruRes.data;
        this.belgeler = belgelerRes.data;
        this.faaliyetler = faaliyetlerRes.data;
  
      } catch (err) {
        console.error("Veriler alınamadı:", err);
        alert("Bir hata oluştu.");
      } finally {
        this.loading = false;
      }
    },
    methods: {
      getPdfUrl(filePath) {
        return `http://localhost:8000/media/${filePath}`
      },
      formatDate(dateString) {
      if (!dateString) return '-';
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(dateString).toLocaleDateString('tr-TR', options);
    }
    }
  }
  </script>
  
  
  <style scoped>
  .basvuru-detay {
    background: #121212;
    color: white;
    padding: 40px;
  }
  
  .durum-blok {
    background: #1f1f1f;
    padding: 20px;
    margin-bottom: 30px;
    border-radius: 12px;
    text-align: center;
  }
  
  .durum-blok h1 {
    font-size: 28px;
    font-weight: bold;
    color: #00bcd4;
  }
  </style>
  