<template>
  <Sidebar />
  <div class="contenido-principal">
    <router-view />
  </div>
</template>

<script setup>
import Sidebar from './components/Sidebar.vue'
</script>

<style scoped>
.contenido-principal {
  margin-left: 200px;
  padding: 0 24px;
}
</style>
