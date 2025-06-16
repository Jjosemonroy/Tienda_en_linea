import { createRouter, createWebHistory } from 'vue-router'
import Login from '../components/Login.vue'
import Productos from '../views/Productos.vue'
import Admin from '../views/Admin.vue'
import AdminCrearProducto from '../views/AdminCrearProducto.vue'

const routes = [
  { path: '/', component: Login },
  { path: '/productos', component: Productos },
  { path: '/admin', component: Admin },
  {
    path: '/admin/crear-producto',
    component: AdminCrearProducto,
    meta: { requiresAdmin: true }
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

  if (to.meta.requiresAdmin) {
    if (usuario?.rol === 'admin') {
      next()
    } else {
      next('/no-autorizado')
    }
  } else {
    next()
  }
})

export default router
