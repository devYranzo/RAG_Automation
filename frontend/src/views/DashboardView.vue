<script setup>
import { ref, onMounted, watch, shallowRef } from 'vue';
import { useAuthStore } from '@/stores/authStore';
import systemService from '@/services/system.service';
import { useMotorStatus } from '@/composables/useMotorStatus';

// Importar los componentes de las pestañas
import TabGeneral from '@/components/tabs/TabGeneral.vue';
import TabUsuarios from '@/components/tabs/TabUsuarios.vue';
import TabAnalytics from '@/components/tabs/TabAnalytics.vue';

const authStore = useAuthStore();
const stats = ref(null);
const activeTab = ref('general');

const { motorStatus, isReady, loadingIngest, encenderMotor, reindexar, init } = useMotorStatus();

const tabs = {
  general: TabGeneral,
  usuarios: TabUsuarios,
  analytics: TabAnalytics,
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
      <div class="col d-flex">
        <h3 class="fw-bold mb-1">Dashboard</h3>
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
          @click="activeTab = 'analytics'"
          :class="[
            'nav-link px-4',
            activeTab === 'analytics' ? 'active rounded-4' : 'text-secondary',
          ]"
        >
          Analytics
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
