<template>
  <div class="kriter-panel">
    <h2>📋 Kadro Kriterleri</h2>
    <div class="tablo-container">
      <table>
        <thead>
          <tr>
            <th>Bölüm</th>
            <th>Unvan</th>
            <th>Faaliyet</th>
            <th>Asgari Adet</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="k in kriterler" :key="k.id">
            <td>{{ k.bolum }}</td>
            <td>{{ k.unvan }}</td>
            <td><span class="badge">{{ k.faaliyet_kodu }}</span> <br> <small>{{ k.faaliyet_adi }}</small></td>
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
.kriter-panel {
  padding: 40px;
  color: #f0f0f0;
  background-color: #111;
  min-height: 100vh;
}
.tablo-container {
  overflow-x: auto;
  background-color: #1e1e1e;
  padding: 20px;
  border-radius: 10px;
}
table {
  width: 100%;
  border-collapse: collapse;
}
th, td {
  padding: 12px;
  border: 1px solid #444;
  text-align: center;
}
th {
  background-color: #2b2b2b;
}
tr:hover {
  background-color: #2d2d2d;
}
input {
  padding: 6px;
  background-color: #292929;
  color: white;
  border: 1px solid #555;
  border-radius: 4px;
  width: 80px;
}
.badge {
  background-color: #00bcd4;
  color: #000;
  padding: 3px 8px;
  border-radius: 4px;
  font-weight: bold;
}
button {
  margin-top: 20px;
  background-color: #2196f3;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  font-weight: bold;
  cursor: pointer;
}
button:hover {
  background-color: #1976d2;
}
</style>