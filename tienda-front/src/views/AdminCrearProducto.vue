<template>
  <div class="crear-producto">
    <h2>Crear nuevo producto</h2>
    <form @submit.prevent="crearProducto" enctype="multipart/form-data">
      <input v-model="nombre" type="text" placeholder="Nombre" required />
      <textarea v-model="descripcion" placeholder="Descripción" required></textarea>
      <input v-model.number="precio" type="number" step="0.01" placeholder="Precio" required />
      <input v-model.number="stock" type="number" placeholder="Stock" required />
      <input type="file" @change="handleFileChange" accept="image/*" required />

      <button type="submit">Guardar producto</button>
    </form>

    <p v-if="mensaje" class="mensaje">{{ mensaje }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const nombre = ref('')
const descripcion = ref('')
const precio = ref(0)
const stock = ref(0)
const imagen = ref(null)
const mensaje = ref('')

const handleFileChange = (event) => {
  imagen.value = event.target.files[0]
}

const crearProducto = async () => {
  mensaje.value = ''
  try {
    const usuario = JSON.parse(localStorage.getItem('usuario'))

    const formData = new FormData()
    formData.append('admin_id', usuario.id)
    formData.append('nombre', nombre.value)
    formData.append('descripcion', descripcion.value)
    formData.append('precio', precio.value)
    formData.append('stock', stock.value)
    formData.append('imagen', imagen.value)

    const res = await axios.post('http://localhost:8000/productos/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })

    mensaje.value = 'Producto creado exitosamente.'
    limpiarFormulario()
  } catch (error) {
    mensaje.value = error.response?.data?.detail || 'Error al crear producto.'
  }
}

const limpiarFormulario = () => {
  nombre.value = ''
  descripcion.value = ''
  precio.value = 0
  stock.value = 0
  imagen.value = null
}
</script>

<style scoped>
.crear-producto {
  max-width: 500px;
  margin: 40px auto;
  padding: 30px;
  background-color: #1e1e1e;
  color: white;
  border-radius: 12px;
}
input,
textarea {
  width: 100%;
  margin: 10px 0;
  padding: 12px;
  font-size: 1rem;
  border-radius: 4px;
  border: none;
}
button {
  margin-top: 10px;
  padding: 12px;
  font-size: 1rem;
  background-color: #333;
  color: white;
  border: none;
  cursor: pointer;
}
.mensaje {
  margin-top: 10px;
  color: lightgreen;
}
</style>
