<script setup>
import { onMounted, ref } from 'vue';

defineProps({
  modelValue: String,
  isReady: Boolean,
  loading: Boolean,
  canSearch: Boolean,
});

const emit = defineEmits(['update:modelValue', 'buscar']);

const placeholder = ref('');

const placeholders = [
  'Ej: Ingeniero de software con 5 años de experiencia...',
  'Ej: Diseñadora UX con enfoque en producto...',
  'Ej: Persona con liderazgo en equipos de ventas...',
  'Ej: Especialista en marketing digital y SEO...',
  'Ej: Desarrollador junior con conocimientos en Vue...',
  'Ej: Project manager en proyectos ágiles...',
  'Ej: Experiencia en atención al cliente y soporte...',
  'Ej: Perfil orientado a análisis de datos...',
  'Ej: Reclutador con experiencia en IT...',
  'Ej: Profesional con habilidades en comunicación y ventas...',
];

function changePlaceholder() {
  const randomIndex = Math.floor(Math.random() * placeholders.length);
  placeholder.value = placeholders[randomIndex];
}

onMounted(() => {
  changePlaceholder();
});
</script>

<template>
  <div class="row justify-content-center mb-5">
    <div class="col-lg-8">
      <div
        :class="[
          'search-container shadow rounded-pill p-1 bg-light border border-light',
          isReady ? 'd-flex' : 'd-none',
        ]"
      >
        <div class="input-group input-group-lg">
          <span class="input-group-text bg-transparent border-0 ps-4">
            <i class="bi bi-search text-primary opacity-50" aria-hidden="true"></i>
          </span>
          <input
            :value="modelValue"
            @input="$emit('update:modelValue', $event.target.value)"
            @keyup.enter="$emit('buscar')"
            type="text"
            class="form-control border-0 rounded-pill shadow-none ps-2"
            :placeholder="isReady ? placeholder : 'Active el motor para buscar...'"
            :disabled="!isReady || loading"
            aria-label="Buscar talento por habilidades"
          />
          <button
            @click="$emit('buscar')"
            class="btn btn-primary rounded-pill px-4 mx-1 fw-bold my-1 shadow"
            :disabled="!canSearch"
          >
            <span
              v-if="loading"
              class="spinner-border spinner-border-sm me-2"
              role="status"
              aria-hidden="true"
            ></span>
            {{ loading ? 'Analizando...' : 'Buscar' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.search-container {
  display: flex;
  transition: transform 0.2s;
}

.search-container:focus-within {
  transform: scale(1.02);
}
</style>
