import { useAuthStore } from '@/stores/authStore';
import axios from 'axios';

const BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: BASE_URL,
  headers: { 'Content-Type': 'application/json' },
});

// Use token on request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

// Token expiration
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
