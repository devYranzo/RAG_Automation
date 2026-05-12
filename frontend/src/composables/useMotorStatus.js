import { ref, computed } from 'vue';
import indexService from '@/services/index.service';

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
  const data = await indexService.getStatus();

  motorStatus.value = {
    ...motorStatus.value,
    ...data,
  };

  return data;
};

/**
 * INIT (dashboard load)
 */
const init = async () => {
  const data = await fetchStatus();

  if (data.is_indexing) {
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

    if (!data.is_indexing) {
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

  await indexService.startIngest();

  startPolling();
};

/**
 * REINDEXAR
 */
const reindexar = async () => {
  if (loadingIngest.value) return;

  loadingIngest.value = true;

  await indexService.reindex();

  startPolling();
};

/**
 * API pública del composable
 */
export function useMotorStatus() {
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
