<script setup>
import { computed } from "vue";

const props = defineProps({
  project: Object
});

const badgeClass = computed(() => {

  switch (props.project.status) {
    case "ACTIVE":
      return "bg-success";
    case "DRAFT":
      return "bg-secondary";
    case "ARCHIVED":
      return "bg-dark";
    default:
      return "bg-primary";
  }
});

const formatDate = (date) => {
  if (!date) return '';

  return new Intl.DateTimeFormat(undefined, {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(new Date(date));
};
</script>

<template>

  <div class="card shadow-sm border-0 h-100 project-card">
    <div class="card-body">
      <div class="d-flex justify-content-between">
        <h5 class="fw-semibold mb-0">
          {{ project.title }}
        </h5>

        <span
            class="badge"
            :class="badgeClass"
        >
                {{ project.status }}
            </span>
      </div>

      <p class="text-muted mt-3 mb-4 project-description">
        {{ project.description }}
      </p>

      <div class="row text-center">
        <div class="col">
          <div class="small text-muted">
            Members
          </div>

          <div class="fw-bold">
            {{ project.members_count }}
          </div>

        </div>

        <div class="col">
          <div class="small text-muted">
            Documents
          </div>

          <div class="fw-bold">
            {{ project.documents_count }}
          </div>

        </div>
      </div>
    </div>

    <div class="card-footer bg-white border-top d-flex justify-content-between">
      <small class="text-muted">
        {{ formatDate(project.updated_at) }}
      </small>

      <i class="bi bi-arrow-right"></i>

    </div>
  </div>
</template>

<style scoped>
.project-card {
  cursor: pointer;
  transition: all .2s ease;
  border-radius: 14px;
}

.project-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, .08) !important;
}

.project-description {
  height: 50px;
  overflow: hidden;
}
</style>
