<template>
    <div class="admin-panel">
      <h2>Admin Panel</h2>
      <nav class="admin-menu">
  <button @click="$router.push('/admin/announcements')">📋 İlan Listesi</button>
  <button @click="$router.push('/admin/announcements/new')">➕ Yeni İlan</button>
  <button @click="$router.push('/admin/applications')">🗃️ Başvurular</button>
  <button @click="$router.push('/admin/kullanicilar')">👥 Kullanıcılar</button>
</nav>
      <router-view />
    </div>
  </template>
  
  <style scoped>
  .admin-panel {
    padding: 40px;
    background-color: #121212;
    color: white;
  }
  
  .admin-menu {
    display: flex;
    gap: 12px;
    margin-bottom: 24px;
  }
  
  .admin-menu button {
    background-color: #00bcd4;
    border: none;
    padding: 10px 14px;
    border-radius: 6px;
    cursor: pointer;
    font-weight: bold;
    color: #121212;
  }
  </style>
  