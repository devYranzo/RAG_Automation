<script setup>
import { ref, onMounted } from 'vue';
import userService from '@/services/user.service';
import UserModal from '../UserModal.vue';
import { useAuthStore } from '@/stores/authStore';

const users = ref([]);
const isLoading = ref(true);
const isEdit = ref(false);

const authStore = useAuthStore();

const form = ref({
  id: null,
  email: '',
  first_name: '',
  last_name: '',
  password: '',
  role: 'viewer',
});

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

const openCreate = () => {
  isEdit.value = false;
  form.value = { id: null, email: '', first_name: '', last_name: '', password: '', role: 'viewer' };
};

const openEdit = (user) => {
  isEdit.value = true;
  form.value = {
    ...user,
    password: '',
  };
};

const isCurrentUser = (rowUserId) => {
  if (!authStore.user) return false;
  return authStore.user.profile_id === rowUserId;
};

const handleSave = async () => {
  try {
    if (isEdit.value) {
      await userService.editUser(form.value);
    } else {
      await userService.createUser(form.value);
    }
    await loadUsers();
  } catch (error) {
    alert('Error: ' + (error.response?.data?.detail || 'No se pudo procesar la solicitud'));
  }
};

const handleDelete = async (user) => {
  // Confirmación nativa del navegador (puedes usar SweetAlert2 si quieres algo más pro)
  const confirmed = confirm(`¿Estás seguro de que quieres eliminar a ${user.first_name}?`);

  if (confirmed) {
    try {
      await userService.deleteUser(user.id);
      await loadUsers();
    } catch (error) {
      alert(error.response?.data?.detail || 'Error al eliminar usuario');
    }
  }
};

onMounted(loadUsers);
</script>

<template>
  <div class="card border-0 shadow-sm rounded-4 p-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h5 class="fw-bold m-0">Gestión de Usuarios</h5>
        <p class="text-muted small m-0">Administra los accesos y roles del sistema</p>
      </div>
      <button
        class="btn btn-primary btn-sm rounded-pill px-3 shadow-sm"
        data-bs-toggle="modal"
        data-bs-target="#userModal"
        @click="openCreate"
      >
        <i class="bi bi-person-plus-fill me-1" aria-hidden="true"></i> Nuevo Usuario
      </button>
    </div>

    <div class="table-responsive">
      <table class="table table-hover align-middle">
        <thead class="table-light">
          <tr>
            <th scope="col" class="border-0 rounded-start ps-3">Usuario</th>
            <th scope="col" class="border-0">Email</th>
            <th scope="col" class="border-0">Rol</th>
            <th scope="col" class="border-0">Estado</th>
            <th scope="col" class="border-0 rounded-end text-end pe-3">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="isLoading">
            <td colspan="5" class="text-center py-5">
              <div class="spinner-border spinner-border-sm text-primary" role="status"></div>
              <span class="ms-2">Cargando usuarios...</span>
            </td>
          </tr>

          <tr v-for="user in users" :key="user.id">
            <td class="ps-3">
              <div class="d-flex align-items-center">
                <div
                  class="avatar-sm bg-light rounded-circle d-flex align-items-center justify-content-center me-2"
                  style="width: 32px; height: 32px"
                >
                  <i class="bi bi-person text-primary" aria-hidden="true"></i>
                </div>
                <span class="fw-medium">{{ user.first_name }} {{ user.last_name }}</span>
              </div>
            </td>
            <td>{{ user.email }}</td>
            <td>
              <span
                class="badge rounded-pill text-capitalize"
                :class="
                  user.role === 'admin' ? 'bg-primary-subtle text-primary' : 'bg-light  border'
                "
              >
                {{ user.role }}
              </span>
            </td>
            <td>
              <span
                v-if="user.is_active"
                class="badge bg-success-subtle text-success border border-success-subtle"
                >Activo</span
              >
              <span v-else class="badge bg-danger-subtle text-danger border border-danger-subtle"
                >Inactivo</span
              >
            </td>
            <td class="text-end pe-3">
              <button
                class="btn btn-outline-secondary btn-sm rounded-pill px-3 me-1"
                data-bs-toggle="modal"
                data-bs-target="#userModal"
                @click="openEdit(user)"
                :disabled="isCurrentUser(user.id)"
                :class="{ 'opacity-50': isCurrentUser(user.id) }"
                :aria-label="'Editar usuario ' + user.first_name + ' ' + user.last_name"
              >
                <i class="bi bi-pencil" aria-hidden="true"></i>
              </button>
              <button
                @click="handleDelete(user)"
                class="btn btn-outline-danger btn-sm rounded-pill px-3"
                :disabled="isCurrentUser(user.id)"
                :class="{ 'opacity-50': isCurrentUser(user.id) }"
                :aria-label="'Eliminar usuario ' + user.first_name + ' ' + user.last_name"
              >
                <i class="bi bi-trash" aria-hidden="true"></i>
              </button>
            </td>
          </tr>

          <tr v-if="!isLoading && users.length === 0">
            <td colspan="5" class="text-center py-4 text-muted">No se encontraron usuarios.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <UserModal :formData="form" :isEdit="isEdit" @save="handleSave" />
  </div>
</template>

<style scoped>
.table thead th {
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 700;
  color: #6c757d;
  background-color: #f8f9fa;
}

.avatar-sm {
  font-size: 0.9rem;
}

.badge {
  font-weight: 600;
  padding: 0.5em 0.8em;
}

.bg-primary-subtle {
  background-color: #e7f1ff;
}
.bg-success-subtle {
  background-color: #e1f7ec;
}
.bg-danger-subtle {
  background-color: #feecef;
}
</style>
