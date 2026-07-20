<script setup>
import { onMounted } from "vue";
import { useRouter } from "vue-router";
import ProjectCard from "@/components/hiring-projects/ProjectCard.vue";
import {useHiringProject} from "@/composables/useHiringProject.js";

const { projectsList: projects, fetchProjects } = useHiringProject();
const router = useRouter();

const openProject = (project) => {
  router.push({ name: 'Hiring Project Detail', params: { projectId: project.id } });
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
        <small class="text-muted">
          Manage your recruitment processes.
        </small>
      </div>

      <button class="btn btn-primary">
        <i class="bi bi-plus-lg me-2"></i>
        New Project
      </button>
    </div>

    <div class="row g-4">

      <div
          class="col-xl-4 col-lg-6"
          v-for="project in projects"
          :key="project.id"
      >
        <ProjectCard
            :project="project"
            @click="openProject(project)"
        />
      </div>
    </div>
  </div>
</template>
