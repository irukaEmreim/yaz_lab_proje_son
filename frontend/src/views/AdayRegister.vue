<template>
  <div class="register">
    <h2 class="text-2xl font-bold mb-4">➕ Üye Ol</h2>

    <label>TC Kimlik No:</label>
    <input v-model="tc_kimlik_no" type="text" maxlength="11" />

    <label>Ad:</label>
    <input v-model="first_name" type="text" />

    <label>Soyad:</label>
    <input v-model="last_name" type="text" />

    <label>E-posta:</label>
    <input v-model="email" type="email" />

    <label>Şifre:</label>
    <input v-model="password" type="password" />

    <button @click="register">Kaydol</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      tc_kimlik_no: '',
      first_name: '',
      last_name: '',
      email: '',
      password: ''
    }
  },
  methods: {
    async register() {
      try {
        await axios.post('http://localhost:8000/api/auth/register/', {
          tc_kimlik_no: this.tc_kimlik_no,
          first_name: this.first_name,
          last_name: this.last_name,
          email: this.email,
          password: this.password
        });
        alert('✅ Kayıt başarılı! Şimdi giriş yapabilirsiniz.');
        this.$router.push('/login');
      } catch (err) {
        console.error('Kayıt hatası:', err);
        alert('❌ Kayıt başarısız: ' + err.response.data.error);
      }
    }
  }
}
</script>

<style scoped>
.register {
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
}
button:hover {
  opacity: 0.9;
}
</style>
