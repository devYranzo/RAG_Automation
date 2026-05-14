<template>
  <AuthLayout title-secondary="Error" subtitle="Something went sideways">
    <div class="text-start">
      <h2 class="display-3 fw-bold text-danger mb-3">{{ errorCode }}</h2>

      <h3 class="fw-bold text-dark">{{ errorConfig.title }}</h3>
      <p class="text-muted mb-5">
        {{ errorConfig.message }}
      </p>

      <div class="d-grid gap-2">
        <router-link to="/" class="btn btn-primary btn-lg"> Return to Home Page </router-link>
        <button @click="router.go(-1)" class="btn btn-link text-muted text-decoration-none small">
          Go back
        </button>
      </div>
    </div>
  </AuthLayout>
</template>

<script setup>
import AuthLayout from '@/components/AuthLayout.vue';
import { computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();

const errorCode = computed(() => route.params.code || '500');

const errorConfigs = {
  403: {
    title: 'Access Denied',
    message:
      'You do not have permission to view this resource. Your role does not authorize access here.',
  },
  404: {
    title: 'Page Not Found',
    message: 'The page you are looking for might have been removed or is temporarily unavailable.',
  },
  500: {
    title: 'Server Error',
    message: 'Our servers are having a bit of a crisis. We are working on fixing it.',
  },
};

const errorConfig = computed(() => errorConfigs[errorCode.value] || errorConfigs['500']);
</script>
