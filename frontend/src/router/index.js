import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import AnnouncementList from '../views/AnnouncementList.vue'
import AnnouncementNew from '../views/AnnouncementNew.vue'
import ApplicationList from '../views/ApplicationList.vue'
import YoneticiDashboard from '../views/YoneticiDashboard.vue'
import YoneticiJuriEkle from '../views/YoneticiJuriEkle.vue'
import YoneticiIlanlar from '../views/YoneticiIlanlar.vue'

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
  },
  {
    path: '/yonetici',
    name: 'YoneticiDashboard',
    component: YoneticiDashboard,
    children: [
      { path: 'juri-ekle', component: YoneticiJuriEkle },
      { path: 'ilanlar', component: YoneticiIlanlar }
    ]
  },
  {
    path: '/yonetici/kadro-kriterleri',
    component: () => import('@/views/YoneticiKadroKriterleri.vue')
  },
  {
    path: '/yonetici/puan-kriterleri',
    component: () => import('@/views/YoneticiPuanKriterleri.vue')
  }
]

const router = createRouter({
    history: createWebHistory(),
    routes
  })

export default router
