import { useAuthStore } from '@/stores/authStore';
import axios from 'axios';
import router from '@/router';

const BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: BASE_URL,
  headers: { 'Content-Type': 'application/json' },
  withCredentials: true,
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (!error.response) {
      router.push({ name: 'Error', params: { code: '500' } });
      return Promise.reject(error);
    }

    const { status } = error.response;
    const authStore = useAuthStore();

    switch (status) {
      case 401:
        authStore.clearAuth();
        if (router.currentRoute.value.path !== '/login') {
          router.push('/login?message=session_expired');
        }
        break;

      case 403:
        router.push({ name: 'Error', params: { code: '403' } });
        break;

      case 404:
        if (error.config.method === 'get') {
          router.push({ name: 'Error', params: { code: '404' } });
        }
        break;

      case 500:
        router.push({ name: 'Error', params: { code: '500' } });
        break;

      default:
        break;
    }

    return Promise.reject(error);
  }
);

export default api;
