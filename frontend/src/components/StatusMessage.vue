<script setup>
defineProps({
  isReady: Boolean,
  loadingIngest: Boolean,
});
</script>

<template>
  <div class="row justify-content-center mx-0">
    <div
      v-if="!loadingIngest && !isReady"
      class="col-md-8 alert alert-warning py-3 rounded-4 shadow-sm border-0"
      role="alert"
      aria-live="polite"
      aria-atomic="true"
    >
      <div class="d-flex align-items-center justify-content-center text-center text-md-start gap-3">
        <i
          class="bi bi-database-fill-exclamation fs-3 flex-shrink-0 d-none d-md-block"
          aria-hidden="true"
        ></i>
        <div>
          <div class="fw-bold mb-1">Sistema no indexado</div>
          <p class="mb-0 small">
            Contacta al administrador para iniciar la indexación de documentos.
          </p>
        </div>
      </div>
    </div>
    <div
      v-if="loadingIngest"
      class="col-md-8 alert alert-info py-3 rounded-4 shadow-sm border-0"
      role="status"
      aria-live="polite"
      aria-atomic="true"
    >
      <div class="d-flex align-items-center justify-content-center text-center text-md-start gap-3">
        <div
          class="spinner-border spinner-border-sm flex-shrink-0"
          role="status"
          aria-label="Indexando documentos"
        >
          <span class="visually-hidden">Cargando...</span>
        </div>
        <div>
          <div class="fw-bold mb-1">Indexando documentos</div>
          <p class="mb-0 small">Por favor espera mientras se procesan los archivos...</p>
        </div>
      </div>
    </div>
  </div>
</template>
