<template>
    <div class="kriter-sayfa">
      <h2>📊 Puan Kriterleri</h2>
  
      <div class="kriter-tablosu">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Bölüm ID</th>
              <th>Unvan</th>
              <th>Faaliyet Kodu</th>
              <th>Asgari Puan</th>
              <th>Azami Puan</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in kriterler" :key="p.id">
              <td>{{ p.id }}</td>
              <td>{{ p.bolum }}</td>
              <td>{{ p.unvan }}</td>
              <td>{{ p.faaliyet_kodu }}</td>
              <td><input type="number" v-model.number="p.asgari_puan" /></td>
              <td><input type="number" v-model.number="p.azami_puan" /></td>
            </tr>
          </tbody>
        </table>
      </div>
  
      <button @click="guncelle">💾 Güncelle</button>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  
  export default {
    data() {
      return { kriterler: [] }
    },
    mounted() {
      const token = localStorage.getItem('token')
      axios.get('http://localhost:8000/api/puan-kriterleri/', {
        headers: { Authorization: `Bearer ${token}` }
      }).then(res => this.kriterler = res.data)
        .catch(e => console.error(e))
    },
    methods: {
      guncelle() {
        const token = localStorage.getItem('token')
        axios.put('http://localhost:8000/api/puan-kriterleri/', this.kriterler, {
          headers: { Authorization: `Bearer ${token}` }
        }).then(() => alert('Puan kriterleri güncellendi'))
          .catch(() => alert('Hata!'))
      }
    }
  }
  </script>
  
  <style scoped>
  .kriter-sayfa {
    padding: 40px;
    color: white;
  }
  .kriter-tablosu table {
    width: 100%;
    border-collapse: collapse;
    background: #1e1e1e;
  }
  .kriter-tablosu th, .kriter-tablosu td {
    padding: 10px;
    border: 1px solid #444;
    text-align: center;
  }
  .kriter-tablosu th {
    background: #2d2d2d;
  }
  .kriter-tablosu tr:hover {
    background: #333;
  }
  input {
    width: 70px;
    padding: 5px;
    background: #2e2e2e;
    border: 1px solid #555;
    color: white;
  }
  button {
    margin-top: 20px;
    padding: 10px 20px;
    background: #2196f3;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-weight: bold;
  }
  button:hover {
    background: #1976d2;
  }
  </style>
  