<script setup>
import { ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useHiringProject } from '@/composables/useHiringProject.js';
import hiringProjectsService from '@/services/hiring-projects.service.js';

const route = useRoute();
const router = useRouter();
const { project, fetchProject } = useHiringProject();
const isLoading = ref(false);
const loadError = ref('');

const documentStatusLabel = (status) => ({
  PENDING: 'Pendiente',
  PROCESSING: 'Procesando',
  PROCESSED: 'Procesado',
  FAILED: 'Error',
}[status] || status);

const documentStatusClass = (status) => ({
  PENDING: 'bg-warning text-dark',
  PROCESSING: 'bg-info text-dark',
  PROCESSED: 'bg-success text-white',
  FAILED: 'bg-danger text-white',
}[status] || 'bg-secondary text-white');

const getDocumentUrl = (relativePath) => hiringProjectsService.getPdfUrl(relativePath);

const loadProject = async (projectId) => {
  isLoading.value = true;
  loadError.value = '';

  try {
    await fetchProject(projectId);
  } catch {
    loadError.value = 'No se ha podido cargar el proyecto.';
  } finally {
    isLoading.value = false;
  }
};

watch(
  () => route.params.projectId,
  (projectId) => loadProject(projectId),
  { immediate: true },
);
</script>

<template>
  <div class="container-fluid py-4">
    <button class="btn btn-outline-secondary mb-4" @click="router.push({ name: 'Hiring Projects' })">
      <i class="bi bi-arrow-left me-2" aria-hidden="true"></i>
      Volver a procesos
    </button>

    <div v-if="isLoading" class="text-center py-5" role="status">
      <div class="spinner-border text-primary" aria-hidden="true"></div>
      <p class="mt-3 text-muted">Cargando proyecto...</p>
    </div>

    <div v-else-if="loadError" class="alert alert-danger" role="alert">
      {{ loadError }}
    </div>

    <template v-else-if="project">
      <div class="d-flex justify-content-between align-items-start gap-3 mb-4">
        <div>
          <div class="d-flex align-items-center gap-2 mb-2">
            <h2 class="fw-bold mb-0">{{ project.title }}</h2>
            <span class="badge" :class="project.status === 'ACTIVE' ? 'bg-success' : 'bg-secondary'">
              {{ project.status }}
            </span>
          </div>
          <p class="text-muted mb-0">{{ project.description }}</p>
        </div>
      </div>

      <div class="row g-4">
        <div class="col-lg-7">
          <section class="card shadow-sm border-0 h-100">
            <div class="card-body">
              <h3 class="h5 fw-bold mb-3">Documentos</h3>
              <div v-if="!project.documents.length" class="text-muted">No hay documentos en este proyecto.</div>
              <ul v-else class="list-group list-group-flush">
                <li v-for="document in project.documents" :key="document.id" class="list-group-item px-0 d-flex justify-content-between align-items-center gap-3">
                  <a :href="getDocumentUrl(document.relative_path)" target="_blank" rel="noopener" class="link-primary text-decoration-none text-truncate">
                    <i class="bi bi-file-earmark-pdf text-danger me-2" aria-hidden="true"></i>{{ document.filename }}
                    <i class="bi bi-box-arrow-up-right ms-1 small" aria-hidden="true"></i>
                  </a>
                  <span class="badge rounded-pill px-3" :class="documentStatusClass(document.status)">
                    {{ documentStatusLabel(document.status) }}
                  </span>
                </li>
              </ul>
            </div>
          </section>
        </div>

        <div class="col-lg-5">
          <section class="card shadow-sm border-0 mb-4">
            <div class="card-body">
              <h3 class="h5 fw-bold mb-3">Equipo</h3>
              <div v-if="!project.members.length" class="text-muted">No hay miembros asignados.</div>
              <ul v-else class="list-group list-group-flush">
                <li v-for="member in project.members" :key="member.id" class="list-group-item px-0">
                  <div class="fw-semibold">{{ member.username }}</div>
                  <small class="text-muted">{{ member.email }} · {{ member.role }}</small>
                </li>
              </ul>
            </div>
          </section>

          <section class="card shadow-sm border-0">
            <div class="card-body">
              <h3 class="h5 fw-bold mb-2">Criterios de búsqueda</h3>
              <p class="mb-0 text-muted">{{ project.search_prompt || 'Sin criterios definidos.' }}</p>
            </div>
          </section>
        </div>
      </div>
    </template>
  </div>
</template>
