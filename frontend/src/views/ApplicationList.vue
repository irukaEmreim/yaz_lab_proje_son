<template>
  <div class="application-page">
    <h3>🗃️ Başvurular</h3>

    <div v-for="ilan in groupedApplications" :key="ilan.id" class="application-card">
      <h4>{{ ilan.title }}</h4>
      <p class="desc">{{ ilan.description || '-' }}</p>
      <p class="dates">{{ ilan.start_date }} - {{ ilan.end_date }}</p>

      <ul class="applicant-list">
        <li v-for="app in ilan.applications" :key="app.id">
          <span>👤 {{ app.candidate_tc }}</span>
          <span class="status">📌 {{ app.status }}</span>
        </li>
      </ul>
    </div>
  </div>
</template>

  
<script>
import axios from "axios"

export default {
  data() {
    return {
      groupedApplications: []
    }
  },
  async created() {
    const token = localStorage.getItem("token")

const ilanRes = await axios.get("http://127.0.0.1:8000/api/announcements/", {
  headers: { Authorization: `Bearer ${token}` }
})

const appRes = await axios.get("http://127.0.0.1:8000/api/applications/", {
  headers: { Authorization: `Bearer ${token}` }
})
if (!token) {
  this.$router.push("/")
  return
}

    const grouped = ilanRes.data.map(ilan => ({
      ...ilan,
      applications: appRes.data
        .filter(app => app.announcement_id === ilan.id)
        .map(app => ({
          id: app.id,
          candidate_tc: app.candidate_tc, // backend'den geliyor olmalı
          status: app.status
        }))
    }))

    this.groupedApplications = grouped
  }
}
</script>


<style scoped>

.application-page {
  padding: 24px;
  color: white;
}

.application-card {
  background: #1e1e1e;
  padding: 20px;
  margin-bottom: 24px;
  border-radius: 12px;
  box-shadow: 0 0 12px rgba(0, 188, 212, 0.1);
}

.application-card h4 {
  margin-bottom: 6px;
  color: #00bcd4;
}

.application-card .desc {
  margin: 4px 0;
  color: #cccccc;
}

.application-card .dates {
  font-size: 13px;
  margin-bottom: 10px;
  color: #999;
}

.applicant-list {
  list-style: none;
  padding: 0;
  margin: 0;
  background-color: #2a2a2a;
  border-radius: 8px;
  overflow: hidden;
}

.applicant-list li {
  display: flex;
  justify-content: space-between;
  padding: 10px 14px;
  border-bottom: 1px solid #444;
  font-size: 14px;
}

.applicant-list li:last-child {
  border-bottom: none;
}

.status {
  color: #00e676;
  font-weight: bold;
}

</style>