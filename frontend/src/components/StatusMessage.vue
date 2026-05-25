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
      class="col-md-8 alert alert-warning py-2 rounded-4 shadow-sm border-0"
      role="alert"
    >
      <div class="d-flex align-items-center justify-content-center text-center text-md-start">
        <i
          class="bi bi-database-fill-exclamation fs-3 me-3 d-none d-md-block"
          aria-hidden="true"
        ></i>
        <div>
          <div class="fw-bold">Acción requerida: El sistema no está indexado</div>
        </div>
      </div>
    </div>
  </div>
</template>
