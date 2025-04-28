<template>
  <div class="basvuru-detay">
    <h2 class="baslik">📄 Başvuru Detayı</h2>

    <div v-if="loading" class="yukleniyor">
      Yükleniyor...
    </div>

    <div v-else>
      <!-- Başvuru Durumu -->
      <div class="kart durum-karti">
        <h3 class="kart-baslik">🟢 Başvuru Durumu</h3>
        <p class="durum">{{ basvuru.status }}</p>
      </div>

      <!-- Faaliyetler -->
      <div class="kart">
        <h3 class="kart-baslik">🧾 Faaliyetler</h3>
        <ul class="liste">
          <li v-for="faaliyet in faaliyetler" :key="faaliyet.id" class="liste-oge">
            {{ faaliyet.faaliyet_kodu }} - {{ faaliyet.adet }} adet
          </li>
        </ul>
      </div>

      <!-- Belgeler -->
      <div class="kart">
        <h3 class="kart-baslik">📎 Belgeler</h3>
        <ul v-if="belgeler.length > 0" class="liste">
          <li v-for="belge in belgeler" :key="belge.id" class="liste-oge">
            <a :href="belge.file_path" target="_blank" class="belge-link">
              📄 {{ belge.file_path.split('/').pop() }}
            </a>
          </li>
        </ul>
        <p v-else class="no-data">Belge bulunamadı.</p>
      </div>

      <!-- Tablo 5 PDF -->
      <div class="kart">
        <h3 class="kart-baslik">📝 Tablo 5 PDF</h3>
        <div v-if="basvuru.tablo5_pdf_path" class="tablo5-link">
          <a :href="basvuru.tablo5_pdf_path" target="_blank" class="belge-link">
            📥 Tablo 5 PDF'ini Görüntüle
          </a>
        </div>
        <p v-else class="no-data">Tablo 5 henüz oluşturulmamış.</p>
      </div>
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
  padding: 40px;
  background-color: #121212;
  color: white;
  min-height: 100vh;
}

.baslik {
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 30px;
  text-align: center;
  color: #00bcd4;
}

.yukleniyor {
  text-align: center;
  font-size: 18px;
  color: #aaa;
}

.kart {
  background-color: #1e1e1e;
  padding: 20px;
  border-radius: 10px;
  margin-bottom: 24px;
  box-shadow: 0 0 5px rgba(255, 255, 255, 0.05);
}

.kart-baslik {
  font-size: 22px;
  color: #00e676;
  margin-bottom: 15px;
}

.liste {
  list-style: none;
  padding-left: 0;
}

.liste-oge {
  margin-bottom: 10px;
}

.belge-link {
  color: #00bcd4;
  text-decoration: none;
  font-weight: bold;
}

.belge-link:hover {
  color: #00acc1;
  text-decoration: underline;
}

.no-data {
  color: #888;
  font-style: italic;
}

.tablo5-link {
  margin-top: 10px;
}

.durum {
  font-size: 24px;
  font-weight: bold;
  color: #00e5ff;
  text-align: center;
}

</style>