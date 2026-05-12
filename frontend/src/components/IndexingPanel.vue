<script setup>
import { useSystemStore } from '@/stores/systemStore';

const systemStore = useSystemStore();
defineProps({
  indexing: Object,
  isIndexed: Boolean,
});
</script>

<template>
  <div class="card shadow-sm border-0 rounded-4">
    <div class="card-body">
      <div class="row d-flex justify-content-between align-items-center mb-4">
        <div class="col-auto">
          <h4 class="fw-bold mb-0">Gestión de Datos</h4>
        </div>

        <div class="col-auto">
          <button
            v-if="!systemStore.isReady && !systemStore.loadingIngest"
            @click="systemStore.encender()"
            class="btn btn-success rounded-pill shadow-sm px-4"
          >
            <i class="bi bi-lightning-charge-fill me-1"></i>Indexar
          </button>

          <button
            v-if="systemStore.isReady && !systemStore.loadingIngest"
            @click="systemStore.reindexar()"
            class="btn btn-warning rounded-pill shadow-sm px-4"
          >
            <i class="bi bi-arrow-clockwise me-1"></i>Reindexar
          </button>

          <button
            v-if="systemStore.loadingIngest"
            class="btn btn-secondary rounded-pill shadow-sm px-4"
            disabled
          >
            <span class="spinner-border spinner-border-sm me-2"></span>Procesando...
          </button>
        </div>
      </div>

      <div class="mb-2 d-flex justify-content-between align-items-end">
        <span class="text-muted small">Progreso de la base de vectores</span>
        <span class="fw-bold">{{ indexing?.progress_percent || 0 }}%</span>
      </div>

      <div class="progress mb-3" style="height: 12px">
        <div
          class="progress-bar bg-primary"
          role="progressbar"
          :style="{ width: (indexing?.progress_percent ?? 0) + '%' }"
        ></div>
      </div>

      <div v-if="indexing?.is_indexing" class="mt-2 text-primary d-flex align-items-center">
        <div class="spinner-grow spinner-grow-sm me-2"></div>
        Indexación en curso...
      </div>
      <div v-else-if="!isIndexed" class="mt-2 text-warning">
        <i class="bi bi-database-fill-exclamation me-2"></i>Sistema sin indexar
      </div>
      <div v-else class="mt-2 text-success">
        <i class="bi bi-check-circle-fill me-2"></i>Motor de búsqueda indexado
      </div>
    </div>
  </div>
</template>
