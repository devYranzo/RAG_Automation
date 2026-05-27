<script setup>
defineProps({
  motorStatus: Object,
  isReady: Boolean,
  loadingIngest: Boolean,
  encenderMotor: Function,
  reindexar: Function,
});
</script>

<template>
  <div class="card shadow-sm border-0 rounded-4">
    <div class="card-body">
      <!-- HEADER -->
      <div class="row d-flex justify-content-between align-items-center mb-4">
        <div class="col-auto">
          <h2 class="fw-bold mb-0 fs-5">Gestión de Datos</h2>
        </div>

        <div class="col-auto">
          <!-- INDEXAR -->
          <button
            v-if="!isReady && !loadingIngest"
            @click="encenderMotor"
            class="btn btn-success rounded-pill px-4"
            aria-label="Iniciar indexación del sistema"
          >
            <i class="bi bi-lightning-charge-fill me-1" aria-hidden="true"></i>
            Indexar
          </button>

          <!-- REINDEXAR -->
          <button
            v-if="isReady && !loadingIngest"
            @click="reindexar"
            class="btn btn-warning rounded-pill px-4"
            aria-label="Reindexar todos los documentos"
          >
            <i class="bi bi-arrow-clockwise me-1" aria-hidden="true"></i>
            Reindexar
          </button>

          <!-- PROCESANDO -->
          <button
            v-if="loadingIngest"
            class="btn btn-secondary rounded-pill px-4"
            disabled
            :aria-busy="true"
          >
            <span
              class="spinner-border spinner-border-sm me-2"
              role="status"
              aria-hidden="true"
            ></span>
            Procesando...
          </button>
        </div>
      </div>

      <!-- PROGRESO -->
      <div class="mb-2 d-flex justify-content-between">
        <span class="text-muted small">Progreso de indexación</span>
        <span class="fw-bold" aria-live="polite" aria-atomic="true">
          {{ motorStatus.progress_percent || 0 }}%
        </span>
      </div>

      <div
        class="progress mb-3"
        style="height: 12px"
        role="progressbar"
        :aria-valuenow="motorStatus.progress_percent || 0"
        aria-valuemin="0"
        aria-valuemax="100"
        :aria-label="`Progreso: ${motorStatus.progress_percent || 0}%`"
      >
        <div
          class="progress-bar"
          :style="{ width: (motorStatus.progress_percent ?? 0) + '%' }"
        ></div>
      </div>

      <!-- ESTADO -->
      <div
        v-if="motorStatus.is_indexing && !isReady"
        class="text-primary d-flex align-items-center"
        role="status"
        aria-live="polite"
        aria-atomic="true"
      >
        <div class="spinner-grow spinner-grow-sm me-2" aria-hidden="true"></div>
        Indexación en curso...
      </div>

      <div v-else-if="!isReady && !motorStatus.is_indexing" class="text-warning" role="status">
        <i class="bi bi-database-fill-exclamation me-2" aria-hidden="true"></i>
        Sistema sin indexar
      </div>

      <div v-else class="text-success" role="status">
        <i class="bi bi-check-circle-fill me-2" aria-hidden="true"></i>
        Sistema indexado
      </div>
    </div>
  </div>
</template>
