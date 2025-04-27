<template>
  <div class="login-form">
    <form @submit.prevent="login">
      <h2>Giriş Yap</h2>

      <label>TC Kimlik No</label>
      <input v-model="tc_kimlik_no" type="text" maxlength="11" required />

      <label>Şifre</label>
      <input v-model="password" type="password" required />

      <button type="submit">Giriş Yap</button>

      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>

      <router-link to="/uye-ol">
        <button type="button" class="uye-ol-buton">➕ Üye Ol</button>
      </router-link>
    </form>
  </div>
</template>

<script>
import axios from 'axios'
import { jwtDecode } from 'jwt-decode'

export default {
  data() {
    return {
      tc_kimlik_no: '',
      password: '',
      errorMessage: ''
    }
  },
  methods: {
    async login() {
      try {
        const response = await axios.post('http://127.0.0.1:8000/api/auth/login/', {
          tc_kimlik_no: this.tc_kimlik_no,
          password: this.password
        })

        const token = response.data.access
        localStorage.setItem('token', token)

        const decoded = jwtDecode(token)
        const role = decoded.role

        if (role === 'admin') {
          this.$router.push('/admin')
        } else if (role === 'yonetici') {
          this.$router.push('/yonetici')
        } else if (role === 'aday') {
          this.$router.push('/aday')
        } else if (role === 'juri') {
          this.$router.push('/juri/dashboard')
        } else {
          alert("Hmm... Bir sorun var gibi. (Bilinmeyen rol)")
        }

      } catch (error) {
        console.error("Giriş hatası:", error)
        this.errorMessage = "Giriş başarısız. TC veya şifre yanlış olabilir."
      }
    }
  }
}
</script>

<style scoped>
.login-form {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 70vh;
  background-color: #121212;
  padding: 40px;
  border-radius: 16px;
  box-shadow: 0 0 15px rgba(255, 255, 255, 0.1);
}

form {
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 350px;
  color: #ffffff;
}

h2 {
  text-align: center;
  margin-bottom: 24px;
  color: #00bcd4;
}

label {
  margin: 8px 0 4px;
  font-weight: 500;
}

input {
  padding: 10px;
  border: none;
  border-radius: 6px;
  margin-bottom: 12px;
  background-color: #1f1f1f;
  color: white;
  outline: none;
}

input:focus {
  border: 1px solid #00bcd4;
}

button {
  padding: 12px;
  background-color: #00bcd4;
  border: none;
  border-radius: 6px;
  color: #121212;
  font-weight: bold;
  cursor: pointer;
  margin-top: 10px;
  transition: background-color 0.2s ease-in-out;
}

button:hover {
  background-color: #00acc1;
}

.uye-ol-buton {
  margin-top: 10px;
  background: #1f1f1f;
  border: 1px solid #00bcd4;
  color: #00bcd4;
  transition: background-color 0.2s ease-in-out, color 0.2s ease-in-out;
}

.uye-ol-buton:hover {
  background-color: #00bcd4;
  color: white;
}

.error {
  margin-top: 12px;
  color: #ff6b6b;
  text-align: center;
}
</style>
