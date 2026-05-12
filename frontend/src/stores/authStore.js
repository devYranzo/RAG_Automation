import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

export const useAuthStore = defineStore('auth', () => {
  // Estado
  const user = ref(null);
  const token = ref(localStorage.getItem('token') || null);

  // Getters
  const isAuthenticated = computed(() => !!token.value);
  const fullName = computed(() => {
    if (!user.value) return 'Usuario';
    return `${user.value.first_name} ${user.value.last_name}`;
  });

  // Acciones de estado
  function setUser(userData) {
    user.value = userData;
  }

  function setToken(newToken) {
    token.value = newToken;
    if (newToken) {
      localStorage.setItem('token', newToken);
    } else {
      localStorage.removeItem('token');
    }
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
    fullName,
    setUser,
    setToken,
    clearAuth,
  };
});
