<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import StatCard from '@/components/StatCard.vue';
import IndexingPanel from '@/components/IndexingPanel.vue';
import { useAuthStore } from '@/stores/authStore';
import systemService from '@/services/system.service';

const stats = ref(null);
const error = ref(null);

const authStore = useAuthStore();

const loadStats = async () => {
  try {
    stats.value = await systemService.getStats();
  } catch (err) {
    console.error('Error cargando stats:', err);
  }
};

onMounted(() => {
  loadStats();
});
</script>

<template>
  <div class="container-fluid py-4">
    <div v-if="error" class="alert alert-danger border-0 rounded-4 shadow-sm mb-4">
      <i class="bi bi-exclamation-triangle-fill me-2"></i>{{ error }}
    </div>

    <div class="row mb-3">
      <h2 class="fw-bold">Hola, {{ authStore.fullName }}</h2>
    </div>

    <!-- Sección de Stats -->
    <div v-if="stats" class="row g-3">
      <StatCard
        title="Estado"
        :value="stats.is_indexed ? 'Activo' : 'No indexado'"
        :variant="stats.is_indexed ? 'text-success' : 'text-warning'"
      />
      <StatCard title="Vectores" :value="stats.vectors_count" />
      <StatCard title="CVs procesados" :value="`${stats.documents_count} / ${stats.total_pdfs}`" />
      <StatCard title="Caché" :value="stats.cache_size" />
    </div>

    <!-- Sección de Control -->
    <div v-if="stats" class="mt-4">
      <IndexingPanel :indexing="stats.indexing" :is-indexed="stats.is_indexed" />
    </div>
  </div>
</template>
