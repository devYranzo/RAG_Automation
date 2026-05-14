import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null);

  const isAuthenticated = computed(() => !!user.value);

  const hasRole = (allowedRoles) => {
    if (!user.value) return false;
    return allowedRoles.includes(user.value.role?.toLowerCase());
  };

  const requireAtLeastRecruiter = computed(() => hasRole(['admin', 'recruiter']));
  const requireAdmin = computed(() => hasRole(['admin']));
  const requireAnyUser = computed(() => hasRole(['admin', 'recruiter', 'viewer']));

  function setUser(userData) {
    user.value = userData;
  }

  function clearAuth() {
    user.value = null;
  }

  return {
    user,
    isAuthenticated,
    requireAdmin,
    requireAtLeastRecruiter,
    requireAnyUser,
    setUser,
    clearAuth,
  };
});
