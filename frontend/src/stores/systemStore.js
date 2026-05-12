import { defineStore } from 'pinia';
import { ref } from 'vue';
import { useMotorStatus } from '@/composables/useMotorStatus';

export const useSystemStore = defineStore('system', () => {
  const loadingIngest = ref(false);

  const { isReady, encenderMotor, reindexar: ejecutarReindexar } = useMotorStatus();

  async function handleEncender() {
    loadingIngest.value = true;
    try {
      await encenderMotor();
    } finally {
      loadingIngest.value = false;
    }
  }

  async function handleReindexar() {
    loadingIngest.value = true;
    try {
      await ejecutarReindexar();
    } finally {
      loadingIngest.value = false;
    }
  }

  return {
    loadingIngest,
    isReady,
    encender: handleEncender,
    reindexar: handleReindexar,
  };
});
