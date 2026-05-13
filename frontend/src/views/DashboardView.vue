<script setup>
import { ref, onMounted, watch, shallowRef } from 'vue';
import { useAuthStore } from '@/stores/authStore';
import systemService from '@/services/system.service';
import { useMotorStatus } from '@/composables/useMotorStatus';

// Importar los componentes de las pestañas
import TabGeneral from '@/components/tabs/TabGeneral.vue';
import TabUsuarios from '@/components/tabs/TabUsuarios.vue';

const authStore = useAuthStore();
const stats = ref(null);
const activeTab = ref('general');

const { motorStatus, isReady, loadingIngest, encenderMotor, reindexar, init } = useMotorStatus();

const tabs = {
  general: TabGeneral,
  usuarios: TabUsuarios,
};

const loadStats = async () => {
  stats.value = await systemService.getStats();
};

watch(
  motorStatus,
  async () => {
    if (!motorStatus.value.is_indexing) await loadStats();
  },
  { deep: true }
);

onMounted(async () => {
  await loadStats();
  await init();
});
</script>

<template>
  <div class="container-fluid py-4">
    <div class="row mb-4">
      <div class="col">
        <h2 class="fw-bold m-0">Hola, {{ authStore.user?.first_name }}</h2>
        <p class="text-muted small">Panel de administración de Talent Finder</p>
      </div>
    </div>

    <ul class="nav nav-pills mb-4 p-1 bg-light rounded-4 d-inline-flex">
      <li class="nav-item">
        <button
          @click="activeTab = 'general'"
          :class="[
            'nav-link px-4',
            activeTab === 'general' ? 'active  rounded-4' : 'text-secondary',
          ]"
        >
          General
        </button>
      </li>
      <li class="nav-item">
        <button
          @click="activeTab = 'usuarios'"
          :class="[
            'nav-link px-4',
            activeTab === 'usuarios' ? 'active rounded-4' : 'text-secondary',
          ]"
        >
          Usuarios
        </button>
      </li>
    </ul>

    <keep-alive>
      <component
        :is="tabs[activeTab]"
        :stats="stats"
        :motor-status="motorStatus"
        :is-ready="isReady"
        :loading-ingest="loadingIngest"
        :encender-motor="encenderMotor"
        :reindexar="reindexar"
      />
    </keep-alive>
  </div>
</template>

<style scoped></style>
