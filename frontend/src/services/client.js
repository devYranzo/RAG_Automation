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
    if (error.response && error.response.status === 401) {
      const authStore = useAuthStore();

      authStore.clearAuth();

      if (router.currentRoute.value.path !== '/login') {
        router.push('/login?message=session_expired');
      }
    }
    return Promise.reject(error);
  }
);

export default api;
