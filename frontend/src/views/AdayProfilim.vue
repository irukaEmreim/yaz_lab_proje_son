<template>
    <div class="profil">
      <h2 class="text-2xl font-bold mb-4">👤 Profilim</h2>
  
      <label>Ad:</label>
      <input v-model="first_name" type="text" />
  
      <label>Soyad:</label>
      <input v-model="last_name" type="text" />
  
      <label>E-posta:</label>
      <input v-model="email" type="email" />
  
      <button @click="guncelle">💾 Bilgileri Güncelle</button>
  
      <hr class="my-6" />
  
      <h3 class="text-xl font-semibold mb-2">🔐 Şifre Güncelle</h3>
      <label>Mevcut Şifre:</label>
      <input v-model="old_password" type="password" />
      <label>Yeni Şifre:</label>
      <input v-model="new_password" type="password" />
  
      <button @click="sifreyiGuncelle">🔁 Şifreyi Güncelle</button>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  
  export default {
    data() {
      return {
        first_name: "",
        last_name: "",
        email: "",
        old_password: "",
        new_password: ""
      }
    },
    async created() {
      const token = localStorage.getItem("token");
      const res = await axios.get("http://localhost:8000/api/profilim/", {
        headers: { Authorization: `Bearer ${token}` }
      });
      this.first_name = res.data.first_name;
      this.last_name = res.data.last_name;
      this.email = res.data.email;
    },
    methods: {
      async guncelle() {
        const token = localStorage.getItem("token");
        await axios.put("http://localhost:8000/api/profilim/guncelle/", {
          first_name: this.first_name,
          last_name: this.last_name,
          email: this.email
        }, {
          headers: { Authorization: `Bearer ${token}` }
        });
        alert("✅ Profil güncellendi!");
      },
      async sifreyiGuncelle() {
        const token = localStorage.getItem("token");
        try {
          await axios.put("http://localhost:8000/api/profilim/sifre/", {
            old_password: this.old_password,
            new_password: this.new_password
          }, {
            headers: { Authorization: `Bearer ${token}` }
          });
          alert("✅ Şifre güncellendi!");
        } catch (err) {
          alert("❌ Şifre güncellenemedi: " + err.response.data.error);
        }
      }
    }
  }
  </script>
  
  <style scoped>
  .profil {
    background: #121212;
    color: white;
    padding: 40px;
  }
  input {
    display: block;
    margin-bottom: 12px;
    padding: 8px;
    width: 100%;
    background: #1f1f1f;
    color: white;
    border: 1px solid #444;
    border-radius: 6px;
  }
  button {
    padding: 10px 16px;
    background: #00bcd4;
    color: white;
    border: none;
    border-radius: 6px;
    font-weight: bold;
    margin-bottom: 20px;
  }
  button:hover {
    opacity: 0.9;
  }
  </style>
  