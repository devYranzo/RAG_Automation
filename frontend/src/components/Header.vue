<script setup>
import { useAuth } from '@/composables/useAuth';
import { useAuthStore } from '@/stores/authStore';
import { onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const { logout, error, fetchProfile } = useAuth();

defineProps({
  isDark: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(['toggle-theme']);

const authStore = useAuthStore();

const route = useRoute();
const router = useRouter();

const handleLogout = () => {
  try {
    logout();
  } catch (e) {
    console.error(e);
  }
};

onMounted(() => {
  fetchProfile();
});
</script>

<template>
  <header class="my-3">
    <div class="d-flex flex-wrap align-items-center justify-content-between gap-3 mb-4">
      <!-- LOGO -->
      <h1 class="display-6 fw-bold text-primary mb-0 pe-3 border-end">
        <i class="bi bi-people me-2 text-dark"></i>
        Talent <span class="text-dark">Finder</span>
      </h1>

      <!-- NAV -->
      <div class="nav nav-pills bg-light rounded-pill shadow-sm">
        <router-link
          to="/"
          class="nav-link rounded-pill px-4"
          :class="{ active: route.path === '/' }"
        >
          <i class="bi bi-search me-1"></i> Buscador
        </router-link>

        <router-link
          to="/filemanager"
          class="nav-link rounded-pill px-4"
          :class="{ active: route.path === '/filemanager' }"
        >
          <i class="bi bi-folder-fill me-1"></i> Gestión CVs
        </router-link>
      </div>

      <!-- ACTIONS + USER -->
      <div class="d-flex gap-2 align-items-center">
        <span class="badge bg-primary text-capitalize">{{ authStore.user?.role }}</span>
        <!-- USER DROPDOWN -->
        <div class="dropdown">
          <button
            class="btn btn-light rounded-circle d-flex align-items-center justify-content-center shadow-sm"
            type="button"
            data-bs-toggle="dropdown"
            aria-expanded="false"
            style="width: 40px; height: 40px"
          >
            <i class="bi bi-person-fill"></i>
          </button>

          <ul class="dropdown-menu dropdown-menu-end shadow-sm">
            <li>
              <button class="dropdown-item" @click="router.push('/dashboard')">
                <i class="bi bi-speedometer2 me-2"></i> Dashboard
              </button>
            </li>

            <li>
              <button class="dropdown-item" @click="emit('toggle-theme')">
                <i class="bi bi-circle-half me-2"></i> Cambiar tema
              </button>
            </li>

            <li><hr class="dropdown-divider" /></li>

            <li>
              <button class="dropdown-item text-danger" @click="handleLogout">
                <i class="bi bi-box-arrow-right me-2"></i> Cerrar sesión
              </button>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </header>
</template>

<style scoped>
.nav-pills .nav-link {
  color: #6c757d;
  font-weight: 500;
  transition: all 0.3s ease;
}

.nav-pills .nav-link.active {
  background-color: #0d6efd;
  color: white;
  box-shadow: 0 4px 10px rgba(13, 110, 253, 0.2);
}

.alert {
  font-size: 0.95rem;
}
</style>
