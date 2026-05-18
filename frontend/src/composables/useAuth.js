import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import authService from '@/services/auth.service';
import { useAuthStore } from '@/stores/authStore';

export function useAuth() {
  const router = useRouter();
  const authStore = useAuthStore();

  const loading = ref(false);
  const error = ref(null);

  /**
   * Login
   */
  const login = async (credentials) => {
    loading.value = true;
    error.value = null;

    try {
      await authService.login(credentials.email, credentials.password);

      const profileResponse = await authService.getCurrentUserProfile();
      const userData = profileResponse.data;

      if (!userData) {
        throw new Error('No se pudieron recuperar los datos del perfil.');
      }

      authStore.setUser(userData);

      await router.push({ path: '/' });

      return { user: userData };
    } catch (err) {
      authStore.clearAuth();
      error.value = err.response?.data?.detail || err.message || 'Error en la autenticación';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const register = async (formData) => {
    loading.value = true;
    errorMessage.value = '';

    try {
      await authService.register(formData);

      router.push({ name: 'Login', query: { registered: 'success' } });
    } catch (error) {
      errorMessage.value =
        error.response?.data?.detail || 'Something went wrong during registration.';
    } finally {
      loading.value = false;
    }
  };

  /**
   * Logout:
   */
  const logout = async () => {
    try {
      await authService.logout();
    } catch (err) {
      console.error('Error al cerrar sesión en servidor:', err);
    } finally {
      authStore.clearAuth();
      router.push({ name: 'Login' });
    }
  };

  /**
   * Sincronización inicial:
   */
  const fetchProfile = async () => {
    try {
      const response = await authService.getCurrentUserProfile();
      authStore.setUser(response.data);
      return response.data;
    } catch (err) {
      authStore.clearAuth();
      return null;
    }
  };

  return {
    loading,
    error,
    login,
    register,
    logout,
    fetchProfile,
    user: computed(() => authStore.user),
    isAuthenticated: computed(() => authStore.isAuthenticated),
  };
}
