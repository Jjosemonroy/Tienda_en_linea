<template>
  <div class="historial-container">
    <!-- Header -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">Mi Historial de Compras</h1>
        <p class="page-subtitle">Revisa todas tus compras realizadas</p>
      </div>
      <div class="header-actions">
        <div class="stats-summary">
          <span class="total-compras">{{ historial.total_compras }}</span>
          <span class="stats-label">compras realizadas</span>
        </div>
      </div>
    </div>

    <!-- Contenido principal -->
    <div class="historial-content">
      <div v-if="cargando" class="loading-state">
        <div class="loading-spinner"></div>
        <p>Cargando tu historial...</p>
      </div>

      <div v-else-if="!historial.historial || historial.historial.length === 0" class="empty-history">
        <div class="empty-icon">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
        </div>
        <h3>Aún no tienes compras</h3>
        <p>Cuando realices tu primera compra, aparecerá aquí</p>
        <router-link to="/productos" class="btn btn-primary">
          <svg class="btn-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"></path>
          </svg>
          Ver productos
        </router-link>
      </div>

      <div v-else class="compras-list">
        <div v-for="compra in historial.historial" :key="compra.venta_id" class="compra-card">
          <!-- Header de la compra -->
          <div class="compra-header">
            <div class="compra-info">
              <h3>Compra #{{ compra.venta_id }}</h3>
              <p class="compra-fecha">{{ compra.fecha }}</p>
            </div>
            <div class="compra-total">
              <span class="total-label">Total:</span>
              <span class="total-amount">Q{{ compra.total.toFixed(2) }}</span>
            </div>
          </div>

          <!-- Información de pago -->
          <div v-if="compra.transaccion" class="payment-info">
            <div class="payment-details">
              <div class="payment-method">
                <svg class="payment-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H5a3 3 0 00-3 3v8a3 3 0 003 3z"></path>
                </svg>
                <span>{{ compra.transaccion.metodo_pago }}</span>
              </div>
              <div class="payment-status" :class="getStatusClass(compra.transaccion.estado)">
                <span class="status-dot"></span>
                {{ compra.transaccion.estado }}
              </div>
              <div class="payment-reference">
                <span class="reference-label">Ref:</span>
                <span class="reference-code">{{ compra.transaccion.referencia }}</span>
              </div>
            </div>
          </div>

          <!-- Productos de la compra -->
          <div class="productos-section">
            <h4>Productos comprados</h4>
            <div class="productos-list">
              <div v-for="producto in compra.productos" :key="producto.nombre" class="producto-item">
                <div class="producto-image">
                  <img :src="getImageUrl(producto.imagen)" :alt="producto.nombre" />
                </div>
                <div class="producto-details">
                  <h5>{{ producto.nombre }}</h5>
                  <div class="producto-info">
                    <span class="cantidad">{{ producto.cantidad }} x Q{{ producto.precio_unitario.toFixed(2) }}</span>
                    <span class="subtotal">Q{{ producto.subtotal.toFixed(2) }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Acciones -->
          <div class="compra-actions">
            <button class="btn btn-outline btn-sm" @click="toggleDetalles(compra.venta_id)">
              <svg class="btn-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
              </svg>
              {{ compraDetalles[compra.venta_id] ? 'Ocultar detalles' : 'Ver detalles' }}
            </button>
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

// Datos reactivos
const usuario = ref(null)
const historial = ref({ total_compras: 0, historial: [] })
const cargando = ref(true)
const compraDetalles = ref({})

onMounted(async () => {
  usuario.value = JSON.parse(localStorage.getItem('usuario'))
  if (!usuario.value) {
    router.push('/login')
    return
  }
  
  await cargarHistorial()
  cargando.value = false
})

async function cargarHistorial() {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get(`${getApiUrl('purchaseHistory')}/${usuario.value.id}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    historial.value = response.data
  } catch (error) {
    console.error('Error al cargar historial:', error)
    toast.error('Error al cargar el historial de compras')
    historial.value = { total_compras: 0, historial: [] }
  }
}

function toggleDetalles(ventaId) {
  compraDetalles.value[ventaId] = !compraDetalles.value[ventaId]
}

function getStatusClass(estado) {
  switch (estado.toLowerCase()) {
    case 'aprobado':
      return 'status-approved'
    case 'pendiente':
      return 'status-pending'
    case 'rechazado':
      return 'status-rejected'
    default:
      return 'status-default'
  }
}
</script>

<style scoped>
.historial-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: var(--spacing-lg);
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

.stats-summary {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-xs);
  background: rgba(255, 255, 255, 0.2);
  padding: var(--spacing-md);
  border-radius: var(--border-radius);
  backdrop-filter: blur(10px);
}

.total-compras {
  font-size: var(--font-size-2xl);
  font-weight: 700;
  color: white;
}

.stats-label {
  color: rgba(255, 255, 255, 0.8);
  font-size: var(--font-size-sm);
}

.loading-state {
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

.empty-history {
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

.empty-history h3 {
  margin-bottom: var(--spacing-sm);
  color: var(--text-primary);
}

.empty-history p {
  margin-bottom: var(--spacing-xl);
}

.compras-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xl);
}

.compra-card {
  background: white;
  border-radius: var(--border-radius-lg);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
}

.compra-card:hover {
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.compra-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-lg);
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  border-bottom: 1px solid #e2e8f0;
}

.compra-info h3 {
  margin: 0 0 var(--spacing-xs) 0;
  color: #2d3748;
  font-weight: 600;
}

.compra-fecha {
  margin: 0;
  color: #4a5568;
  font-size: var(--font-size-sm);
}

.compra-total {
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
  font-size: var(--font-size-xl);
  font-weight: 700;
  color: #667eea;
}

.payment-info {
  padding: var(--spacing-lg);
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
}

.payment-details {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: var(--spacing-md);
}

.payment-method {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  color: #4a5568;
}

.payment-icon {
  width: 20px;
  height: 20px;
}

.payment-status {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--border-radius);
  font-size: var(--font-size-sm);
  font-weight: 500;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.status-approved {
  background: #f0fff4;
  color: #2f855a;
  border: 1px solid #9ae6b4;
}

.status-approved .status-dot {
  background: #38a169;
}

.status-pending {
  background: #fef5e7;
  color: #c05621;
  border: 1px solid #f6e05e;
}

.status-pending .status-dot {
  background: #ed8936;
}

.status-rejected {
  background: #fed7d7;
  color: #c53030;
  border: 1px solid #feb2b2;
}

.status-rejected .status-dot {
  background: #e53e3e;
}

.payment-reference {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  color: #4a5568;
  font-size: var(--font-size-sm);
}

.reference-label {
  font-weight: 500;
}

.reference-code {
  font-family: monospace;
  background: #e2e8f0;
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--border-radius);
}

.productos-section {
  padding: var(--spacing-lg);
}

.productos-section h4 {
  margin: 0 0 var(--spacing-lg) 0;
  color: #2d3748;
  font-weight: 600;
}

.productos-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.producto-item {
  display: flex;
  gap: var(--spacing-md);
  padding: var(--spacing-md);
  background: #f8fafc;
  border-radius: var(--border-radius);
  border: 1px solid #e2e8f0;
}

.producto-image {
  flex-shrink: 0;
  width: 60px;
  height: 60px;
  border-radius: var(--border-radius);
  overflow: hidden;
}

.producto-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.producto-details {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.producto-details h5 {
  margin: 0 0 var(--spacing-xs) 0;
  color: #2d3748;
  font-weight: 500;
}

.producto-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.cantidad {
  color: #4a5568;
  font-size: var(--font-size-sm);
}

.subtotal {
  font-weight: 600;
  color: #667eea;
}

.compra-actions {
  padding: var(--spacing-lg);
  border-top: 1px solid #e2e8f0;
  background: #f8fafc;
  display: flex;
  justify-content: center;
}

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

.btn-sm {
  padding: var(--spacing-sm) var(--spacing-md);
  font-size: var(--font-size-sm);
}

.btn-icon {
  width: 18px;
  height: 18px;
}

/* Responsive */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: var(--spacing-lg);
    text-align: center;
  }
  
  .compra-header {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-md);
  }
  
  .compra-total {
    align-items: flex-start;
  }
  
  .payment-details {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .producto-info {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-xs);
  }
}

/* Animaciones */
.compra-card {
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
</style>