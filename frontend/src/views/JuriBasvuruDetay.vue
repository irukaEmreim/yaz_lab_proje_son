<template>
    <div class="basvuru-detay">
      <h2 class="text-3xl font-bold mb-8 text-center text-cyan-400">📄 Başvuru Detayı</h2>
  
      <div v-if="loading" class="text-center text-gray-400">Yükleniyor...</div>
  
      <div v-else>
        <!-- Aday Bilgileri -->
        <div class="aday-bilgileri mb-8 p-6 rounded-lg border border-cyan-400 bg-[#1f1f1f]">
          <h3 class="text-2xl font-bold text-cyan-300 mb-4">👤 Aday Bilgileri</h3>
          <p><strong>Adı Soyadı:</strong> {{ aday.first_name }} {{ aday.last_name }}</p>
          <p><strong>E-posta:</strong> {{ aday.email }}</p>
        </div>
  
        <!-- Faaliyetler ve Belgeler -->
        <div v-for="(belgeler, kategori) in kategorilereGoreGruplanmisBelgeler" :key="kategori" class="kategori-blok mb-10">
          <h3 class="text-xl font-semibold mb-4 text-cyan-300">{{ kategoriBasliklari[kategori] || kategori }}</h3>
  
          <ul v-if="belgeler.length > 0">
            <li v-for="belge in belgeler" :key="belge.id" class="mb-2">
              <a :href="belge.file_path" target="_blank" class="belge-link">
                📎 {{ belge.file_path }}
              </a>
              <span class="faaliyet-adi">({{ getFaaliyetAdi(belge.faaliyet_kodu) }})</span>
            </li>
          </ul>
          <p v-else class="text-gray-400">Belge eklenmemiş.</p>
        </div>
  
        <div v-if="aday.tablo5_pdf_path" class="mt-6">
          <a :href="aday.tablo5_pdf_path" target="_blank" download class="bg-cyan-500 hover:bg-cyan-400 text-white font-bold py-2 px-4 rounded mt-4 inline-block">
  📄 Tablo 5 PDF'ini İndir
</a>
        </div>
        <div v-else class="mt-6 text-gray-400">
            Tablo 5 henüz oluşturulmamış.
        </div>

        


        <!-- Jüri Değerlendirme Formu -->
        <div class="degerlendirme-form mt-16 p-6 rounded-lg border border-green-400 bg-[#1a1a1a]">
          <h3 class="text-2xl font-bold text-green-300 mb-6">🖋️ Jüri Değerlendirmesi</h3>
  
          <label class="block text-gray-300 mb-2">Değerlendirme Notu (Olumlu/Olumsuz):</label>
          <textarea v-model="degerlendirmeNotu" rows="5" class="input-alani mb-6" placeholder="Aday hakkındaki görüşlerinizi yazınız..." required></textarea>
  
          <label class="block text-gray-300 mb-2">Değerlendirme Sonucu:</label>
          <div class="flex items-center space-x-6 mb-6">
            <label class="flex items-center">
              <input type="radio" value="olumlu" v-model="degerlendirmeSonucu" class="radio-input" required />
              <span class="ml-2">Olumlu</span>
            </label>
            <label class="flex items-center">
              <input type="radio" value="olumsuz" v-model="degerlendirmeSonucu" class="radio-input" required />
              <span class="ml-2">Olumsuz</span>
            </label>
          </div>
  
          <label class="block text-gray-300 mb-2">Değerlendirme Dosyası (PDF):</label>
          <input type="file" @change="handleFileUpload" class="input-dosya mb-6" accept="application/pdf" required />
  
          <button @click="submitDegerlendirme" class="degerlendir-buton">✅ Değerlendir ve Kaydet</button>
        </div>
  
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  
  export default {
    data() {
      return {
        aday: {},
        belgeler: [],
        faaliyetler: [],
        loading: true,
        degerlendirmeNotu: '',
        degerlendirmeSonucu: '',
        degerlendirmeDosya: null,
        kategoriBasliklari: {
          A: "📘 Makaleler",
          B: "📑 Bildiriler",
          C: "📚 Kitaplar",
          D: "🔗 Atıflar",
          E: "🏫 Eğitim",
          F: "🧑‍🏫 Danışmanlık",
          G: "🧪 Patent",
          H: "🔬 Araştırma Projeleri",
          I: "📰 Editörlük",
          J: "🏆 Ödüller",
          K: "🏛️ Yönetim Geçmişi"
        }
      }
    },
    computed: {
      kategorilereGoreGruplanmisBelgeler() {
        const gruplar = {}
  
        for (const belge of this.belgeler) {
          const kategori = belge.faaliyet_kodu ? belge.faaliyet_kodu.charAt(0) : "Diğer"
          if (!gruplar[kategori]) {
            gruplar[kategori] = []
          }
          gruplar[kategori].push(belge)
        }
        return gruplar
      }
    },
    async created() {
      const token = localStorage.getItem("token");
      const appId = this.$route.params.id
  
      try {
        const [adayRes, belgeRes, faaliyetTurleriRes] = await Promise.all([
          axios.get(`http://localhost:8000/api/aday-bilgileri/${appId}/`, {
            headers: { Authorization: `Bearer ${token}` }
          }),
          axios.get(`http://localhost:8000/api/belgeler/${appId}/`, {
            headers: { Authorization: `Bearer ${token}` }
          }),
          axios.get(`http://localhost:8000/api/faaliyet-turleri/${appId}/`, {
            headers: { Authorization: `Bearer ${token}` }
          })
        ])
  
        this.aday = adayRes.data
        this.belgeler = belgeRes.data
        this.faaliyetler = faaliyetTurleriRes.data
  
      } catch (err) {
        console.error("Detaylar yüklenemedi:", err)
        alert("Detaylar yüklenirken bir hata oluştu.")
      } finally {
        this.loading = false
      }
    },
    methods: {
      getFileUrl(fileName) {
        return `http://localhost:8000/uploads/${fileName}`
      },
      getFaaliyetAdi(faaliyetKodu) {
        const faaliyet = this.faaliyetler.find(f => f.faaliyet_kodu === faaliyetKodu)
        return faaliyet ? faaliyet.faaliyet_adi : "Bilinmeyen Faaliyet"
      },
      handleFileUpload(event) {
        this.degerlendirmeDosya = event.target.files[0];
      },
      async submitDegerlendirme() {
        if (!this.degerlendirmeNotu || !this.degerlendirmeSonucu || !this.degerlendirmeDosya) {
          alert("Lütfen değerlendirme notu yazın, sonucu seçin ve dosya yükleyin.");
          return;
        }
  
        const token = localStorage.getItem("token");
        const appId = this.$route.params.id;
        const formData = new FormData();
  
        formData.append("application_id", appId);
        formData.append("degerlendirme_notu", this.degerlendirmeNotu);
        formData.append("sonuc", this.degerlendirmeSonucu);
        formData.append("dosya", this.degerlendirmeDosya);
  
        try {
          await axios.post(`http://localhost:8000/api/juri/degerlendir/`, formData, {
            headers: {
              Authorization: `Bearer ${token}`,
              'Content-Type': 'multipart/form-data'
            }
          });
  
          alert("✅ Değerlendirme başarıyla kaydedildi!");
          this.$router.push('/juri');
  
        } catch (err) {
          console.error("Değerlendirme kaydedilirken hata:", err);
          alert("❌ Değerlendirme kaydedilirken bir hata oluştu.");
        }
      }
    }
  }
  </script>
  
  <style scoped>
  .basvuru-detay {
    background: #121212;
    color: white;
    padding: 40px;
    min-height: 100vh;
  }
  
  .kategori-blok {
    background: #1f1f1f;
    padding: 20px;
    border-radius: 10px;
    border: 1px solid #00bcd4;
  }
  
  .belge-link {
    color: #00bcd4;
    text-decoration: underline;
  }
  
  .belge-link:hover {
    color: #00acc1;
  }
  
  .faaliyet-adi {
    color: #80deea;
    font-size: 0.9rem;
    margin-left: 8px;
  }
  
  .degerlendirme-form {
    background: #1a1a1a;
    padding: 30px;
    border-radius: 12px;
    border: 1px solid #00e676;
    margin-top: 40px;
  }
  
  .input-alani, .input-dosya {
    width: 100%;
    padding: 10px;
    background: #2a2a2a;
    border: 1px solid #555;
    border-radius: 8px;
    color: white;
  }
  
  .radio-input {
    width: 18px;
    height: 18px;
    accent-color: #00e676;
  }
  
  .degerlendir-buton {
    padding: 12px 24px;
    background: #00e676;
    color: #121212;
    font-weight: bold;
    border: none;
    border-radius: 8px;
    cursor: pointer;
  }
  
  .degerlendir-buton:hover {
    background: #00c853;
  }
  </style>
  