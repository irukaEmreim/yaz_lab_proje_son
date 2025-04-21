<template>
  <div class="yonetici-panel">
    <h2>👨‍💼 Yönetici Paneli</h2>
    <div class="menu-buttons">
      <button @click="$router.push('/yonetici/juri-ekle')">👤 Yeni Jüri Oluştur</button>
      <button @click="$router.push('/yonetici/ilanlar')">📄 İlanları Görüntüle</button>
    </div>
    <div class="p-6">
    <h1 class="text-2xl font-bold mb-6">Yönetici Paneli</h1>
    
    <div class="flex flex-col gap-4">
      <router-link to="/yonetici/kadro-kriterleri">
        <button class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded w-full text-left">
          Kadro Kriterlerini Düzenle
        </button>
      </router-link>

      <router-link to="/yonetici/puan-kriterleri">
        <button class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded w-full text-left">
          Puan Kriterlerini Düzenle
        </button>
      </router-link>
    </div>
  </div>
    <router-view />
  </div>
</template>

<style scoped>
.yonetici-panel {
  padding: 40px;
  color: white;
  background-color: #121212;
}
.menu-buttons {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}
.menu-buttons button {
  background-color: #00bcd4;
  border: none;
  padding: 12px 16px;
  font-weight: bold;
  border-radius: 8px;
  cursor: pointer;
  color: #121212;
}
</style>

<script>
export default {
  name: "YoneticiDashboard"
}
</script>