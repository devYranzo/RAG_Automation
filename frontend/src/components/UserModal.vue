<script setup>
const props = defineProps({
  formData: Object,
  isEdit: Boolean,
});
const emit = defineEmits(['save']);
</script>

<template>
  <div class="modal fade" id="userModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content border-0 shadow rounded-4">
        <div class="modal-header border-0">
          <h5 class="fw-bold">{{ isEdit ? 'Editar' : 'Nuevo' }} Usuario</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="emit('save')">
            <div class="row mb-3">
              <div class="col">
                <label class="form-label">Nombre</label>
                <input v-model="formData.first_name" class="form-control" required />
              </div>
              <div class="col">
                <label class="form-label">Apellido</label>
                <input v-model="formData.last_name" class="form-control" required />
              </div>
            </div>
            <div class="mb-3">
              <label class="form-label">Email</label>
              <input v-model="formData.email" type="email" class="form-control" required />
            </div>
            <div class="mb-3" v-if="!isEdit">
              <label class="form-label">Contraseña</label>
              <input v-model="formData.password" type="password" class="form-control" required />
            </div>
            <div class="mb-3">
              <label class="form-label">Rol</label>
              <select v-model="formData.role" class="form-select">
                <option value="admin">Admin</option>
                <option value="viewer">Viewer</option>
              </select>
            </div>
            <button type="submit" class="btn btn-primary w-100" data-bs-dismiss="modal">
              Guardar
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
