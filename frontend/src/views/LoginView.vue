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
    <h4 class="text-secondary mb-4">Welcome Back</h4>

    <form @submit.prevent="handleLogin">
      <div class="mb-3">
        <label for="email" class="form-label small fw-bold">Email address</label>
        <div class="input-group">
          <span class="input-group-text bg-light border-end-0">
            <i class="bi bi-envelope text-muted"></i>
          </span>
          <input
            type="email"
            class="form-control border-start-0"
            v-model="form.email"
            id="email"
            placeholder="your@account.com"
            required
            autofocus
          />
        </div>
      </div>

      <div class="mb-4">
        <label for="password" class="form-label small fw-bold">Password</label>
        <div class="input-group">
          <span class="input-group-text bg-light border-end-0">
            <i class="bi bi-lock text-muted"></i>
          </span>
          <input
            type="password"
            v-model="form.password"
            class="form-control border-start-0"
            id="password"
            placeholder="········"
            required
          />
        </div>
      </div>

      <div class="d-grid">
        <button type="submit" :disabled="loading" class="btn btn-primary btn-lg">
          {{ loading ? 'Signing In...' : 'Sign In' }}
        </button>
        <div class="d-block mt-3 text-primary small">
          <span class="text-muted me-1">Don't have an account?</span>
          <router-link to="/register" class="text-decoration-none">
            <b>Sign Up</b>
          </router-link>
        </div>
      </div>

      <div v-if="error" class="alert alert-danger mt-3 mb-0">
        <i class="bi bi-exclamation-circle me-2"></i>
        {{ error }}
      </div>
    </form>
  </AuthLayout>
</template>
