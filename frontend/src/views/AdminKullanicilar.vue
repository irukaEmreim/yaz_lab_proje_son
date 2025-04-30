<template>
    <div class="admin-users">
      <h2 class="text-3xl font-bold mb-8 text-center text-cyan-400">👥 Kullanıcı Listesi</h2>
  
      <div v-if="loading" class="text-center text-gray-400">Yükleniyor...</div>
  
      <div v-else>
        <!-- Adminler -->
        <div v-if="adminler.length">
          <h3 class="text-2xl font-bold mb-4 text-green-400">👑 Adminler</h3>
          <div v-for="user in adminler" :key="user.id" class="user-card">
            <p><strong>Ad Soyad:</strong> {{ user.first_name }} {{ user.last_name }}</p>
            <p><strong>E-posta:</strong> {{ user.email }}</p>
            <p><strong>Durum:</strong> {{ user.is_active ? 'Aktif' : 'Pasif' }}</p>
          </div>
        </div>
  
        <!-- Yöneticiler -->
        <div v-if="yoneticiler.length" class="mt-10">
          <h3 class="text-2xl font-bold mb-4 text-orange-400">🏢 Yöneticiler</h3>
          <div v-for="user in yoneticiler" :key="user.id" class="user-card">
            <p><strong>Ad Soyad:</strong> {{ user.first_name }} {{ user.last_name }}</p>
            <p><strong>E-posta:</strong> {{ user.email }}</p>
            <p><strong>Durum:</strong> {{ user.is_active ? 'Aktif' : 'Pasif' }}</p>
          </div>
        </div>
  
        <!-- Jüriler -->
        <div v-if="juriler.length" class="mt-10">
          <h3 class="text-2xl font-bold mb-4 text-purple-400">🎓 Jüriler</h3>
          <div v-for="user in juriler" :key="user.id" class="user-card">
            <p><strong>Ad Soyad:</strong> {{ user.first_name }} {{ user.last_name }}</p>
            <p><strong>E-posta:</strong> {{ user.email }}</p>
            <p><strong>Durum:</strong> {{ user.is_active ? 'Aktif' : 'Pasif' }}</p>
          </div>
        </div>
  
        <!-- Adaylar -->
        <div v-if="adaylar.length" class="mt-10">
          <h3 class="text-2xl font-bold mb-4 text-cyan-400">🧑‍🎓 Adaylar</h3>
          <div v-for="user in adaylar" :key="user.id" class="user-card">
            <p><strong>Ad Soyad:</strong> {{ user.first_name }} {{ user.last_name }}</p>
            <p><strong>E-posta:</strong> {{ user.email }}</p>
            <p><strong>Durum:</strong> {{ user.is_active ? 'Aktif' : 'Pasif' }}</p>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  
  export default {
    data() {
      return {
        users: [],
        adminler: [],
        yoneticiler: [],
        juriler: [],
        adaylar: [],
        loading: true
      }
    },
    async created() {
      const token = localStorage.getItem('token')
  
      try {
        const res = await axios.get('http://localhost:8000/api/kullanicilar/', {
          headers: { Authorization: `Bearer ${token}` }
        })
  
        this.users = res.data
  
        this.adminler = this.users.filter(user => user.role === 'admin')
        this.yoneticiler = this.users.filter(user => user.role === 'yonetici')
        this.juriler = this.users.filter(user => user.role === 'juri')
        this.adaylar = this.users.filter(user => user.role === 'aday')
  
      } catch (err) {
        console.error("Kullanıcılar yüklenemedi:", err)
        alert("Kullanıcılar yüklenirken bir hata oluştu.")
      } finally {
        this.loading = false
      }
    }
  }
  </script>
  
  <style scoped>
  .admin-users {
    background: #121212;
    color: white;
    padding: 40px;
    min-height: 100vh;
  }
  
  .user-card {
    background: #1f1f1f;
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 20px;
    border: 1px solid #00bcd4;
  }
  
  .user-card p {
    margin-bottom: 6px;
  }
  </style>
  