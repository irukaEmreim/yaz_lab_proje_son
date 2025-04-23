<template>
  <div class="form-wrapper">
    <form @submit.prevent="submit" class="edit-form">
      <h3>➕ Yeni İlan Ekle</h3>

      <label>Başlık</label>
      <input v-model="form.title" placeholder="Başlık" required />

      <label>Pozisyon</label>
      <select v-model="form.position_type" required>
        <option disabled value="">Pozisyon Seç</option>
        <option>Dr. Öğr. Üyesi</option>
        <option>Doçent</option>
        <option>Profesör</option>
      </select>
      <label> Bölüm </label>
      <select v-model="form.bolum_id" required>
  <option disabled value="">Bölüm Seçiniz</option>
  <option v-for="b in bolumler" :key="b.id" :value="b.id">
    {{ b.ad }}
  </option>
</select>


      <label>Açıklama</label>
      <textarea v-model="form.description" placeholder="Açıklama" rows="3" />

      <label>Başlangıç Tarihi</label>
      <input type="date" v-model="form.start_date" required />

      <label>Bitiş Tarihi</label>
      <input type="date" v-model="form.end_date" required />

      <div class="form-buttons">
        <button type="submit">💾 Kaydet</button>
      </div>
    </form>
  </div>
</template>

<script>
import axios from "axios"
import { jwtDecode } from "jwt-decode"

export default {
  data() {
    return {
      form: {
        title: "",
        position_type: "",
        description: "",
        start_date: "",
        end_date: "",
        bolum_id: ""
      },
      bolumler: []  // 💥 Eksikti, eklendi
    }
  },
  mounted() {
    const token = localStorage.getItem("token")
    axios.get("http://localhost:8000/api/bolumler/", {
      headers: { Authorization: `Bearer ${token}` }
    })
    .then(res => {
      this.bolumler = res.data
    })
    .catch(e => {
      console.error("Bölümler alınamadı:", e)
    })
  },
  methods: {
    async submit() {
      const token = localStorage.getItem("token")
      const decoded = jwtDecode(token)

      const payload = {
        ...this.form,
        created_by: decoded.user_id,
        created_at: new Date().toISOString().split("T")[0]
      }

      try {
        await axios.post("http://127.0.0.1:8000/api/announcements/", payload, {
          headers: { Authorization: `Bearer ${token}` }
        })
        alert("Yeni ilan eklendi!")
        this.$router.push("/admin/announcements") 
      } catch (err) {
        console.error("İlan eklenemedi:", err)
        alert("İlan eklenirken bir hata oluştu.")
      }
    }
  }
}
</script>


<style scoped>

.form-wrapper {
  max-width: 500px;
  margin: 0 auto;
}

.edit-form {
  padding: 20px;
  background-color: #1e1e1e;
  border-radius: 12px;
  box-shadow: 0 0 12px rgba(0, 188, 212, 0.2);
  color: white;
}

.edit-form label {
  font-size: 14px;
  margin-top: 10px;
  display: block;
  color: #cccccc;
}

.edit-form input,
.edit-form textarea,
.edit-form select {
  width: 100%;
  padding: 10px;
  border-radius: 6px;
  border: none;
  margin-top: 4px;
  margin-bottom: 12px;
  background-color: #2a2a2a;
  color: white;
}

.edit-form input:focus,
.edit-form textarea:focus,
.edit-form select:focus {
  outline: 1px solid #00bcd4;
}

.form-buttons {
  display: flex;
  justify-content: flex-end;
}

.edit-form button {
  padding: 10px 14px;
  border: none;
  background-color: #00bcd4;
  color: #121212;
  font-weight: bold;
  border-radius: 6px;
  cursor: pointer;
}
</style>
