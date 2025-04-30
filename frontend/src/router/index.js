import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import AnnouncementList from '../views/AnnouncementList.vue'
import AnnouncementNew from '../views/AnnouncementNew.vue'
import ApplicationList from '../views/ApplicationList.vue'
import YoneticiDashboard from '../views/YoneticiDashboard.vue'
import YoneticiJuriEkle from '../views/YoneticiJuriEkle.vue'
import YoneticiIlanlar from '../views/YoneticiIlanlar.vue'
import AdayDashboard from '../views/AdayDashboard.vue' 
import BasvuruForm from '../views/BasvuruForm.vue' 

const routes = [
  { path: '/', name: 'Login', component: LoginView },

  {
    path: '/admin',
    name: 'AdminDashboard',
    component: AdminDashboard,
    meta: { requiresAuth: true, role: 'admin' }, 
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
    meta: { requiresAuth: true, role: 'yonetici' }, 
    children: [
      { path: 'juri-ekle', component: YoneticiJuriEkle },
      { path: 'ilanlar', component: YoneticiIlanlar }
    ]
  },
  {
    path: '/yonetici/kadro-kriterleri',
    component: () => import('@/views/YoneticiKadroKriterleri.vue'),
    meta: { requiresAuth: true, role: 'yonetici' } 
  },
  {
    path: '/yonetici/puan-kriterleri',
    component: () => import('@/views/YoneticiPuanKriterleri.vue'),
    meta: { requiresAuth: true, role: 'yonetici' } 
  },
  {
    path: '/aday',
    component: AdayDashboard,
    meta: { requiresAuth: true, role: 'aday' } 
  },
  {
    path: '/aday/ilan/:id/detay',
    component: () => import('@/views/IlanDetay.vue'),
    meta: { requiresAuth: true, role: 'aday' }
  },
  {
    path: '/aday/ilan/:id/basvur',
    name: 'BasvuruForm',
    component: BasvuruForm,
    meta: { requiresAuth: true, role: 'aday' }
  },
  {
    path: '/aday/basvurularim',
    name: 'Basvurularim',
    component: () => import('@/views/AdayBasvurularim.vue')
  },
  {
    path: '/aday/basvuru/:id',
    name: 'BasvuruDetay',
    component: () => import('@/views/BasvuruDetay.vue')
  },
  {
    path: '/aday/profilim',
    name: 'Profilim',
    component: () => import('@/views/AdayProfilim.vue')
  },
  {
    path: '/uye-ol',
    name: 'AdayRegister',
    component: () => import('@/views/AdayRegister.vue')
  },
  {
    path: '/juri/dashboard',
    name: 'JuriDashboard',
    component: () => import('@/views/JuriDashboard.vue')
  },
  {
    path: '/juri/basvuru/:id',
    name: 'JuriBasvuruDetay',
    component: () => import('@/views/JuriBasvuruDetay.vue')
  },
  {
    path: '/yonetici/yonetici-degerlendirilecek-ilanlar',
    component: () => import('@/views/YoneticiDegerlendirilecekIlanlariListeleme.vue'),  
    meta: { requiresAuth: true, role: 'yonetici' }
  },
  {
    path: '/yonetici/basvuru/:id/sonuclandir',
    name: 'YoneticiDegerlendirme',
    component: () => import('@/views/YoneticiDegerlendirme.vue'),
    meta: { requiresAuth: true, role: 'yonetici' }
  },
  {
    path: '/aday/tablo5-olustur/:id',
    name: 'Tablo5Olustur',
    component: () => import('@/views/Tablo5Olustur.vue'),
    meta: { requiresAuth: true, role: 'aday' }
  },
  {
    path: '/admin/kullanicilar',
    name: 'AdminKullanicilar',
    component: () => import('@/views/AdminKullanicilar.vue'),
    meta: { requiresAuth: true, role: 'admin' }
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
