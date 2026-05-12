import { ref } from 'vue';
import { useRouter } from 'vue-router';
import authService from '@/services/auth.service';
import { useAuthStore } from '@/stores/authStore';

export function useAuth() {
  const router = useRouter();
  const authStore = useAuthStore();

  const loading = ref(false);
  const error = ref(null);

  const login = async (credentials) => {
    loading.value = true;
    error.value = null;

    try {
      const response = await authService.login(credentials.email, credentials.password);
      const { access_token, user_data } = response.data;

      authStore.setToken(access_token);
      authStore.setUser(user_data);

      await router.push('/');
      return response.data;
    } catch (err) {
      error.value = err.response?.data?.detail || 'Error al iniciar sesión';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const logout = () => {
    authStore.clearAuth();
    router.push('/login');
  };

  const fetchProfile = async () => {
    if (!authStore.token) return;
    try {
      const response = await authService.getCurrentUserProfile();
      authStore.setUser(response.data);
    } catch (err) {
      console.error(err);
    }
  };

  return {
    loading,
    error,
    login,
    logout,
    fetchProfile,
    user: authStore.user,
    isAuthenticated: authStore.isAuthenticated,
  };
}
