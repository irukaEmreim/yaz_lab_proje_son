import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import AnnouncementList from '../views/AnnouncementList.vue'
import AnnouncementNew from '../views/AnnouncementNew.vue'
import ApplicationList from '../views/ApplicationList.vue'

const routes = [
  { path: '/', name: 'Login', component: LoginView },
  {
    path: '/admin',
    name: 'AdminDashboard',
    component: AdminDashboard,
    children: [
      { path: 'announcements', component: AnnouncementList },
      { path: 'announcements/new', component: AnnouncementNew },
      { path: 'applications', component: ApplicationList },
    ]
  }
]

const router = createRouter({
    history: createWebHistory(),
    routes
  })

export default router
