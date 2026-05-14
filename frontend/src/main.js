import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import 'bootstrap-icons/font/bootstrap-icons.css';
import router from './router';

// Initialize theme on app load
const initializeTheme = () => {
  const savedTheme = localStorage.getItem('theme');
  const isDark = savedTheme
    ? savedTheme === 'dark'
    : window.matchMedia('(prefers-color-scheme: dark)').matches;

  if (isDark) {
    document.documentElement.setAttribute('data-bs-theme', 'dark');
  } else {
    document.documentElement.removeAttribute('data-bs-theme');
  }
};

// Initialize pinia
const pinia = createPinia();

initializeTheme();

const app = createApp(App);
app.use(router);
app.use(pinia);
app.mount('#app');
