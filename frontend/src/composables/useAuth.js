import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import authService from '@/services/auth.service';

const user = ref(null);
const token = ref(localStorage.getItem('authToken') || null);
const loading = ref(false);
const error = ref(null);

export function useAuth() {
  const router = useRouter();
  const isAuthenticated = computed(() => !!token.value);

  const login = async (credentials) => {
    loading.value = true;
    error.value = null;

    try {
      const response = await authService.login(credentials.email, credentials.password);

      const { access_token } = response.data;
      token.value = access_token;

      authService.setToken(access_token);
      localStorage.setItem('authToken', access_token);

      // Redirigir a home
      await router.push('/');

      return response.data;
    } catch (err) {
      error.value = err.response?.data?.detail || 'Error al iniciar sesión';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const register = async (formData) => {
    loading.value = true;
    error.value = null;

    try {
      const response = await authService.register(
        formData.email,
        formData.password,
        formData.first_name,
        formData.last_name
      );

      // Hacer login automático después del registro
      await login({
        email: formData.email,
        password: formData.password,
      });

      return response.data;
    } catch (err) {
      error.value = err.response?.data?.detail || 'Error en el registro';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  /**
   * Cerrar sesión
   */
  const logout = () => {
    user.value = null;
    token.value = null;

    authService.logout();
    localStorage.removeItem('authToken');
    localStorage.removeItem('user');

    router.push('/login');
  };

  /**
   * Cargar usuario desde localStorage
   */
  const loadUser = () => {
    const storedUser = localStorage.getItem('user');

    if (storedUser) {
      user.value = JSON.parse(storedUser);
    }
  };

  return {
    user,
    token,
    loading,
    error,
    isAuthenticated,
    login,
    register,
    logout,
    loadUser,
  };
}
