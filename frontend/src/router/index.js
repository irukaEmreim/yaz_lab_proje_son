import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import AnnouncementList from '../views/AnnouncementList.vue'
import AnnouncementNew from '../views/AnnouncementNew.vue'
import ApplicationList from '../views/ApplicationList.vue'
import YoneticiDashboard from '../views/YoneticiDashboard.vue'
import YoneticiJuriEkle from '../views/YoneticiJuriEkle.vue'
import YoneticiIlanlar from '../views/YoneticiIlanlar.vue'
import AdayDashboard from '../views/AdayDashboard.vue' // ✅ eklendi
import BasvuruForm from '../views/BasvuruForm.vue'  // En üste ekle

const routes = [
  { path: '/', name: 'Login', component: LoginView },

  {
    path: '/admin',
    name: 'AdminDashboard',
    component: AdminDashboard,
    meta: { requiresAuth: true, role: 'admin' }, // ✅ eklendi
    children: [
      { path: 'announcements', component: AnnouncementList },
      { path: 'announcements/new', component: AnnouncementNew },
      { path: 'applications', component: ApplicationList }
    ]
  },

  {
    path: '/yonetici',
    name: 'YoneticiDashboard',
    component: YoneticiDashboard,
    meta: { requiresAuth: true, role: 'yonetici' }, // ✅ eklendi
    children: [
      { path: 'juri-ekle', component: YoneticiJuriEkle },
      { path: 'ilanlar', component: YoneticiIlanlar }
    ]
  },
  {
    path: '/yonetici/kadro-kriterleri',
    component: () => import('@/views/YoneticiKadroKriterleri.vue'),
    meta: { requiresAuth: true, role: 'yonetici' } // ✅ eklendi
  },
  {
    path: '/yonetici/puan-kriterleri',
    component: () => import('@/views/YoneticiPuanKriterleri.vue'),
    meta: { requiresAuth: true, role: 'yonetici' } // ✅ eklendi
  },
  {
    path: '/aday',
    component: AdayDashboard,
    meta: { requiresAuth: true, role: 'aday' } // ✅ zaten vardı
  },
  {
    path: '/aday/ilan/:id/detay',
    component: () => import('@/views/IlanDetay.vue'),
    meta: { requiresAuth: true, role: 'aday' }
  },
  {
    path: '/aday/basvuru/:id',
    component: BasvuruForm,
    meta: { requiresAuth: true, role: 'aday' }
  }
  
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  let user = null

  try {
    const payload = JSON.parse(atob(token?.split('.')[1] || ''))
    user = payload
  } catch (e) {
    user = null
  }

  if (to.meta.requiresAuth) {
    if (!token) {
      alert("Lütfen giriş yapınız.")
      return next('/')
    }

    if (to.meta.role && to.meta.role !== user?.role) {
      alert("Bu sayfaya erişim yetkiniz yok.")
      return next('/')
    }
  }

  next()
})

export default router
