import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/stores/authStore';
import { useAuth } from '@/composables/useAuth';

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/LoginView.vue'),
    meta: { hideHeader: true },
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
    meta: { requiresAuth: true, allowedRoles: ['admin'] },
  },
  {
    path: '/filemanager',
    name: 'File Manager',
    component: () => import('@/views/FileManager.vue'),
    meta: { requiresAuth: true, allowedRoles: ['admin', 'recruiter'] },
  },
  {
    path: '/error/:code',
    name: 'Error',
    component: () => import('@/views/ErrorView.vue'),
    props: true,
    meta: { hideHeader: true },
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/error/404',
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

  if (to.meta.allowedRoles) {
    const userRole = authStore.user?.role?.toLowerCase();

    if (!to.meta.allowedRoles.includes(userRole)) {
      console.warn(`Acceso denegado a ${to.path}. Rol requerido: ${to.meta.allowedRoles}`);
      // Redirigir a Home o a una página de "No autorizado"
      return { path: '/' };
    }
  }

  if (to.name === 'Login' && authStore.isAuthenticated) {
    return { path: '/' };
  }
});

export default router;
