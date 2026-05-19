import { ref, computed } from 'vue';
import indexService from '@/services/index.service';

export function useMotorStatus() {
  const motorStatus = ref({
    is_indexing: false,
    has_data: false,
    processed: 0,
    total: 0,
    progress_percent: 0,
  });

  const loadingIngest = ref(false);
  let statusInterval = null;
  let isPolling = false;

  const isReady = computed(() => {
    return !motorStatus.value.is_indexing && motorStatus.value.has_data;
  });

  /**
   * PETICIÓN BASE
   */
  const fetchStatus = async () => {
    try {
      const data = await indexService.getStatus();
      motorStatus.value = {
        ...motorStatus.value,
        ...data,
      };
      return data;
    } catch (error) {
      console.error('Error al traer el estado del motor:', error);
      return motorStatus.value;
    }
  };

  /**
   * INIT (dashboard load)
   */
  const init = async () => {
    const data = await fetchStatus();
    if (data && data.is_indexing) {
      startPolling();
    }
  };

  /**
   * START POLLING
   */
  const startPolling = () => {
    if (isPolling) return;
    isPolling = true;

    statusInterval = setInterval(async () => {
      const data = await fetchStatus();
      if (!data || !data.is_indexing) {
        stopPolling();
        loadingIngest.value = false;
      }
    }, 2500);
  };

  /**
   * STOP POLLING
   */
  const stopPolling = () => {
    if (statusInterval) {
      clearInterval(statusInterval);
      statusInterval = null;
    }
    isPolling = false;
  };

  /**
   * INICIAR INDEXACIÓN
   */
  const encenderMotor = async () => {
    if (loadingIngest.value) return;
    loadingIngest.value = true;
    try {
      await indexService.startIngest();
      startPolling();
    } catch (error) {
      loadingIngest.value = false;
    }
  };

  /**
   * REINDEXAR
   */
  const reindexar = async () => {
    if (loadingIngest.value) return;
    loadingIngest.value = true;
    try {
      await indexService.reindex();
      startPolling();
    } catch (error) {
      loadingIngest.value = false;
    }
  };

  return {
    motorStatus,
    loadingIngest,
    isReady,
    init,
    encenderMotor,
    reindexar,
    fetchStatus,
  };
}
