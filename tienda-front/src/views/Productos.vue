<template>
  <div class="productos-container">
    <v-card class="page-header mb-6" elevation="4" rounded="xl">
      <v-card-text class="pa-6">
        <v-row align="center" justify="space-between">
          <v-col cols="12" md="8">
            <h1 class="text-h3 font-weight-bold text-primary mb-2">
              Catálogo de Productos
            </h1>
            <p class="text-body-1 text-medium-emphasis">
              Descubre nuestra colección de productos de calidad
            </p>
          </v-col>
          <v-col cols="12" md="4">
            <v-text-field
              v-model="busqueda"
              placeholder="Buscar productos..."
              prepend-inner-icon="mdi-magnify"
              variant="outlined"
              rounded="lg"
              density="comfortable"
              hide-details
            ></v-text-field>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <v-card class="filters-section mb-6" elevation="2" rounded="lg">
      <v-card-text class="pa-6">
        <v-row>
          <v-col cols="12" sm="6" md="3">
            <v-select
              v-model="categoriaFiltro"
              label="Categoría"
              :items="categorias"
              item-title="nombre"
              item-value="id"
              variant="outlined"
              rounded="lg"
              density="comfortable"
              hide-details
              clearable
              placeholder="Todas las categorías"
            ></v-select>
          </v-col>
          
          <v-col cols="12" sm="6" md="3">
            <v-select
              v-model="ordenamiento"
              label="Ordenar por"
              :items="[
                { title: 'Nombre', value: 'nombre' },
                { title: 'Precio: menor a mayor', value: 'precio-asc' },
                { title: 'Precio: mayor a menor', value: 'precio-desc' },
                { title: 'Stock disponible', value: 'stock' }
              ]"
              variant="outlined"
              rounded="lg"
              density="comfortable"
              hide-details
            ></v-select>
          </v-col>
          
          <v-col cols="12" sm="6" md="3">
            <v-text-field
              v-model.number="precioMin"
              label="Precio mínimo"
              type="number"
              placeholder="Mín"
              variant="outlined"
              rounded="lg"
              density="comfortable"
              hide-details
              prepend-inner-icon="mdi-currency-usd"
            ></v-text-field>
          </v-col>
          
          <v-col cols="12" sm="6" md="3">
            <v-text-field
              v-model.number="precioMax"
              label="Precio máximo"
              type="number"
              placeholder="Máx"
              variant="outlined"
              rounded="lg"
              density="comfortable"
              hide-details
              prepend-inner-icon="mdi-currency-usd"
            ></v-text-field>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <v-card class="results-section" elevation="2" rounded="lg">
      <v-card-text class="pa-6">
        <v-row align="center" justify="space-between" class="mb-6">
          <div class="d-flex align-center">
            <v-chip
              color="primary"
              size="large"
              class="mr-3"
            >
              {{ productosFiltrados.length }}
            </v-chip>
            <span class="text-body-1 text-medium-emphasis">
              productos encontrados
            </span>
          </div>
          
          <v-btn-toggle
            v-model="viewMode"
            mandatory
            rounded="lg"
            color="primary"
          >
            <v-btn value="grid" icon="mdi-view-grid"></v-btn>
            <v-btn value="list" icon="mdi-view-list"></v-btn>
          </v-btn-toggle>
        </v-row>

        <v-alert
          v-if="mensaje"
          :type="mensajeTipo"
          variant="tonal"
          class="mb-6"
          :text="mensaje"
          closable
          @click:close="mensaje = ''"
        ></v-alert>

        <v-row v-if="productosFiltrados.length === 0" justify="center" class="py-12">
          <v-col cols="12" sm="8" md="6" class="text-center">
            <v-icon
              size="80"
              color="grey-lighten-1"
              class="mb-4"
            >
              mdi-package-variant-off
            </v-icon>
            <h3 class="text-h5 text-medium-emphasis mb-2">
              No se encontraron productos
            </h3>
            <p class="text-body-2 text-medium-emphasis">
              Intenta ajustar los filtros de búsqueda
            </p>
          </v-col>
        </v-row>

        <v-row v-else-if="viewMode === 'grid'" class="productos-grid">
          <v-col
            v-for="producto in productosFiltrados"
            :key="producto.id"
            cols="12"
            sm="6"
            md="4"
            lg="3"
          >
            <v-card
              class="producto-card h-100"
              elevation="2"
              rounded="lg"
              hover
              @click="verProducto(producto)"
            >
              <v-img
                :src="getSimpleImageUrl(producto.imagen) || '/src/assets/placeholder.svg'"
                height="200"
                cover
                class="producto-imagen"
              >
                <template v-slot:placeholder>
                  <v-row align="center" justify="center" class="fill-height">
                    <v-icon size="60" color="grey-lighten-2">mdi-image</v-icon>
                  </v-row>
                </template>
              </v-img>
              
              <v-card-text class="pa-4">
                <h3 class="text-h6 font-weight-bold mb-2 text-truncate">
                  {{ producto.nombre }}
                </h3>
                <p class="text-body-2 text-medium-emphasis mb-3 text-truncate-2">
                  {{ producto.descripcion }}
                </p>
                <div class="d-flex align-center justify-space-between mb-3">
                  <span class="text-h6 font-weight-bold text-primary">
                    ${{ producto.precio }}
                  </span>
                  <v-chip
                    :color="producto.stock > 0 ? 'success' : 'error'"
                    size="small"
                    variant="tonal"
                  >
                    {{ producto.stock > 0 ? 'En stock' : 'Sin stock' }}
                  </v-chip>
                </div>
              </v-card-text>
              
              <v-card-actions class="pa-4 pt-0">
                <v-btn
                  color="primary"
                  variant="outlined"
                  block
                  rounded="lg"
                  :disabled="producto.stock === 0"
                  @click.stop="agregarAlCarrito(producto)"
                >
                  <v-icon start>mdi-cart-plus</v-icon>
                  Agregar al carrito
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>

        <v-list v-else class="productos-lista">
          <v-list-item
            v-for="producto in productosFiltrados"
            :key="producto.id"
            class="mb-4"
            rounded="lg"
            elevation="2"
            hover
            @click="verProducto(producto)"
          >
            <template v-slot:prepend>
              <v-avatar size="80" rounded="lg">
                <v-img
                  :src="getSimpleImageUrl(producto.imagen) || '/src/assets/placeholder.svg'"
                  cover
                ></v-img>
              </v-avatar>
            </template>
            
            <v-list-item-title class="text-h6 font-weight-bold mb-1">
              {{ producto.nombre }}
            </v-list-item-title>
            <v-list-item-subtitle class="text-body-2 mb-2">
              {{ producto.descripcion }}
            </v-list-item-subtitle>
            
            <template v-slot:append>
              <div class="d-flex flex-column align-end">
                <span class="text-h6 font-weight-bold text-primary mb-2">
                  ${{ producto.precio }}
                </span>
                <v-chip
                  :color="producto.stock > 0 ? 'success' : 'error'"
                  size="small"
                  variant="tonal"
                  class="mb-2"
                >
                  {{ producto.stock > 0 ? 'En stock' : 'Sin stock' }}
                </v-chip>
                <v-btn
                  color="primary"
                  variant="outlined"
                  size="small"
                  rounded="lg"
                  :disabled="producto.stock === 0"
                  @click.stop="agregarAlCarrito(producto)"
                >
                  <v-icon start>mdi-cart-plus</v-icon>
                  Agregar
                </v-btn>
              </div>
            </template>
          </v-list-item>
        </v-list>
      </v-card-text>
    </v-card>

    <v-row v-if="totalPaginas > 1" justify="center" class="mt-6">
      <v-pagination
        v-model="paginaActual"
        :length="totalPaginas"
        :total-visible="7"
        rounded="lg"
        color="primary"
      ></v-pagination>
    </v-row>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
import { getApiUrl, getSimpleImageUrl } from '../config/api.js'

const router = useRouter()
const toast = useToast()
const productos = ref([])
const categorias = ref([])
const usuario = ref(null)
const viewMode = ref('grid')

// Variables para filtros
const busqueda = ref('')
const categoriaFiltro = ref('')
const ordenamiento = ref('nombre')
const precioMin = ref('')
const precioMax = ref('')

// Variables para mensajes y paginación
const mensaje = ref('')
const mensajeTipo = ref('info')
const paginaActual = ref(1)
const totalPaginas = ref(1)

onMounted(async () => {
  usuario.value = JSON.parse(localStorage.getItem('usuario'))
  
  try {
    const [productosResponse, categoriasResponse] = await Promise.all([
      axios.get(getApiUrl('products')),
      axios.get(getApiUrl('categories'))
    ])
    
    productos.value = productosResponse.data
    categorias.value = categoriasResponse.data
    
    // Limpiar datos de imagen inválidos
    productos.value = productos.value.map(producto => {
      if (producto.imagen) {
        const invalidValues = ['no hay', 'sin imagen', 'null', 'undefined', 'none', '']
        if (invalidValues.includes(producto.imagen.toLowerCase().trim())) {
          producto.imagen = null
        }
      }
      return producto
    })
  } catch (error) {
    console.error('Error al cargar datos:', error)
    toast.error('Error al cargar los productos')
  }
})

// Computed properties para filtros
const productosFiltrados = computed(() => {
  let filtrados = [...productos.value]
  
  if (busqueda.value) {
    const searchTerm = busqueda.value.toLowerCase()
    filtrados = filtrados.filter(producto =>
      producto.nombre.toLowerCase().includes(searchTerm) ||
      producto.descripcion.toLowerCase().includes(searchTerm)
    )
  }
  
  if (categoriaFiltro.value) {
    filtrados = filtrados.filter(producto => producto.categoria?.id === categoriaFiltro.value)
  }
  
  if (precioMin.value) {
    filtrados = filtrados.filter(producto => producto.precio >= precioMin.value)
  }
  if (precioMax.value) {
    filtrados = filtrados.filter(producto => producto.precio <= precioMax.value)
  }
  
  switch (ordenamiento.value) {
    case 'precio-asc':
      filtrados.sort((a, b) => a.precio - b.precio)
      break
    case 'precio-desc':
      filtrados.sort((a, b) => b.precio - a.precio)
      break
    case 'stock':
      filtrados.sort((a, b) => b.stock - a.stock)
      break
    default:
      filtrados.sort((a, b) => a.nombre.localeCompare(b.nombre))
  }
  
  return filtrados
})

async function agregarAlCarrito(producto) {
  if (!usuario.value) {
    router.push('/login')
    return
  }
  
  try {
    const token = localStorage.getItem('token')
    await axios.post(getApiUrl('addToCart'), {
      usuario_id: usuario.value.id,
      producto_id: producto.id,
      cantidad: 1
    }, {
      headers: { Authorization: `Bearer ${token}` }
    })
    
    toast.success(`${producto.nombre} agregado al carrito`)
  } catch (error) {
    console.error('Error al agregar al carrito:', error)
    toast.error('Error al agregar al carrito')
  }
}

function verProducto(producto) {
  // Implementar modal o navegación a vista de detalle
}
</script>

<style scoped>
.producto-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
}

.producto-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.producto-imagen {
  transition: transform 0.3s ease;
  border-radius: 8px 8px 0 0;
}

.producto-card:hover .producto-imagen {
  transform: scale(1.05);
}

.text-truncate-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.v-img {
  background-color: #f8fafc;
}

.v-img img {
  object-fit: cover;
}

.v-avatar .v-img {
  border: 2px solid #e5e7eb;
  transition: border-color 0.3s ease;
}

.v-avatar:hover .v-img {
  border-color: #3b82f6;
}


</style>
