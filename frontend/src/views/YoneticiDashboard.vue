<template>
  <div class="yonetici-panel">
    <h2>👨‍💼 Yönetici Paneli</h2>
    <div class="menu-buttons">
      <button @click="$router.push('/yonetici/juri-ekle')">👤 Yeni Jüri Oluştur</button>
      <button @click="$router.push('/yonetici/ilanlar')">📄 İlanları Görüntüle</button>
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
