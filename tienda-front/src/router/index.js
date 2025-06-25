import { createRouter, createWebHistory } from 'vue-router'
import Login from '../components/Login.vue'
import Registro from '../components/Registro.vue'
import Productos from '../views/Productos.vue'
import Admin from '../views/Admin.vue'
import AdminCrearProducto from '../views/AdminCrearProducto.vue'
import Perfil from '../views/Perfil.vue'

const routes = [
  { path: '/', component: Login },
  { path: '/registro', component: Registro },
  { path: '/perfil', component: Perfil, meta: { requiresAuth: true } },
  { path: '/productos', component: Productos, meta: { requiresAuth: true } },
  { path: '/admin', component: Admin, meta: { requiresAuth: true, requiresAdmin: true } },
  {
    path: '/admin/crear-producto',
    component: AdminCrearProducto,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/no-autorizado',
    component: {
      template: '<div style="padding:40px; color:white;"><h2>No autorizado</h2><p>No tienes permisos para acceder a esta página.</p></div>'
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const usuario = JSON.parse(localStorage.getItem('usuario'))
  const token = localStorage.getItem('token')

  if (to.meta.requiresAuth) {
    if (!usuario || !token) {
      next('/')
      return
    }
    if (to.meta.requiresAdmin && usuario.rol !== 'admin') {
      next('/no-autorizado')
      return
    }
  }
  next()
})

export default router
