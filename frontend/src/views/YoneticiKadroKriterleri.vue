<template>
    <div class="kriter-sayfa">
      <h2>📋 Kadro Kriterleri</h2>
  
      <div class="kriter-tablosu">
        <table>
            <thead>
  <tr>
    <th>ID</th>
    <th>Bölüm</th>
    <th>Unvan</th>
    <th>Faaliyet</th>
    <th>Asgari Adet</th>
  </tr>
</thead>
<tbody>
  <tr v-for="k in kriterler" :key="k.id">
    <td>{{ k.id }}</td>
    <td>{{ k.bolum }}</td>
    <td>{{ k.unvan }}</td>
    <td>{{ k.faaliyet_kodu }} - {{ k.faaliyet_adi }}</td>
    <td><input type="number" v-model.number="k.asgari_adet" /></td>
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
      axios.get('http://localhost:8000/api/kadro-kriterleri/', {
        headers: { Authorization: `Bearer ${token}` }
      }).then(res => this.kriterler = res.data)
        .catch(e => console.error(e))
    },
    methods: {
      guncelle() {
        const token = localStorage.getItem('token')
        axios.put('http://localhost:8000/api/kadro-kriterleri/', this.kriterler, {
          headers: { Authorization: `Bearer ${token}` }
        }).then(() => alert('Kriterler güncellendi'))
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
  