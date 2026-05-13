<template>
  <div v-if="stats">
    <div class="row g-3">
      <StatCard
        title="Estado"
        :value="stats.is_indexed ? 'Activo' : 'Inactivo'"
        :variant="stats.is_indexed ? 'text-success' : 'text-warning'"
      />
      <StatCard title="Vectores" :value="stats.vectors_count" />
      <StatCard title="CVs indexados" :value="`${stats.documents_count} / ${stats.total_pdfs}`" />
      <StatCard title="Búsquedas" :value="stats.cache_size" />
    </div>

    <div class="mt-4">
      <IndexingPanel
        :motor-status="motorStatus"
        :is-ready="isReady"
        :loading-ingest="loadingIngest"
        :encender-motor="encenderMotor"
        :reindexar="reindexar"
      />
    </div>
  </div>
</template>
<script setup>
defineProps(['stats', 'motorStatus', 'isReady', 'loadingIngest', 'encenderMotor', 'reindexar']);
import StatCard from '@/components/StatCard.vue';
import IndexingPanel from '@/components/IndexingPanel.vue';
</script>
