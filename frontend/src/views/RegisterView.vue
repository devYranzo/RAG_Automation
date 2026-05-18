<script setup>
import AuthLayout from '@/components/AuthLayout.vue';
import { useAuth } from '@/composables/useAuth';
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const currentStep = ref(1);
const errorMessage = ref('');

const { register, loading, error } = useAuth();

const form = reactive({
  company_name: '',
  email: '',
  password: '',
});

const goToNextStep = () => {
  if (form.company_name.trim()) {
    errorMessage.value = '';
    currentStep.value = 2;
  }
};

const handleRegister = async () => {
  try {
    await register(form);
  } catch (e) {
    console.error(e);
  }
};
</script>

<template>
  <AuthLayout
    title-primary="Talent"
    title-secondary="Finder"
    subtitle="Create your workspace in seconds"
  >
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h4 class="text-secondary mb-0">
        {{ currentStep === 1 ? 'Step 1: Your Company' : 'Step 2: Admin Account' }}
      </h4>
      <span class="badge bg-light text-muted border">{{ currentStep }} / 2</span>
    </div>

    <form @submit.prevent="handleRegister">
      <div v-if="currentStep === 1" class="step-animation">
        <div class="mb-4">
          <label for="companyName" class="form-label small fw-bold"
            >Company / Organization Name</label
          >
          <div class="input-group shadow-sm">
            <span class="input-group-text bg-light border-end-0">
              <i class="bi bi-building text-muted"></i>
            </span>
            <input
              type="text"
              class="form-control border-start-0"
              v-model="form.company_name"
              id="companyName"
              placeholder="Company name"
              required
              autofocus
            />
          </div>
          <div class="form-text text-muted small mt-2">
            This will be the name of your private workspace.
          </div>
        </div>

        <div class="d-grid mt-5">
          <button
            type="button"
            @click="goToNextStep"
            :disabled="!form.company_name"
            class="btn btn-primary btn-lg shadow-sm"
          >
            Continue <i class="bi bi-arrow-right ms-2"></i>
          </button>
        </div>
      </div>

      <div v-if="currentStep === 2" class="step-animation">
        <div class="mb-3">
          <label for="email" class="form-label small fw-bold">Admin Email address</label>
          <div class="input-group shadow-sm">
            <span class="input-group-text bg-light border-end-0">
              <i class="bi bi-envelope text-muted"></i>
            </span>
            <input
              type="email"
              class="form-control border-start-0"
              v-model="form.email"
              id="email"
              placeholder="you@company.com"
              required
            />
          </div>
        </div>

        <div class="mb-4">
          <label for="password" class="form-label small fw-bold">Password</label>
          <div class="input-group shadow-sm">
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

        <div class="d-grid gap-2">
          <button type="submit" :disabled="loading" class="btn btn-primary btn-lg shadow-sm">
            {{ loading ? 'Creating Workspace...' : 'Complete Setup' }}
          </button>

          <button
            type="button"
            @click="currentStep = 1"
            class="btn btn-link text-muted text-decoration-none small"
          >
            <i class="bi bi-arrow-left me-1"></i> Back to company info
          </button>
        </div>
      </div>

      <div v-if="errorMessage" class="alert alert-danger mt-3 mb-0">
        <i class="bi bi-exclamation-circle me-2"></i>
        {{ errorMessage }}
      </div>

      <div class="d-block mt-3 text-primary small">
        <span class="text-muted me-1">Already have an account?</span>
        <router-link to="/login" class="text-decoration-none">
          <b>Sign In</b>
        </router-link>
      </div>
    </form>
  </AuthLayout>
</template>

<style scoped>
/* Un pequeño efecto de transición para que no cambie de golpe */
.step-animation {
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(5px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
