<template>
  <div class="carrito-container">
    <!-- Header -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">Mi Carrito</h1>
        <p class="page-subtitle">Revisa y gestiona tus productos seleccionados</p>
      </div>
      <div class="header-actions">
        <div class="cart-summary">
          <span class="cart-count">{{ carrito.items?.length || 0 }}</span>
          <span class="cart-label">productos</span>
        </div>
      </div>
    </div>

    <!-- Contenido principal -->
    <div class="cart-content">
      <div v-if="cargando" class="loading-state">
        <div class="loading-spinner"></div>
        <p>Cargando tu carrito...</p>
      </div>

      <div v-else-if="!carrito.items || carrito.items.length === 0" class="empty-cart">
        <div class="empty-icon">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13m0 0l-2.5 5M7 13l2.5 5m6-5v6a2 2 0 01-2 2H9a2 2 0 01-2-2v-6m8 0V9a2 2 0 00-2-2H9a2 2 0 00-2 2v4.01"></path>
          </svg>
        </div>
        <h3>Tu carrito está vacío</h3>
        <p>Agrega algunos productos para comenzar tu compra</p>
        <router-link to="/productos" class="btn btn-primary">
          <svg class="btn-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"></path>
          </svg>
          Ver productos
        </router-link>
      </div>

      <div v-else class="cart-items">
        <!-- Lista de productos -->
        <div class="items-section">
          <div class="section-header">
            <h2>Productos en el carrito</h2>
          </div>
          
          <div class="items-list">
            <div v-for="item in carrito.items" :key="item.id" class="cart-item">
              <div class="item-image">
                <img :src="getImageUrl(item.imagen)" :alt="item.producto" class="product-image" />
              </div>
              
              <div class="item-details">
                <div class="item-info">
                  <h3 class="item-name">{{ item.producto }}</h3>
                  <p class="item-price">Q{{ item.precio.toFixed(2) }} cada uno</p>
                </div>
                
                <div class="item-actions">
                  <div class="quantity-controls">
                    <button 
                      class="quantity-btn" 
                      @click="cambiarCantidad(item, -1)" 
                      :disabled="item.cantidad <= 1"
                    >
                      <svg class="quantity-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4"></path>
                      </svg>
                    </button>
                    
                    <span class="quantity-display">{{ item.cantidad }}</span>
                    
                    <button class="quantity-btn" @click="cambiarCantidad(item, 1)">
                      <svg class="quantity-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
                      </svg>
                    </button>
                  </div>
                  
                  <div class="item-total">
                    <span class="total-label">Total:</span>
                    <span class="total-amount">Q{{ item.total_linea.toFixed(2) }}</span>
                  </div>
                  
                  <button class="remove-btn" @click="eliminarItem(item)">
                    <svg class="remove-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                    </svg>
                    Eliminar
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Resumen de compra -->
        <div class="cart-summary-section">
          <div class="summary-card">
            <div class="summary-header">
              <h3>Resumen de compra</h3>
            </div>
            
            <div class="summary-content">
              <div class="summary-row">
                <span class="summary-label">Subtotal:</span>
                <span class="summary-value">Q{{ carrito.total_carrito.toFixed(2) }}</span>
              </div>
              
              <div class="summary-row">
                <span class="summary-label">Envío:</span>
                <span class="summary-value">Gratis</span>
              </div>
              
              <div class="summary-divider"></div>
              
              <div class="summary-row total">
                <span class="summary-label">Total:</span>
                <span class="summary-value">Q{{ carrito.total_carrito.toFixed(2) }}</span>
              </div>
            </div>
            
            <div class="summary-actions">
              <button class="btn btn-primary btn-lg checkout-btn" @click="finalizarCompra">
                <svg class="btn-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H5a3 3 0 00-3 3v8a3 3 0 003 3z"></path>
                </svg>
                Procesar pago
              </button>
              
              <router-link to="/productos" class="btn btn-outline btn-lg continue-shopping">
                <svg class="btn-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"></path>
                </svg>
                Continuar comprando
              </router-link>
            </div>
      </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
import { getApiUrl, getImageUrl } from '../config/api.js'

const router = useRouter()
const toast = useToast()
const usuario = ref(null)
const carrito = ref({ items: [], total_carrito: 0 })
const cargando = ref(true)

onMounted(async () => {
  usuario.value = JSON.parse(localStorage.getItem('usuario'))
  if (!usuario.value) {
    router.push('/login')
    return
  }
  await cargarCarrito()
})

async function cargarCarrito() {
  cargando.value = true
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get(`${getApiUrl('cart')}/${usuario.value.id}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    carrito.value = {
      ...response.data,
      items: response.data.items.map(item => ({
        ...item,
        imagen: item.imagen || null
      }))
    }
  } catch (error) {
    console.error('Error al cargar el carrito:', error)
    carrito.value = { items: [], total_carrito: 0 }
    toast.error('No se pudo cargar el carrito')
  }
  cargando.value = false
}

async function cambiarCantidad(item, delta) {
  const nuevaCantidad = item.cantidad + delta
  if (nuevaCantidad < 1) return

  try {
    const token = localStorage.getItem('token')
    await axios.post(getApiUrl('updateCart'), {
      usuario_id: usuario.value.id,
      producto_id: item.producto_id,
      cantidad: nuevaCantidad
    }, {
      headers: { Authorization: `Bearer ${token}` }
    })
    
    await cargarCarrito()
    toast.success('Cantidad actualizada')
  } catch (error) {
    console.error('Error al actualizar cantidad:', error)
    toast.error('Error al actualizar la cantidad')
  }
}

async function eliminarItem(item) {
  try {
    const token = localStorage.getItem('token')
    await axios.post(getApiUrl('removeFromCart'), {
      usuario_id: usuario.value.id,
      producto_id: item.producto_id,
      cantidad: item.cantidad
    }, {
      headers: { Authorization: `Bearer ${token}` }
    })
    
    await cargarCarrito()
    
    // Actualizar el contador del carrito en la barra lateral
    actualizarContadorCarrito()
    
    toast.success('Producto eliminado del carrito')
  } catch (error) {
    console.error('Error al eliminar item:', error)
    toast.error('Error al eliminar el producto')
  }
}

// Función para actualizar el contador del carrito
async function actualizarContadorCarrito() {
  if (!usuario.value) return
  
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get(`${getApiUrl('cart')}/${usuario.value.id}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    
    if (response.status === 200) {
      // Calcular el número de items en el carrito
      const carritoData = response.data
      const carritoCount = carritoData.items ? carritoData.items.length : 0
      
      // Disparar un evento personalizado para que el Sidebar lo detecte
      const carritoEvent = new CustomEvent('carritoActualizado', { 
        detail: { count: carritoCount } 
      })
      window.dispatchEvent(carritoEvent)
    }
  } catch (error) {
    console.error('Error al actualizar contador del carrito:', error)
  }
}

async function finalizarCompra() {
  if (carrito.value.items.length === 0) {
    toast.warning('Tu carrito está vacío')
    return
  }

  router.push('/proceso-pago')
}
</script>

<style scoped>
.carrito-container {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-2xl);
  padding: var(--spacing-xl);
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: var(--border-radius-lg);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  color: white;
}

.header-content {
  flex: 1;
}

.page-title {
  font-size: var(--font-size-3xl);
  font-weight: 700;
  color: white;
  margin-bottom: var(--spacing-xs);
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.page-subtitle {
  color: rgba(255, 255, 255, 0.9);
  font-size: var(--font-size-base);
}

.cart-summary {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-xs);
  background: rgba(255, 255, 255, 0.2);
  padding: var(--spacing-md);
  border-radius: var(--border-radius);
  backdrop-filter: blur(10px);
}

.cart-count {
  font-size: var(--font-size-2xl);
  font-weight: 700;
  color: white;
}

.cart-label {
  color: rgba(255, 255, 255, 0.8);
  font-size: var(--font-size-sm);
}

.cart-content {
  display: grid;
  grid-template-columns: 1fr 350px;
  gap: var(--spacing-xl);
}

.loading-state {
  grid-column: 1 / -1;
  text-align: center;
  padding: var(--spacing-2xl);
  color: var(--text-muted);
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #e2e8f0;
  border-top: 4px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto var(--spacing-lg);
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-cart {
  grid-column: 1 / -1;
  text-align: center;
  padding: var(--spacing-2xl);
  color: var(--text-muted);
}

.empty-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto var(--spacing-lg);
  color: var(--text-muted);
}

.empty-cart h3 {
  margin-bottom: var(--spacing-sm);
  color: var(--text-primary);
}

.empty-cart p {
  margin-bottom: var(--spacing-xl);
}

/* Botones mejorados */
.btn {
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-md) var(--spacing-lg);
  border: none;
  border-radius: var(--border-radius);
  font-weight: 500;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: var(--font-size-base);
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 4px 14px rgba(102, 126, 234, 0.4);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
}

.btn-outline {
  background: transparent;
  color: #667eea;
  border: 2px solid #667eea;
}

.btn-outline:hover {
  background: #667eea;
  color: white;
  transform: translateY(-1px);
}

.btn-lg {
  padding: var(--spacing-lg) var(--spacing-xl);
  font-size: var(--font-size-lg);
  font-weight: 600;
}

.btn-icon {
  width: 18px;
  height: 18px;
}

.items-section {
  background: white;
  border-radius: var(--border-radius-lg);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  border: 1px solid #e2e8f0;
}

.section-header {
  padding: var(--spacing-lg);
  border-bottom: 1px solid #e2e8f0;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
}

.section-header h2 {
  margin: 0;
  color: #2d3748;
  font-weight: 600;
}

.items-list {
  padding: var(--spacing-lg);
}

.cart-item {
  display: flex;
  gap: var(--spacing-lg);
  padding: var(--spacing-lg);
  border: 1px solid #e2e8f0;
  border-radius: var(--border-radius-lg);
  margin-bottom: var(--spacing-lg);
  background: white;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.cart-item:hover {
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
  border-color: #667eea;
}

.cart-item:last-child {
  margin-bottom: 0;
}

.item-image {
  flex-shrink: 0;
  width: 120px;
  height: 120px;
  border-radius: var(--border-radius);
  overflow: hidden;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.product-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.item-details {
  flex: 1;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.item-info {
  flex: 1;
}

.item-name {
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: #2d3748;
  margin-bottom: var(--spacing-xs);
}

.item-price {
  color: #4a5568;
  font-size: var(--font-size-base);
}

.item-actions {
  display: flex;
  align-items: center;
  gap: var(--spacing-lg);
}

.quantity-controls {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  background: #f8fafc;
  border-radius: var(--border-radius);
  padding: var(--spacing-xs);
  border: 1px solid #e2e8f0;
}

.quantity-btn {
  width: 32px;
  height: 32px;
  border: none;
  background: white;
  border-radius: var(--border-radius);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  border: 1px solid #e2e8f0;
}

.quantity-btn:hover:not(:disabled) {
  background: #667eea;
  color: white;
  border-color: #667eea;
  transform: scale(1.05);
}

.quantity-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.quantity-icon {
  width: 16px;
  height: 16px;
}

.quantity-display {
  min-width: 40px;
  text-align: center;
  font-weight: 600;
  color: #2d3748;
}

.item-total {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: var(--spacing-xs);
}

.total-label {
  font-size: var(--font-size-sm);
  color: #718096;
}

.total-amount {
  font-size: var(--font-size-lg);
  font-weight: 700;
  color: #667eea;
}

.remove-btn {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-sm) var(--spacing-md);
  background: transparent;
  border: 2px solid #e53e3e;
  border-radius: var(--border-radius);
  color: #e53e3e;
  cursor: pointer;
  transition: all 0.2s ease;
  font-weight: 500;
}

.remove-btn:hover {
  background: #e53e3e;
  color: white;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(229, 62, 62, 0.3);
}

.remove-icon {
  width: 16px;
  height: 16px;
}

.cart-summary-section {
  position: sticky;
  top: var(--spacing-lg);
}

.summary-card {
  background: white;
  border-radius: var(--border-radius-lg);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  border: 1px solid #e2e8f0;
}

.summary-header {
  padding: var(--spacing-lg);
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  border-bottom: 1px solid #e2e8f0;
}

.summary-header h3 {
  margin: 0;
  color: #2d3748;
  font-weight: 600;
}

.summary-content {
  padding: var(--spacing-lg);
}

.summary-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-md);
  color: #4a5568;
}

.summary-row:last-child {
  margin-bottom: 0;
}

.summary-label {
  color: #4a5568;
  font-size: var(--font-size-base);
}

.summary-value {
  font-weight: 600;
  color: #2d3748;
}

.summary-divider {
  height: 1px;
  background: #e2e8f0;
  margin: var(--spacing-lg) 0;
}

.summary-row.total {
  margin-top: var(--spacing-lg);
  padding-top: var(--spacing-lg);
  border-top: 2px solid #e2e8f0;
}

.summary-row.total .summary-value {
  font-size: var(--font-size-xl);
  color: #667eea;
  font-weight: 700;
}

.summary-actions {
  padding: var(--spacing-lg);
  border-top: 1px solid #e2e8f0;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
  background: #f8fafc;
}

.checkout-btn {
  width: 100%;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 4px 14px rgba(102, 126, 234, 0.4);
  font-weight: 600;
}

.checkout-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
}

.continue-shopping {
  width: 100%;
  justify-content: center;
  background: transparent;
  color: #667eea;
  border: 2px solid #667eea;
}

.continue-shopping:hover {
  background: #667eea;
  color: white;
  transform: translateY(-1px);
}

/* Responsive */
@media (max-width: 1024px) {
  .cart-content {
    grid-template-columns: 1fr;
  }
  
  .cart-summary-section {
    position: static;
  }
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: var(--spacing-lg);
    text-align: center;
  }
  
  .cart-item {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .item-details {
    width: 100%;
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-md);
  }
  
  .item-actions {
    width: 100%;
    justify-content: space-between;
  }
  
  .quantity-controls {
    flex: 1;
    justify-content: center;
  }
}

/* Animaciones */
.cart-item {
  animation: fadeInUp 0.6s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Estados de hover mejorados */
.btn:focus,
.cart-item:focus,
.remove-btn:focus {
  outline: 2px solid #667eea;
  outline-offset: 2px;
}

/* Mejoras de accesibilidad */
.quantity-btn:focus {
  outline: 2px solid #667eea;
  outline-offset: 2px;
}

/* Indicadores visuales */
.summary-card {
  position: relative;
}

.summary-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
</style>