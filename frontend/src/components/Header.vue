<script setup>
import { useAuth } from '@/composables/useAuth';
import { useAuthStore } from '@/stores/authStore';
import { useRoute, useRouter } from 'vue-router';
import { ref } from 'vue';
import ChangePasswordModal from './ChangePasswordModal.vue';

const { logout } = useAuth();

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

const showChangePasswordModal = ref(false);

const handleLogout = () => {
  try {
    logout();
  } catch (e) {
    console.error(e);
  }
};

const handlePasswordChangeSuccess = () => {
  showChangePasswordModal.value = false;
};
</script>

<template>
  <header class="my-3">
    <div class="d-flex flex-wrap align-items-center justify-content-between gap-3 mb-4">
      <!-- LOGO -->
      <h1 class="display-6 fw-bold text-primary mb-0 pe-3 border-end">
        <i class="bi bi-people me-2 text-body" aria-hidden="true"></i>
        Talent <span class="text-body">Finder</span>
      </h1>

      <!-- NAV -->
      <nav class="nav nav-pills bg-light rounded-pill shadow-sm" aria-label="Navegación principal">
        <router-link
          to="/"
          v-if="authStore.requireAnyUser"
          class="nav-link rounded-pill px-4"
          :class="{ active: route.path === '/' }"
        >
          <i class="bi bi-search me-1" aria-hidden="true"></i> Buscador
        </router-link>

        <router-link
            to="/hiringProjects"
            v-if="authStore.requireAtLeastRecruiter"
            class="nav-link rounded-pill px-4"
            :class="{ active: route.path === '/hiringProjects' }"
        >
          <i class="bi bi-clipboard2-data-fill me-1" aria-hidden="true"></i> Procesos
        </router-link>

        <router-link
          to="/filemanager"
          v-if="authStore.requireAtLeastRecruiter"
          class="nav-link rounded-pill px-4"
          :class="{ active: route.path === '/filemanager' }"
        >
          <i class="bi bi-folder-fill me-1" aria-hidden="true"></i> Gestión CVs
        </router-link>
      </nav>

      <!-- ACTIONS + USER -->
      <div class="d-flex gap-2 align-items-center">
        <span class="badge bg-primary text-capitalize" role="status" aria-label="Rol de usuario">{{
          authStore.user?.role
        }}</span>
        <!-- USER DROPDOWN -->
        <div class="dropdown">
          <button
            class="btn btn-light rounded-circle d-flex align-items-center justify-content-center shadow-sm"
            type="button"
            data-bs-toggle="dropdown"
            aria-expanded="false"
            :aria-label="`Menú de usuario ${authStore.user?.profile?.first_name || 'Usuario'}`"
            style="width: 40px; height: 40px"
          >
            <i class="bi bi-person-fill" aria-hidden="true"></i>
          </button>

          <ul class="dropdown-menu dropdown-menu-end shadow-sm">
            <li>
              <button
                v-if="authStore.requireAdmin"
                class="dropdown-item"
                @click="router.push('/dashboard')"
              >
                <i class="bi bi-speedometer2 me-2" aria-hidden="true"></i>Dashboard
              </button>
            </li>

            <li>
              <button class="dropdown-item" @click="showChangePasswordModal = true">
                <i class="bi bi-key me-2" aria-hidden="true"></i>Cambiar Contraseña
              </button>
            </li>

            <li>
              <button
                class="dropdown-item"
                @click="emit('toggle-theme')"
                :aria-label="`Cambiar a tema ${isDark ? 'claro' : 'oscuro'}`"
              >
                <i class="bi bi-circle-half me-2" aria-hidden="true"></i>Cambiar tema
              </button>
            </li>

            <li><hr class="dropdown-divider" /></li>

            <li>
              <button class="dropdown-item text-danger" @click="handleLogout">
                <i class="bi bi-box-arrow-right me-2" aria-hidden="true"></i> Cerrar sesión
              </button>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <!-- Modal de cambio de contraseña -->
    <ChangePasswordModal
      v-if="showChangePasswordModal"
      @close="showChangePasswordModal = false"
      @success="handlePasswordChangeSuccess"
    />
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
</style>
