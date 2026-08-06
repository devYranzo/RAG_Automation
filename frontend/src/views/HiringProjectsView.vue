<script setup>
import { onMounted, ref, reactive } from "vue";
import { useRouter } from "vue-router";
import ProjectCard from "@/components/hiring-projects/ProjectCard.vue";
import { useHiringProject } from "@/composables/useHiringProject.js";

const { projectsList: projects, fetchProjects, createProject, loading, error } = useHiringProject();
const router = useRouter();

const showCreateModal = ref(false);
const form = reactive({ title: '', description: '', search_prompt: '' });

const openProject = (project) => {
  router.push({ name: 'Hiring Project Detail', params: { projectId: project.id } });
};

const openCreateModal = () => {
  form.title = '';
  form.description = '';
  form.search_prompt = '';
  showCreateModal.value = true;
};

const handleCreate = async () => {
  if (!form.title.trim()) return;
  try {
    const created = await createProject({ ...form });
    showCreateModal.value = false;
    await fetchProjects();
    router.push({ name: 'Hiring Project Detail', params: { projectId: created.id } });
  } catch (e) {
    // el error ya queda en `error.value`
  }
};

onMounted(async () => {
  await fetchProjects();
});
</script>

<template>
  <div class="container-fluid py-4">

    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h3 class="fw-bold mb-1">Hiring Projects</h3>
        <small class="text-muted">Manage your recruitment processes.</small>
      </div>

      <button class="btn btn-primary" @click="openCreateModal">
        <i class="bi bi-plus-lg me-2"></i>
        New Project
      </button>
    </div>

    <div class="row g-4">
      <div class="col-xl-4 col-lg-6" v-for="project in projects" :key="project.id">
        <ProjectCard :project="project" @click="openProject(project)" />
      </div>
    </div>

    <!-- MODAL DE CREACIÓN -->
    <div
        v-if="showCreateModal"
        class="modal fade show d-block"
        tabindex="-1"
        role="dialog"
        style="background-color: rgba(0, 0, 0, 0.5)"
    >
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 shadow rounded-4">
          <div class="modal-header border-0">
            <h5 class="fw-bold mb-0">Nuevo Hiring Project</h5>
            <button type="button" class="btn-close" @click="showCreateModal = false"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="handleCreate">
              <div class="mb-3">
                <label class="form-label small fw-bold">Título</label>
                <input v-model="form.title" class="form-control" required autofocus />
              </div>
              <div class="mb-3">
                <label class="form-label small fw-bold">Descripción</label>
                <textarea v-model="form.description" class="form-control" rows="3"></textarea>
              </div>
              <div class="mb-3">
                <label class="form-label small fw-bold">Criterios de búsqueda</label>
                <textarea v-model="form.search_prompt" class="form-control" rows="2"
                          placeholder="Ej: Python FastAPI PostgreSQL Docker"></textarea>
              </div>

              <div v-if="error" class="alert alert-danger py-2 small">{{ error }}</div>

              <div class="d-grid mt-4">
                <button type="submit" class="btn btn-primary" :disabled="loading">
                  {{ loading ? 'Creando...' : 'Crear proyecto' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>