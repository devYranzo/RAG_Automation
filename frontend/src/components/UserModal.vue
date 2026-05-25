<script setup>
const props = defineProps({
  formData: Object,
  isEdit: Boolean,
});
const emit = defineEmits(['save']);
</script>

<template>
  <div class="modal fade" id="userModal" tabindex="-1" role="dialog" aria-modal="true" aria-labelledby="userModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content border-0 shadow rounded-4">
        <div class="modal-header border-0">
          <h5 class="fw-bold" id="userModalLabel">{{ isEdit ? 'Editar' : 'Nuevo' }} Usuario</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Cerrar"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="emit('save')">
            <div class="row mb-3">
              <div class="col">
                <label for="firstNameInput" class="form-label">Nombre</label>
                <input id="firstNameInput" v-model="formData.first_name" class="form-control" autocomplete="given-name" required />
              </div>
              <div class="col">
                <label for="lastNameInput" class="form-label">Apellido</label>
                <input id="lastNameInput" v-model="formData.last_name" class="form-control" autocomplete="family-name" required />
              </div>
            </div>
            <div class="mb-3">
              <label for="emailInput" class="form-label">Email</label>
              <input id="emailInput" v-model="formData.email" type="email" class="form-control" autocomplete="email" required />
            </div>
            <div class="mb-3" v-if="!isEdit">
              <label for="passwordInput" class="form-label">Contraseña</label>
              <input id="passwordInput" v-model="formData.password" type="password" class="form-control" autocomplete="new-password" required />
            </div>
            <div class="mb-3">
              <label for="roleSelect" class="form-label">Rol</label>
              <select id="roleSelect" v-model="formData.role" class="form-select">
                <option value="admin">Admin</option>
                <option value="recruiter">Recruiter</option>
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
