<script setup>
import { ref } from 'vue';
import userService from '@/services/user.service';

const props = defineProps({
  userId: Number,
  userName: String,
});

const emit = defineEmits(['close', 'success']);

const newPassword = ref('');
const confirmPassword = ref('');
const isLoading = ref(false);
const errorMessage = ref('');
const successMessage = ref('');
const showNewPassword = ref(false);
const showConfirmPassword = ref(false);

const validateForm = () => {
  errorMessage.value = '';

  if (!newPassword.value) {
    errorMessage.value = 'La nueva contraseña es requerida';
    return false;
  }

  if (newPassword.value.length < 6) {
    errorMessage.value = 'La nueva contraseña debe tener al menos 6 caracteres';
    return false;
  }

  if (newPassword.value !== confirmPassword.value) {
    errorMessage.value = 'Las contraseñas no coinciden';
    return false;
  }

  return true;
};

const handleSubmit = async () => {
  if (!validateForm()) {
    return;
  }

  isLoading.value = true;
  errorMessage.value = '';

  try {
    await userService.editUser({
      id: props.userId,
      password: newPassword.value,
    });

    successMessage.value = `Contraseña de ${props.userName} cambiada exitosamente`;

    // Limpiar formulario
    newPassword.value = '';
    confirmPassword.value = '';

    // Cerrar modal después de 2 segundos
    setTimeout(() => {
      emit('success');
      emit('close');
    }, 2000);
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || 'Error al cambiar la contraseña';
  } finally {
    isLoading.value = false;
  }
};

const handleClose = () => {
  newPassword.value = '';
  confirmPassword.value = '';
  errorMessage.value = '';
  successMessage.value = '';
  emit('close');
};
</script>

<template>
  <div
    class="modal fade show d-block"
    tabindex="-1"
    role="dialog"
    style="background-color: rgba(0, 0, 0, 0.5)"
  >
    <div class="modal-dialog modal-dialog-centered" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title fw-bold">Cambiar Contraseña de {{ userName }}</h5>
          <button
            type="button"
            class="btn-close"
            aria-label="Close"
            @click="handleClose"
            :disabled="isLoading"
          ></button>
        </div>

        <div class="modal-body">
          <!-- Mensaje de éxito -->
          <div v-if="successMessage" class="alert alert-success mb-3" role="alert">
            <i class="bi bi-check-circle"></i> {{ successMessage }}
          </div>

          <!-- Mensaje de error -->
          <div v-if="errorMessage" class="alert alert-danger mb-3" role="alert">
            <i class="bi bi-exclamation-triangle"></i> {{ errorMessage }}
          </div>

          <!-- Nota informativa -->
          <div v-if="!successMessage" class="alert alert-info mb-3" role="alert">
            <i class="bi bi-info-circle"></i>
            <small
              >Establece la nueva contraseña para este usuario. El usuario podrá cambiarla
              posteriormente.</small
            >
          </div>

          <!-- Formulario -->
          <form @submit.prevent="handleSubmit" v-if="!successMessage">
            <!-- Nueva contraseña -->
            <div class="mb-3">
              <label for="newPassword" class="form-label">Nueva Contraseña</label>
              <div class="input-group">
                <input
                  id="newPassword"
                  v-model="newPassword"
                  :type="showNewPassword ? 'text' : 'password'"
                  class="form-control"
                  placeholder="Ingresa la nueva contraseña"
                  :disabled="isLoading"
                />
                <button
                  type="button"
                  class="btn btn-outline-secondary"
                  @click="showNewPassword = !showNewPassword"
                  :disabled="isLoading"
                >
                  <i :class="showNewPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
                </button>
              </div>
              <small class="text-muted">Mínimo 6 caracteres</small>
            </div>

            <!-- Confirmar contraseña -->
            <div class="mb-3">
              <label for="confirmPassword" class="form-label">Confirmar Contraseña</label>
              <div class="input-group">
                <input
                  id="confirmPassword"
                  v-model="confirmPassword"
                  :type="showConfirmPassword ? 'text' : 'password'"
                  class="form-control"
                  placeholder="Confirma la nueva contraseña"
                  :disabled="isLoading"
                />
                <button
                  type="button"
                  class="btn btn-outline-secondary"
                  @click="showConfirmPassword = !showConfirmPassword"
                  :disabled="isLoading"
                >
                  <i :class="showConfirmPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
                </button>
              </div>
            </div>
          </form>
        </div>

        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-secondary"
            @click="handleClose"
            :disabled="isLoading"
          >
            Cerrar
          </button>
          <button
            type="button"
            class="btn btn-primary"
            @click="handleSubmit"
            :disabled="isLoading || !!successMessage"
          >
            <span
              v-if="isLoading"
              class="spinner-border spinner-border-sm me-2"
              role="status"
              aria-hidden="true"
            ></span>
            {{ isLoading ? 'Cambiando...' : 'Cambiar Contraseña' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal.show {
  display: block;
}

.input-group .btn-outline-secondary {
  border-color: #dee2e6;
  color: #6c757d;
}

.input-group .btn-outline-secondary:hover {
  background-color: #f8f9fa;
  border-color: #dee2e6;
}

.input-group .btn-outline-secondary:disabled {
  opacity: 0.65;
  cursor: not-allowed;
}
</style>
