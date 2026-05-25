<script setup lang="ts">
import Header from './components/Header.vue';
import { useRoute } from 'vue-router';
import { useMotorStatus } from '@/composables/useMotorStatus';
import { useTheme } from '@/composables/useTheme';
import { onMounted } from 'vue';
import { useAuth } from './composables/useAuth';
import Footer from './components/Footer.vue';

const route = useRoute();
const { isReady, encenderMotor, reindexar } = useMotorStatus();
const { isDark, toggleTheme } = useTheme();
const { fetchProfile } = useAuth();

onMounted(async () => {
  await fetchProfile();
});
</script>

<template>
  <div class="container-lg d-flex flex-column min-vh-100">
    <a href="#main-content" class="skip-link visually-hidden-focusable"
      >Saltar al contenido principal</a
    >
    <Header
      v-if="!route.meta.hideHeader"
      :is-ready="isReady"
      :is-dark="isDark"
      @encender="encenderMotor"
      @reindexar="reindexar"
      @toggle-theme="toggleTheme"
    />
    <main id="main-content" class="flex-grow-1">
      <router-view />
    </main>
    <Footer />
  </div>
</template>

<style>
.container-lg {
  max-width: 1100px;
}
/* Estilo para saber qué link está activo */
.router-link-active {
  color: #fff !important;
  font-weight: bold;
}
</style>
