<script setup>
import { useAuthStore } from '@/stores/authStore';

const authStore = useAuthStore();
</script>

<template>
  <div class="card border-0 shadow-sm rounded-4 p-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h5 class="fw-bold m-0">Gestión de Usuarios</h5>
      <button class="btn btn-primary btn-sm rounded-pill px-3">+ Nuevo Usuario</button>
    </div>
    <div class="table-responsive">
      <table class="table align-middle">
        <thead class="table-light">
          <tr>
            <th>Nombre</th>
            <th>Email</th>
            <th>Rol</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>{{ authStore.fullName }}</td>
            <td>admin@talent.com</td>
            <td><span class="badge bg-primary-subtle text-primary">Admin</span></td>
            <td><button class="btn btn-light btn-sm">Editar</button></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
