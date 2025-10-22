import { createRouter, createWebHistory } from 'vue-router'
import Login from '../components/Login.vue'
import Registro from '../components/Registro.vue'
import Productos from '../views/Productos.vue'
import Admin from '../views/Admin.vue'
import AdminCrearProducto from '../views/AdminCrearProducto.vue'
import Perfil from '../views/Perfil.vue'
import Carrito from '../views/Carrito.vue'
import ProcesoPago from '../views/ProcesoPago.vue'
import HistorialCompras from '../views/HistorialCompras.vue'

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
  { path: '/carrito', name: 'Carrito', component: Carrito },
  { path: '/proceso-pago', name: 'ProcesoPago', component: ProcesoPago, meta: { requiresAuth: true } },
  { path: '/historial-compras', name: 'HistorialCompras', component: HistorialCompras, meta: { requiresAuth: true } }

]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  try {
    const usuario = JSON.parse(localStorage.getItem('usuario') || 'null')
    const token = localStorage.getItem('token')

    // Verificar que el token no esté expirado
    if (token) {
      try {
        const tokenPayload = JSON.parse(atob(token.split('.')[1]))
        const currentTime = Math.floor(Date.now() / 1000)
        
        if (tokenPayload.exp && tokenPayload.exp < currentTime) {
          // Token expirado, limpiar y redirigir al login
          localStorage.removeItem('usuario')
          localStorage.removeItem('token')
          if (to.path !== '/') {
            next('/')
            return
          }
        }
      } catch (tokenError) {
        // Token inválido, limpiar y redirigir al login
        localStorage.removeItem('usuario')
        localStorage.removeItem('token')
        if (to.path !== '/') {
          next('/')
          return
        }
      }
    }

    if (to.meta.requiresAuth) {
      if (!usuario || !token) {
        next('/')
        return
      }
      if (to.meta.requiresAdmin && usuario.rol !== 'admin') {
        // Redirigir a productos si no es admin
        next('/productos')
        return
      }
    }
    
    // Si ya está logueado y va al login, redirigir según su rol
    if (to.path === '/' && usuario && token) {
      if (usuario.rol === 'admin') {
        next('/admin')
      } else {
        next('/productos')
      }
      return
    }
    
    next()
  } catch (error) {
    console.error('Error en navegación:', error)
    // En caso de error, limpiar y ir al login
    localStorage.removeItem('usuario')
    localStorage.removeItem('token')
    next('/')
  }
})

export default router
