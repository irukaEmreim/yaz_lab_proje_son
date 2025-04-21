<template>
    <div class="form-container">
      <h2>👤 Yeni Jüri Oluştur</h2>
      <form @submit.prevent="createNewJury">
        <input v-model="newJury.tc_kimlik_no" placeholder="TC Kimlik No" required />
        <input v-model="newJury.first_name" placeholder="Ad" required />
        <input v-model="newJury.last_name" placeholder="Soyad" required />
        <input v-model="newJury.email" type="email" placeholder="Email" required />
        <input v-model="newJury.password" type="password" placeholder="Şifre" required />
        <button type="submit">✅ Oluştur</button>
      </form>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  
  export default {
    data() {
      return {
        newJury: {
          tc_kimlik_no: '',
          first_name: '',
          last_name: '',
          email: '',
          password: ''
        }
      }
    },
    methods: {
      async createNewJury() {
        const token = localStorage.getItem('token')
        try {
          await axios.post('http://127.0.0.1:8000/api/juri-olustur/', this.newJury, {
            headers: { Authorization: `Bearer ${token}` }
          })
          alert('Jüri başarıyla oluşturuldu!')
          this.newJury = { tc_kimlik_no: '', first_name: '', last_name: '', email: '', password: '' }
        } catch (err) {
          alert('Hata: Jüri oluşturulamadı!')
          console.error(err)
        }
      }
    }
  }
  </script>
  
  <style scoped>
  .form-container {
    background-color: #1e1e1e;
    padding: 20px;
    border-radius: 10px;
    max-width: 400px;
    margin: auto;
    color: white;
  }
  input {
    display: block;
    width: 100%;
    margin-bottom: 12px;
    padding: 10px;
    border: none;
    border-radius: 6px;
    background: #2a2a2a;
    color: white;
  }
  button {
    background: #00bcd4;
    color: #121212;
    padding: 10px 16px;
    border: none;
    border-radius: 6px;
    font-weight: bold;
    cursor: pointer;
  }
  </style>
  