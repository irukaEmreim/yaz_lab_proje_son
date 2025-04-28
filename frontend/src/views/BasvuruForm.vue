<template>
  <div class="basvuru-form">
    <h2 class="text-2xl font-bold mb-6">📝 Başvuru Formu</h2>

    <div v-for="(grup, kategori) in gruplar" :key="kategori" class="kategori-blok">
      <h3 class="kategori-baslik">{{ kategoriBasliklari[kategori] }}</h3>

      <div v-for="(entry, index) in secimler[kategori]" :key="index" class="secim-alani">
        <label>Faaliyet Türü:</label>
        <select v-model="entry.kod">
          <option disabled value="">Faaliyet Seç</option>
          <option v-for="f in grup" :key="f.faaliyet_kodu" :value="f.faaliyet_kodu">
            {{ f.faaliyet_kodu }} - {{ f.faaliyet_adi }}
          </option>
        </select>

        <label>Adet:</label>
        <input type="number" v-model.number="entry.adet" min="0" />

        <label>Belgeler:</label>
        <input type="file" :multiple="entry.adet > 1" @change="e => handleUpload(kategori, index, e)" />
      </div>

      <button class="alt-ekle" @click="faaliyetEkle(kategori)">➕ Faaliyet Ekle</button>
    </div>

    <button @click="submitForm">📤 Başvur</button>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      faaliyetler: [],
      gruplar: {},
      secimler: {},

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
  async created() {
    const token = localStorage.getItem("token")
    const res = await axios.get("http://localhost:8000/api/faaliyet-puanlari/", {
      headers: { Authorization: `Bearer ${token}` }
    })

    this.faaliyetler = res.data

    const gruplar = {}
    const secimler = {}

    res.data.forEach(faaliyet => {
      const kategori = faaliyet.faaliyet_kodu.charAt(0)
      if (!gruplar[kategori]) {
        gruplar[kategori] = []
        secimler[kategori] = []
      }
      gruplar[kategori].push(faaliyet)
    })

    this.gruplar = gruplar
    this.secimler = secimler
  },
  methods: {
    faaliyetEkle(kategori) {
      this.secimler[kategori].push({
        kod: "",
        adet: 0,
        belgeler: []
      })
    },
    handleUpload(kategori, index, event) {
      const files = Array.from(event.target.files)
      if (!this.secimler[kategori][index]) return
      this.secimler[kategori][index].belgeler = files
    },
    async submitForm() {
      
      const token = localStorage.getItem('token');
  const ilanId = this.$route.params.id;

  // 1️⃣ Gönderilecek form objesini düz formatta hazırlıyoruz
  const form = {};
  for (const kategori in this.secimler) {
    for (const entry of this.secimler[kategori]) {
      if (entry.kod) {
        form[entry.kod] = {
          adet: entry.adet,
          belgeler: entry.belgeler
        };
      }
    }
  }

  try {
    // 2️⃣ Başvuru verisini gönder
    const payload = {
      announcement_id: ilanId,
      form: form
    };

    const appRes = await axios.post("http://localhost:8000/api/basvuru-yap/", payload, {
      headers: { Authorization: `Bearer ${token}` }
    });

    const applicationId = appRes.data.application_id;

    // 3️⃣ Belgeleri yükle
    for (const kod in form) {
      const belgeler = form[kod].belgeler || [];
      for (const belge of belgeler) {
        const formData = new FormData();
        formData.append("application_id", applicationId);
        formData.append("file", belge);
        formData.append("faaliyet_kodu", kod);  // Başvurduğu faaliyet kodunu da gönderiyoruz

        await axios.post("http://localhost:8000/api/belge-yukle/", formData, {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'multipart/form-data'
          }
        });
      }
    }

    alert("✅ Başvuru ve belgeler başarıyla gönderildi!");
    this.$router.push(`/aday/tablo5-olustur/${applicationId}`);

  } catch (err) {
    console.error("❌ Başvuru gönderilirken hata:", err);
    alert("Başvuru sırasında bir hata oluştu.");
  }
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
.kategori-blok {
  margin-bottom: 30px;
}
.kategori-baslik {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 10px;
  color: #00bcd4;
}
.secim-alani {
  background: #1f1f1f;
  padding: 14px;
  margin-bottom: 12px;
  border-radius: 8px;
}
input,
select {
  display: block;
  width: 100%;
  margin-top: 6px;
  margin-bottom: 12px;
  padding: 8px;
  background: #2a2a2a;
  color: white;
  border: 1px solid #444;
  border-radius: 6px;
}
button {
  padding: 10px 18px;
  border: none;
  border-radius: 6px;
  font-weight: bold;
  cursor: pointer;
}
.alt-ekle {
  margin-top: 10px;
  background: #666;
  color: white;
}
button:hover {
  opacity: 0.9;
}
</style>
