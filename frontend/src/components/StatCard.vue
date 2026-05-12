<script setup>
defineProps({
  title: String,
  value: [String, Number],
  variant: { type: String, default: '' },
});
</script>

<template>
  <div class="col-md-3">
    <div class="card shadow-sm border-0 rounded-4">
      <div class="card-body">
        <h6 class="text-muted">{{ title }}</h6>
        <h3 class="fw-bold" :class="variant">
          {{ value }}
        </h3>
      </div>
    </div>
  </div>
</template>
