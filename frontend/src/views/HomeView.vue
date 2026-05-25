<script setup>
import { onMounted } from 'vue';
import SearchBar from '@/components/SearchBar.vue';
import ResultCard from '@/components/ResultCard.vue';
import { useSearch } from '@/composables/useSearch';
import { useMotorStatus } from '@/composables/useMotorStatus';
import StatusMessage from '@/components/StatusMessage.vue';
import { useAuthStore } from '@/stores/authStore';

const { isReady, loadingIngest, init } = useMotorStatus();

const authStore = useAuthStore();

const { query, respuesta, loading, copiado, canSearch, buscar, copiarAlPortapapeles } =
  useSearch(isReady);

onMounted(async () => {
  await init();
});
</script>

<template>
  <div>
    <StatusMessage :is-ready="isReady" :loadingIngest="loadingIngest" />

    <!-- <h2 class="fw-bold m-0">Hola, {{ authStore.user?.first_name }}</h2> -->

    <SearchBar
      v-model="query"
      :is-ready="isReady"
      :loading="loading"
      :can-search="canSearch"
      @buscar="buscar"
    />

    <ResultCard :respuesta="respuesta" :copiado="copiado" @copiar="copiarAlPortapapeles" />
  </div>
</template>
