<script setup>
import { ref, onMounted, computed } from 'vue';
import { useAuthStore } from '@/stores/authStore';
import userService from '@/services/user.service'; // Importa el servicio

const authStore = useAuthStore();
const users = ref([]); // Variable para guardar la lista
const isLoading = ref(true);

// Función para cargar los usuarios
const loadUsers = async () => {
  try {
    isLoading.value = true;
    users.value = await userService.getAllUsers();
  } catch (error) {
    console.error('Error cargando usuarios:', error);
  } finally {
    isLoading.value = false;
  }
};

// Ejecutar al montar el componente
onMounted(() => {
  loadUsers();
});

// Helper para colores de estado (ahora recibe al usuario como parámetro)
const getStatusClass = (user) => {
  return user.is_active ? 'bg-success' : 'bg-secondary';
};
</script>

<template>
  <div class="card border-0 shadow-sm rounded-4 p-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h5 class="fw-bold m-0">Gestión de Usuarios</h5>
      <button class="btn btn-primary btn-sm rounded-pill px-3">
        <i class="bi bi-plus"></i> Nuevo Usuario
      </button>
    </div>

    <div class="table-responsive">
      <table class="table align-middle">
        <thead class="table-light">
          <tr>
            <th>Nombre</th>
            <th>Email</th>
            <th>Rol</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="isLoading">
            <td colspan="5" class="text-center py-4">
              <div class="spinner-border spinner-border-sm text-primary" role="status"></div>
              <span class="ms-2">Cargando usuarios...</span>
            </td>
          </tr>

          <tr v-for="user in users" :key="user.id">
            <td>
              <div class="d-flex align-items-center">
                <div
                  class="avatar-sm me-2 bg-light rounded-circle text-center"
                  style="width: 32px; height: 32px; line-height: 32px"
                >
                  {{ user.first_name.charAt(0) }}{{ user.last_name.charAt(0) }}
                </div>
                {{ user.first_name }} {{ user.last_name }}
              </div>
            </td>
            <td>{{ user.email }}</td>
            <td>
              <span class="badge bg-primary-subtle text-primary text-capitalize">
                {{ user.role || 'Usuario' }}
              </span>
            </td>
            <td>
              <span class="badge text-capitalize" :class="getStatusClass(user)">
                {{ user.is_active ? 'Activa' : 'Inactiva' }}
              </span>
            </td>
            <td>
              <button class="btn btn-light btn-sm border">Editar</button>
            </td>
          </tr>

          <tr v-if="!isLoading && users.length === 0">
            <td colspan="5" class="text-center text-muted py-4">No se encontraron usuarios.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
