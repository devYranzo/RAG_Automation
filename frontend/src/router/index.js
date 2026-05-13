import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '@/views/HomeView.vue';
import FileManager from '@/views/FileManager.vue';
import LoginView from '@/views/LoginView.vue';
import DashboardView from '@/views/DashboardView.vue';
import { useAuthStore } from '@/stores/authStore';
import { useAuth } from '@/composables/useAuth';

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
  },
  {
    path: '/',
    name: 'Home',
    component: HomeView,
    meta: { requiresAuth: true },
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: DashboardView,
    meta: { requiresAuth: true },
  },
  {
    path: '/filemanager',
    name: 'File Manager',
    component: FileManager,
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to) => {
  const authStore = useAuthStore();
  const { fetchProfile } = useAuth();

  if (to.meta.requiresAuth) {
    if (!authStore.isAuthenticated) {
      const user = await fetchProfile();

      if (!user) {
        return {
          name: 'Login',
          query: { redirect: to.fullPath },
        };
      }
    }
  }

  if (to.name === 'Login' && authStore.isAuthenticated) {
    return { path: '/' };
  }
});

export default router;
