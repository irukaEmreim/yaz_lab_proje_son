<template>
  <div>
    <h3>📋 Tüm İlanlar</h3>
    <div
      v-for="ilan in announcements"
      :key="ilan.id"
      class="ilan-karti"
    >
      <h4>{{ ilan.title }}</h4>
      <p><strong>Pozisyon:</strong> {{ ilan.position_type }}</p>
      <p><strong>Açıklama:</strong> {{ ilan.description || '-' }}</p>
      <p><strong>Tarih:</strong> {{ ilan.start_date }} - {{ ilan.end_date }}</p>
      <p><strong>Başvuru Sayısı:</strong> {{ ilan.app_count }}</p>
      <button @click="toggleEditForm(ilan.id)">✏️ Düzenle</button>

      <form
        v-if="activeEditId === ilan.id"
        @submit.prevent="updateAnnouncement"
        class="edit-form"
      >
        <label>Başlık</label>
        <input v-model="form.title" required />

        <label>Pozisyon</label>
        <select v-model="form.position_type" required>
          <option>Dr. Öğr. Üyesi</option>
          <option>Doçent</option>
          <option>Profesör</option>
        </select>

        <label>Açıklama</label>
        <textarea v-model="form.description" rows="3" />

        <label>Başlangıç Tarihi</label>
        <input type="date" v-model="form.start_date" required />

        <label>Bitiş Tarihi</label>
        <input type="date" v-model="form.end_date" required />

        <div class="form-buttons">
          <button type="submit">💾 Kaydet</button>
          <button type="button" class="cancel" @click="cancelEdit">❌ İptal</button>
        </div>
      </form>
    </div>
  </div>
</template>

  
<script>
import axios from "axios"

export default {
  data() {
    return {
      announcements: [],
      applications: [],
      form: {},
      activeEditId: null 
    }
  },
  async created() {
    const token = localStorage.getItem("token")

    const [ilanRes, appRes] = await Promise.all([
      axios.get("http://127.0.0.1:8000/api/announcements/", {
        headers: { Authorization: `Bearer ${token}` }
      }),
      axios.get("http://127.0.0.1:8000/api/applications/", {
        headers: { Authorization: `Bearer ${token}` }
      })
    ])

    this.announcements = ilanRes.data.map(ilan => {
      const count = appRes.data.filter(app => app.announcement_id === ilan.id).length
      return { ...ilan, app_count: count }
    })
  },
  methods: {
    toggleEditForm(id) {
      const ilan = this.announcements.find(a => a.id === id)
      this.form = { ...ilan }
      this.activeEditId = id
    },
    cancelEdit() {
      this.activeEditId = null
      this.form = {}
    },
    async updateAnnouncement() {
      const token = localStorage.getItem("token")
      const res = await axios.put(
        `http://127.0.0.1:8000/api/announcements/${this.form.id}/`,
        this.form,
        { headers: { Authorization: `Bearer ${token}` } }
      )
      const index = this.announcements.findIndex(i => i.id === this.form.id)
      this.announcements[index] = res.data
      this.cancelEdit()
      alert("İlan güncellendi!")
    }
  }
}
</script>

  
  <style scoped>
  .ilan {
    margin-bottom: 10px;
  }
  .edit-form {
  margin-top: 24px;
  padding: 20px;
  background-color: #1e1e1e;
  border-radius: 12px;
  box-shadow: 0 0 12px rgba(0, 188, 212, 0.2);
  max-width: 500px;
}

.edit-form label {
  color: #cccccc;
  font-size: 14px;
  margin-top: 10px;
  display: block;
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
  gap: 10px;
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

.edit-form .cancel {
  background-color: #888;
  color: white;
}

.ilan-karti {
  background: #1e1e1e;
  padding: 20px;
  margin-bottom: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 188, 212, 0.1);
}

.ilan-karti h4 {
  margin: 0 0 8px;
}

.ilan-karti p {
  margin: 4px 0;
}
.ilan-karti button {
  margin-top: 10px;
  padding: 8px 16px;
  border: none;
  background-color: transparent;
  border: 1px solid #00bcd4;
  color: #00bcd4;
  font-weight: bold;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.ilan-karti button:hover {
  background-color: #00bcd4;
  color: #121212;
  box-shadow: 0 0 6px rgba(0, 188, 212, 0.4);
}

  </style>
  