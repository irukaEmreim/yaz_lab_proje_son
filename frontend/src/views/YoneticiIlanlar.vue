<template>
    <div class="ilanlar-sayfa">
      <h2>📄 İlanlar ve Jüri Atama</h2>
  
      <div v-for="ilan in announcements" :key="ilan.id" class="ilan-karti">
        <h3>{{ ilan.title }}</h3>
        <p>{{ ilan.description }}</p>
        <button @click="loadJuries(ilan.id)">👥 Jüri Ata</button>
  
        <div v-if="selectedIlan === ilan.id" class="juri-ata-blok">
          <h4>Atanmış Jüriler</h4>
          <ul>
            <li v-for="j in juries" :key="j.id">👤 TC: {{ j.jury_tc }}</li>
          </ul>
  
          <select v-model="selectedJuryTc">
            <option disabled value="">Jüri Seç</option>
            <option v-for="j in availableJuries" :key="j.id" :value="j.tc_kimlik_no">
              {{ j.tc_kimlik_no }}
            </option>
          </select>
          <button @click="assignJury(ilan.id)">➕ Ata</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  
  export default {
    data() {
      return {
        announcements: [],
        juries: [],
        availableJuries: [],
        selectedJuryTc: '',
        selectedIlan: null
      }
    },
    async created() {
      const token = localStorage.getItem('token')
      const ilanRes = await axios.get('http://127.0.0.1:8000/api/announcements/', {
        headers: { Authorization: `Bearer ${token}` }
      })
      const juryRes = await axios.get('http://127.0.0.1:8000/api/uygun-juriler/', {
        headers: { Authorization: `Bearer ${token}` }
      })
      this.announcements = ilanRes.data
      this.availableJuries = juryRes.data
    },
    methods: {
      async loadJuries(announcementId) {
        const token = localStorage.getItem('token')
        const res = await axios.get(`http://127.0.0.1:8000/api/juri-atamasi/${announcementId}/`, {
          headers: { Authorization: `Bearer ${token}` }
        })
        this.juries = res.data
        this.selectedIlan = announcementId
      },
      async assignJury(announcementId) {
        const token = localStorage.getItem('token')
        await axios.post('http://127.0.0.1:8000/api/juri-ekle/', {
          announcement_id: announcementId,
          tc_kimlik_no: this.selectedJuryTc
        }, {
          headers: { Authorization: `Bearer ${token}` }
        })
        alert('Jüri atandı!')
        this.selectedJuryTc = ''
        this.loadJuries(announcementId)
      }
    }
  }
  </script>
  
  <style scoped>
  .ilanlar-sayfa {
    padding: 40px;
    color: white;
  }
  .ilan-karti {
    background: #1e1e1e;
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 20px;
  }
  .juri-ata-blok {
    margin-top: 12px;
    background-color: #2a2a2a;
    padding: 10px;
    border-radius: 8px;
  }
  select {
    width: 100%;
    padding: 8px;
    margin-top: 8px;
    background: #2e2e2e;
    border: none;
    color: white;
    border-radius: 6px;
  }
  button {
    margin-top: 8px;
    padding: 8px 16px;
    border: none;
    background: #00bcd4;
    color: #121212;
    border-radius: 6px;
    font-weight: bold;
    cursor: pointer;
  }
  </style>
  