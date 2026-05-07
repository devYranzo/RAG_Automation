import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '@/views/HomeView.vue';
import FileManager from '@/views/FileManager.vue';
import LoginView from '@/views/LoginView.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView,
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
  },
  {
    path: '/filemanager',
    name: 'File Manager',
    component: FileManager,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
