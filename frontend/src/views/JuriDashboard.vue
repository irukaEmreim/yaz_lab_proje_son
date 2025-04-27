<template>
  <div class="juri-dashboard">
    <h2 class="text-3xl font-bold mb-8 text-center text-cyan-400">🧑‍⚖️ Jüri Dashboard</h2>

    <div v-if="basvurular.length === 0" class="text-center text-gray-400">
      Size atanmış başvuru bulunmamaktadır.
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div v-for="basvuru in basvurular" :key="basvuru.id" class="basvuru-kart">
  <h3 class="text-lg font-bold mb-2 text-cyan-300">Başvuru Numarası: {{ basvuru.id }}</h3>
  <p><strong>İlan Başlığı:</strong> {{ basvuru.announcement_title }}</p>
  <p><strong>Bölüm:</strong> {{ basvuru.department_name }}</p>
  <p><strong>Başvuru Durumu:</strong> {{ basvuru.status }}</p>
  <p><strong>Başvuru Tarihi:</strong> {{ formatDate(basvuru.submitted_at) }}</p>
  <p><strong>Son Başvuru Tarihi:</strong> {{ formatDate(basvuru.end_date) }}</p>

  <router-link :to="`/juri/basvuru/${basvuru.id}`">
    <button class="degerlendir-buton">📝 Değerlendir</button>
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
      const res = await axios.get("http://localhost:8000/api/juri/basvurularim/", {
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
      if (!dateString) return '-';
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(dateString).toLocaleDateString('tr-TR', options);
    }
  }
}
</script>

<style scoped>
.juri-dashboard {
  background: #121212;
  color: white;
  padding: 40px;
  min-height: 100vh;
}

.basvuru-kart {
  background: #1f1f1f;
  padding: 20px;
  border-radius: 12px;
  border: 1px solid #00bcd4;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.basvuru-kart:hover {
  transform: translateY(-5px);
  box-shadow: 0 0 10px #00bcd4;
}

.degerlendir-buton {
  margin-top: 15px;
  padding: 10px 18px;
  background: #00bcd4;
  color: #121212;
  font-weight: bold;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.degerlendir-buton:hover {
  background: #00acc1;
}
</style>
