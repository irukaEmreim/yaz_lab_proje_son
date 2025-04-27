<template>
    <div class="finalize-page">
      <h2 class="text-3xl font-bold mb-8 text-center text-cyan-400">📝 Başvuruyu Sonuçlandır</h2>
  
      <div v-if="loading" class="text-center text-gray-400">Yükleniyor...</div>
  
      <div v-else>
        <!-- Jüri Raporları -->
        <div v-for="rapor in raporlar" :key="rapor.jury_member_name" class="rapor-kart mb-6 p-4 border border-cyan-400 rounded-lg bg-[#1f1f1f]">
          <h3 class="text-xl font-semibold text-cyan-300 mb-2">{{ rapor.jury_member_name }}</h3>
          <p><strong>Sonuç:</strong> {{ rapor.evaluation_result === 'olumlu' ? '✅ Olumlu' : '❌ Olumsuz' }}</p>
          <p><strong>Açıklama:</strong> {{ rapor.description }}</p>
          <a :href="getFileUrl(rapor.report_file_path)" target="_blank" class="file-link">📎 Raporu Görüntüle</a>
          <p class="text-sm text-gray-400 mt-2">Yükleme Tarihi: {{ formatDate(rapor.submitted_at) }}</p>
        </div>
  
        <!-- Son Karar -->
        <div class="karar-bolumu mt-10">
          <h3 class="text-2xl font-bold mb-4 text-cyan-300">🎯 Son Kararınızı Seçin</h3>
  
          <select v-model="seciliDurum" class="select-input">
            <option disabled value="">Karar Seçiniz</option>
            <option value="Onaylandı">✅ Onaylandı</option>
            <option value="Reddedildi">❌ Reddedildi</option>
          </select>
  
          <button class="submit-buton" @click="sonuclandir">💾 Kararı Kaydet</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  
  export default {
    data() {
      return {
        raporlar: [],
        loading: true,
        seciliDurum: ""
      }
    },
    async created() {
      const token = localStorage.getItem('token')
      const appId = this.$route.params.id
  
      try {
        const res = await axios.get(`http://localhost:8000/api/basvuru/${appId}/jury-raporlari/`, {
          headers: { Authorization: `Bearer ${token}` }
        })
  
        this.raporlar = res.data
  
      } catch (err) {
        console.error("Raporlar alınamadı:", err)
        alert("Raporlar yüklenirken bir hata oluştu.")
      } finally {
        this.loading = false
      }
    },
    methods: {
      getFileUrl(fileName) {
        return `http://localhost:8000/uploads/${fileName}`
      },
      formatDate(dateString) {
        const options = { year: 'numeric', month: 'long', day: 'numeric' }
        return new Date(dateString).toLocaleDateString('tr-TR', options)
      },
      async sonuclandir() {
        if (!this.seciliDurum) {
          alert("Lütfen bir karar seçiniz.")
          return
        }
  
        const token = localStorage.getItem('token')
        const appId = this.$route.params.id
  
        try {
          await axios.put(`http://localhost:8000/api/basvuru-sonuclandir/${appId}/`, {
            status: this.seciliDurum
          }, {
            headers: { Authorization: `Bearer ${token}` }
          })
  
          alert("Başvuru durumu başarıyla güncellendi!")
          this.$router.push('/yonetici')  // Yönetici anasayfasına dön
        } catch (err) {
          console.error("Durum güncellenemedi:", err)
          alert("Başvuru durumunu kaydederken bir hata oluştu.")
        }
      }
    }
  }
  </script>
  
  <style scoped>
  .finalize-page {
    background: #121212;
    color: white;
    padding: 40px;
    min-height: 100vh;
  }
  
  .rapor-kart {
    background: #1f1f1f;
  }
  
  .file-link {
    color: #00bcd4;
    text-decoration: underline;
  }
  
  .file-link:hover {
    color: #00acc1;
  }
  
  .karar-bolumu {
    margin-top: 30px;
  }
  
  .select-input {
    width: 100%;
    padding: 10px;
    background: #1f1f1f;
    color: white;
    border: 1px solid #00bcd4;
    border-radius: 6px;
    margin-bottom: 20px;
  }
  
  .submit-buton {
    background: #00bcd4;
    color: #121212;
    font-weight: bold;
    padding: 12px 20px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
  }
  
  .submit-buton:hover {
    background: #00acc1;
  }
  </style>
  