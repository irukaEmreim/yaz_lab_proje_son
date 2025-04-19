<template>
    <div class="login-container">
      <h2>Giriş Yap</h2>
      <LoginForm />
    </div>
  </template>
  
  <script>
  import LoginForm from '../components/LoginForm.vue'
  
  export default {
    components: { LoginForm }
  }
  </script>
  
  <style scoped>
  .login-container {
    max-width: 400px;
    margin: 100px auto;
  }
  </style>
  