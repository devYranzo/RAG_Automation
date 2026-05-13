import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null);

  const isAuthenticated = computed(() => !!user.value);

  function setUser(userData) {
    user.value = userData;
  }

  function clearAuth() {
    user.value = null;
  }

  return { user, isAuthenticated, setUser, clearAuth };
});
