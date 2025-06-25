<template>
  <div class="productos">
    <h2>Catálogo de Productos</h2>
    <div v-if="productos.length === 0">
      <p>No hay productos disponibles.</p>
    </div>
    <div class="grid">
      <div v-for="producto in productos" :key="producto.id" class="card">
        <img :src="`http://localhost:8000${producto.imagen}`" alt="Imagen del producto" class="imagen" />
        <h3>{{ producto.nombre }}</h3>
        <p>{{ producto.descripcion }}</p>
        <p><strong>Precio:</strong> Q{{ producto.precio.toFixed(2) }}</p>
        <p><strong>Stock:</strong> {{ producto.stock }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const productos = ref([])
const usuario = ref(null)

onMounted(async () => {
  usuario.value = JSON.parse(localStorage.getItem('usuario'))
  try {
    const response = await axios.get('http://localhost:8000/productos/')
    productos.value = response.data
  } catch (error) {
    console.error('Error al obtener productos:', error)
  }
})

function cerrarSesion() {
  localStorage.removeItem('token')
  localStorage.removeItem('usuario')
  router.push('/')
}
</script>

<style scoped>
.productos {
  padding: 40px;
  color: white;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
  margin-top: 30px;
}

.card {
  background-color: #1e1e1e;
  border-radius: 12px;
  padding: 16px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.3);
}

.imagen {
  max-width: 100%;
  height: 150px;
  object-fit: cover;
  margin-bottom: 10px;
  border-radius: 8px;
}

button {
  background: #333;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}

.perfil-link {
  color: #4caf50;
  text-decoration: underline;
  margin-right: 8px;
}
</style>
