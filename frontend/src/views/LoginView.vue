<script setup>
import AuthLayout from '@/components/AuthLayout.vue';
import { useAuth } from '@/composables/useAuth';
import { reactive } from 'vue';

const { login, loading, error } = useAuth();

const form = reactive({
  email: '',
  password: '',
});

const handleLogin = async () => {
  try {
    await login(form);
  } catch (e) {
    console.error(e);
  }
};
</script>

<template>
  <AuthLayout title-primary="Talent" title-secondary="Finder" subtitle="Smarter hiring starts here">
    <h1 class="text-secondary mb-4 fs-5">Bienvenido de nuevo</h1>

    <form @submit.prevent="handleLogin">
      <div class="mb-3">
        <label for="email" class="form-label small fw-bold">Correo electrónico</label>
        <div class="input-group">
          <span class="input-group-text bg-light border-end-0">
            <i class="bi bi-envelope text-muted" aria-hidden="true"></i>
          </span>
          <input
            type="email"
            class="form-control border-start-0"
            v-model="form.email"
            id="email"
            placeholder="tu@correo.com"
            autocomplete="username email"
            aria-describedby="emailHelp"
            required
            autofocus
          />
        </div>
        <small id="emailHelp" class="form-text text-muted">Utiliza tu correo registrado</small>
      </div>

      <div class="mb-4">
        <label for="password" class="form-label small fw-bold">Contraseña</label>
        <div class="input-group">
          <span class="input-group-text bg-light border-end-0">
            <i class="bi bi-lock text-muted" aria-hidden="true"></i>
          </span>
          <input
            type="password"
            v-model="form.password"
            class="form-control border-start-0"
            id="password"
            placeholder="········"
            autocomplete="current-password"
            aria-describedby="passwordHelp"
            required
          />
        </div>
        <small id="passwordHelp" class="form-text text-muted"
          >Tu contraseña es privada y segura</small
        >
      </div>

      <div class="d-grid">
        <button
          type="submit"
          :disabled="loading"
          class="btn btn-primary btn-lg"
          :aria-busy="loading"
        >
          {{ loading ? 'Iniciando sesión...' : 'Iniciar sesión' }}
        </button>
        <div class="d-block mt-3 text-primary small">
          <span class="text-muted me-1">¿No tienes cuenta?</span>
          <router-link to="/register" class="text-decoration-none">
            <b>Regístrate aquí</b>
          </router-link>
        </div>
      </div>

      <div v-if="error" class="alert alert-danger mt-3 mb-0" role="alert">
        <i class="bi bi-exclamation-circle me-2" aria-hidden="true"></i>
        <strong>Error:</strong> {{ error }}
      </div>
    </form>
  </AuthLayout>
</template>
