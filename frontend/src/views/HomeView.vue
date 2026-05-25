<script setup>
import { onMounted } from 'vue';
import SearchBar from '@/components/SearchBar.vue';
import ResultCard from '@/components/ResultCard.vue';
import { useSearch } from '@/composables/useSearch';
import { useMotorStatus } from '@/composables/useMotorStatus';
import StatusMessage from '@/components/StatusMessage.vue';

const { isReady, loadingIngest, init } = useMotorStatus();

const { query, respuesta, loading, copiado, canSearch, buscar, copiarAlPortapapeles } =
  useSearch(isReady);

onMounted(async () => {
  await init();
});
</script>

<template>
  <div>
    <StatusMessage :is-ready="isReady" :loadingIngest="loadingIngest" />

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
