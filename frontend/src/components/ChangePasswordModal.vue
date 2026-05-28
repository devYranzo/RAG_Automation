<script setup>
import { ref } from 'vue';
import authService from '@/services/auth.service';

const emit = defineEmits(['close', 'success']);

const currentPassword = ref('');
const newPassword = ref('');
const confirmPassword = ref('');
const isLoading = ref(false);
const errorMessage = ref('');
const successMessage = ref('');
const showCurrentPassword = ref(false);
const showNewPassword = ref(false);
const showConfirmPassword = ref(false);

const validateForm = () => {
  errorMessage.value = '';

  if (!currentPassword.value) {
    errorMessage.value = 'La contraseña actual es requerida';
    return false;
  }

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

  if (currentPassword.value === newPassword.value) {
    errorMessage.value = 'La nueva contraseña no puede ser igual a la actual';
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
    const response = await authService.changePassword(currentPassword.value, newPassword.value);

    successMessage.value = response.message || 'Contraseña cambiada exitosamente';

    // Limpiar formulario
    currentPassword.value = '';
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
  currentPassword.value = '';
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
          <h5 class="modal-title fw-bold">Cambiar Contraseña</h5>
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

          <!-- Formulario -->
          <form @submit.prevent="handleSubmit" v-if="!successMessage">
            <!-- Contraseña actual -->
            <div class="mb-3">
              <label for="currentPassword" class="form-label">Contraseña Actual</label>
              <div class="input-group">
                <input
                  id="currentPassword"
                  v-model="currentPassword"
                  :type="showCurrentPassword ? 'text' : 'password'"
                  class="form-control"
                  placeholder="Ingresa tu contraseña actual"
                  :disabled="isLoading"
                />
                <button
                  type="button"
                  class="btn btn-outline-secondary"
                  @click="showCurrentPassword = !showCurrentPassword"
                  :disabled="isLoading"
                >
                  <i :class="showCurrentPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
                </button>
              </div>
            </div>

            <!-- Nueva contraseña -->
            <div class="mb-3">
              <label for="newPassword" class="form-label">Nueva Contraseña</label>
              <div class="input-group">
                <input
                  id="newPassword"
                  v-model="newPassword"
                  :type="showNewPassword ? 'text' : 'password'"
                  class="form-control"
                  placeholder="Ingresa tu nueva contraseña"
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
              <label for="confirmPassword" class="form-label">Confirmar Nueva Contraseña</label>
              <div class="input-group">
                <input
                  id="confirmPassword"
                  v-model="confirmPassword"
                  :type="showConfirmPassword ? 'text' : 'password'"
                  class="form-control"
                  placeholder="Confirma tu nueva contraseña"
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
