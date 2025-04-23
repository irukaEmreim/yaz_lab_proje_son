<template>
    <div class="ilan-detay">
      <h2>📄 İlan Detayları</h2>
  
      <div v-if="ilan">
        <h3>{{ ilan.title }}</h3>
        <p><strong>Pozisyon:</strong> {{ ilan.position_type }}</p>
        <p><strong>Tarih:</strong> {{ ilan.start_date }} - {{ ilan.end_date }}</p>
        <p><strong>Açıklama:</strong> {{ ilan.description }}</p>
        <p><strong>Bölüm:</strong> {{ ilan.bolum_adi || 'Bilinmiyor' }}</p>
  
        <div class="kriterler">
          <h4>🧾 Kadro Kriterleri</h4>
          <ul>
            <li v-for="k in kadroKriterleri" :key="k.id">
              {{ k.faaliyet_kodu }} - {{ k.faaliyet_adi }}: Minimum {{ k.asgari_adet }} adet
            </li>
          </ul>
  
          <h4>📊 Toplam Asgari Puan Gereksinimi</h4>
          <p v-if="toplamAsgariPuan !== null">Minimum toplam puan: <strong>{{ toplamAsgariPuan }}</strong></p>
          <p v-else>Veri bulunamadı.</p>
        </div>
      </div>
      <div v-else>
        <p>İlan yükleniyor...</p>
      </div>
    </div>
  </template>
  
  <script>
import axios from 'axios'

export default {
  data() {
    return {
      ilan: null,
      kadroKriterleri: [],
      toplamAsgariPuan: null
    }
  },
  async created() {
    const token = localStorage.getItem('token')
    const ilanId = this.$route.params.id

    // İlan bilgisi
    const ilanRes = await axios.get(`http://localhost:8000/api/announcements/${ilanId}/`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    this.ilan = ilanRes.data

    // Kadro kriterleri
    const kadroRes = await axios.get(`http://localhost:8000/api/kadro-kriterleri/`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    this.kadroKriterleri = kadroRes.data.filter(k => k.unvan === this.ilan.position_type)

    // Puan kriterleri
    const puanRes = await axios.get(`http://localhost:8000/api/puan-kriterleri/`, {
      headers: { Authorization: `Bearer ${token}` }
    })

    let eslesenUnvan = this.ilan.position_type.trim()
    if (eslesenUnvan === "Doçent" || eslesenUnvan === "Profesör") {
      eslesenUnvan = "Doçent/Profesör"
    }

    const toplamSatiri = puanRes.data.find(p =>
      p.unvan.toLowerCase().trim() === eslesenUnvan.toLowerCase().trim() &&
      p.faaliyet_kodu.toLowerCase().trim() === "toplam"
    )

    this.toplamAsgariPuan = toplamSatiri?.asgari_puan ?? 0

    // Kontrol için konsola basalım
    console.log("İlan tipi:", this.ilan.position_type)
    console.log("Eşleşen unvan:", eslesenUnvan)
    console.log("Toplam satırı:", toplamSatiri)
    console.log("Toplam asgari puan:", this.toplamAsgariPuan)
  }
}
</script>

  
  
  <style scoped>
  .ilan-detay {
    padding: 40px;
    background-color: #121212;
    color: white;
  }
  .kriterler {
    margin-top: 20px;
    background-color: #1e1e1e;
    padding: 20px;
    border-radius: 8px;
  }
  ul {
    margin-top: 10px;
    padding-left: 20px;
    list-style: square;
  }
  </style>