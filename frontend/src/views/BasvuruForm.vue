<template>
    <div class="basvuru-form">
      <h2>📝 Başvuru Formu</h2>
  
      <div v-if="ilan">
        <h3>{{ ilan.title }}</h3>
        <p><strong>Pozisyon:</strong> {{ ilan.position_type }}</p>
        <p><strong>Açıklama:</strong> {{ ilan.description }}</p>
      </div>
  
      <form @submit.prevent="submitForm">
        <div class="form-group">
          <label>🔢 Atıf Sayısı</label>
          <input v-model.number="atifSayisi" type="number" min="0" required />
        </div>
  
        <div class="form-group">
          <label>📎 Her Atıf için Belge Yükleyin</label>
          <input type="file" multiple @change="handleFileUpload" />
        </div>
  
        <div class="form-group">
          <label>🎓 Konferans Yayınına Katıldınız mı?</label>
          <select v-model="konferansVar">
            <option :value="true">Evet</option>
            <option :value="false">Hayır</option>
          </select>
        </div>
  
        <div v-if="konferansVar" class="form-group">
          <label>📁 Katılım Belgesi Yükleyin</label>
          <input type="file" @change="handleConferenceUpload" />
        </div>
  
        <button type="submit">📤 Başvuruyu Gönder</button>
      </form>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  
  export default {
    data() {
      return {
        ilan: null,
        atifSayisi: 0,
        atifBelgeleri: [],
        konferansVar: false,
        konferansBelgesi: null
      }
    },
    async created() {
      const ilanId = this.$route.params.id
      const token = localStorage.getItem('token')
  
      const res = await axios.get(`http://localhost:8000/api/announcements/${ilanId}/`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      this.ilan = res.data
    },
    methods: {
      handleFileUpload(e) {
        this.atifBelgeleri = Array.from(e.target.files)
      },
      handleConferenceUpload(e) {
        this.konferansBelgesi = e.target.files[0]
      },
      async submitForm() {
        const token = localStorage.getItem('token')
  
        // 1. Başvuru kaydı oluştur
        const appRes = await axios.post('http://localhost:8000/api/applications/', {
          announcement_id: this.ilan.id
        }, {
          headers: { Authorization: `Bearer ${token}` }
        })
  
        const applicationId = appRes.data.id
  
        // 2. Atıf belgelerini yükle
        for (const file of this.atifBelgeleri) {
          const formData = new FormData()
          formData.append('application_id', applicationId)
          formData.append('document_type_id', 1)  // İndeksli Yayın
          formData.append('file', file)
          await axios.post('http://localhost:8000/api/documents/', formData, {
            headers: {
              Authorization: `Bearer ${token}`,
              'Content-Type': 'multipart/form-data'
            }
          })
        }
  
        // 3. Konferans belgesi yükle
        if (this.konferansVar && this.konferansBelgesi) {
          const formData = new FormData()
          formData.append('application_id', applicationId)
          formData.append('document_type_id', 4)  // Konferans Katılım
          formData.append('file', this.konferansBelgesi)
          await axios.post('http://localhost:8000/api/documents/', formData, {
            headers: {
              Authorization: `Bearer ${token}`,
              'Content-Type': 'multipart/form-data'
            }
          })
        }
  
        alert('Başvuru başarıyla gönderildi!')
        this.$router.push('/aday')
      }
    }
  }
  </script>
  
  <style scoped>
  .basvuru-form {
    background: #121212;
    color: white;
    padding: 40px;
  }
  form {
    display: flex;
    flex-direction: column;
    gap: 20px;
    margin-top: 20px;
  }
  input,
  select {
    padding: 10px;
    background: #1f1f1f;
    border: 1px solid #444;
    color: white;
    border-radius: 6px;
  }
  button {
    padding: 12px;
    background-color: #00bcd4;
    color: #121212;
    font-weight: bold;
    border: none;
    border-radius: 6px;
    cursor: pointer;
  }
  button:hover {
    background-color: #0097a7;
  }
  </style>
  