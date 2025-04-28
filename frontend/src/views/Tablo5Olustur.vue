<template>
    <div class="tablo5-olustur">
      <h2>Tablo 5 oluşturuluyor, lütfen bekleyin...</h2>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  
  export default {
    async created() {
      const token = localStorage.getItem('token')
      const applicationId = this.$route.params.id
  
      try {
        await axios.get(`http://localhost:8000/api/tablo5/${applicationId}/`, {}, {
          headers: { Authorization: `Bearer ${token}` }
        })
  
        alert("Tablo 5 başarıyla oluşturuldu!")
        this.$router.push('/aday')
  
      } catch (err) {
        console.error("Tablo 5 oluşturulamadı:", err)
        alert("Tablo 5 oluşturulurken hata oluştu.")
        this.$router.push('/aday')
      }
    }
  }
  </script>
  
  <style scoped>
  .tablo5-olustur {
    background: #121212;
    color: white;
    text-align: center;
    padding: 40px;
  }
  </style>
  