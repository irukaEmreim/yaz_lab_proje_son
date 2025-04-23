<template>
  <div class="yonetici-panel">
    <h2>👨‍💼 Yönetici Paneli</h2>

    <!-- Tüm yönlendirme butonları aynı satırda -->
    <div class="menu-buttons">
      <button @click="$router.push('/yonetici/juri-ekle')">👤 Yeni Jüri Oluştur</button>
      <button @click="$router.push('/yonetici/ilanlar')">📄 İlanları Görüntüle</button>
      <button @click="$router.push('/yonetici/kadro-kriterleri')">📋 Kadro Kriterlerini Düzenle</button>
      <button @click="$router.push('/yonetici/puan-kriterleri')">📊 Puan Kriterlerini Düzenle</button>
    </div>

    <router-view />
  </div>
</template>

<script>
export default {
  name: "YoneticiDashboard"
}
</script>

<style scoped>
.yonetici-panel {
  padding: 40px;
  color: white;
  background-color: #121212;
}

.menu-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 30px;
}

.menu-buttons button {
  background-color: #00bcd4;
  border: none;
  padding: 12px 18px;
  font-weight: bold;
  border-radius: 8px;
  cursor: pointer;
  color: #121212;
  transition: background-color 0.2s ease-in-out;
}

.menu-buttons button:hover {
  background-color: #00acc1;
}
</style>
