import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/stores/authStore';
import { useAuth } from '@/composables/useAuth';

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/LoginView.vue'),
  },
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/HomeView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/DashboardView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/filemanager',
    name: 'File Manager',
    component: () => import('@/views/FileManager.vue'),
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
