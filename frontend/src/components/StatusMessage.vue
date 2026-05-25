<script setup>
defineProps({
  isReady: Boolean,
  loadingIngest: Boolean,
});
</script>

<template>
  <div class="row justify-content-center mx-0">
    <div
      v-if="isReady"
      class="col-md-6 alert alert-success py-2 rounded-pill shadow-sm border-0 text-center"
      role="status"
    >
      <i class="bi bi-check-circle-fill me-2" aria-hidden="true"></i>
      Motor RAG <strong>Activo</strong> - Base de datos sincronizada
    </div>

    <div
      v-else-if="!loadingIngest"
      class="col-md-8 alert alert-warning py-2 rounded-4 shadow-sm border-0"
      role="alert"
    >
      <div class="d-flex align-items-center justify-content-center text-center text-md-start">
        <i class="bi bi-database-fill-exclamation fs-3 me-3 d-none d-md-block" aria-hidden="true"></i>
        <div>
          <div class="fw-bold">Acción requerida: El sistema no tiene datos indexados</div>
        </div>
      </div>
    </div>
  </div>
</template>
