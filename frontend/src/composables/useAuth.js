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
   * Proceso de Login en dos pasos:
   * 1. Obtener Access Token.
   * 2. Obtener Perfil de Usuario con el token obtenido.
   */
  const login = async (credentials) => {
    loading.value = true;
    error.value = null;

    try {
      // PASO 1: Autenticación
      const authResponse = await authService.login(credentials.email, credentials.password);

      const token = authResponse.data.access_token || authResponse.data.token;

      if (!token) {
        throw new Error('No se recibió el token de acceso del servidor.');
      }

      authStore.setToken(token);

      // PASO 2: Obtención de perfil (Endpoint /profile/me)
      const profileResponse = await authService.getCurrentUserProfile();
      const userData = profileResponse.data;

      if (!userData) {
        throw new Error('No se pudieron recuperar los datos del perfil.');
      }

      authStore.setUser(userData);

      // PASO 3: Navegación
      await router.push({ path: '/' });

      return { token, user: userData };
    } catch (err) {
      authStore.clearAuth();
      error.value = err.response?.data?.detail || err.message || 'Error en la autenticación';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const logout = () => {
    authStore.clearAuth();
    router.push({ name: 'Login' });
  };

  return {
    loading,
    error,
    login,
    logout,
    user: computed(() => authStore.user),
    isAuthenticated: computed(() => authStore.isAuthenticated),
  };
}
