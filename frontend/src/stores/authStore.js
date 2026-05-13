import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

export const useAuthStore = defineStore('auth', () => {
  // --- ESTADO ---
  const token = ref(localStorage.getItem('token') || null);

  const user = ref(
    (() => {
      try {
        const savedUser = localStorage.getItem('user');
        return savedUser ? JSON.parse(savedUser) : null;
      } catch (e) {
        console.error('Error al recuperar sesión de usuario');
        localStorage.removeItem('user');
        return null;
      }
    })()
  );

  // --- GETTERS ---
  const isAuthenticated = computed(() => !!token.value && !!user.value);

  const isAdmin = computed(() => user.value?.role === 'admin' || user.value?.is_staff === true);

  const fullName = computed(() => {
    if (!user.value) return 'Usuario';
    const first = user.value.first_name || '';
    const last = user.value.last_name || '';
    const name = `${first} ${last}`.trim();
    return name || user.value.username || 'Usuario';
  });

  // --- ACCIONES ---

  function setUser(userData) {
    if (!userData) {
      clearAuth();
      return;
    }

    user.value = userData;
    localStorage.setItem('user', JSON.stringify(userData));
  }

  function setToken(newToken) {
    if (!newToken) {
      clearAuth();
      return;
    }
    token.value = newToken;
    localStorage.setItem('token', newToken);
  }

  function clearAuth() {
    user.value = null;
    token.value = null;
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  }

  return {
    user,
    token,
    isAuthenticated,
    isAdmin,
    fullName,
    setUser,
    setToken,
    clearAuth,
  };
});
