<script setup>
import { ref, watch, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useHiringProject } from '@/composables/useHiringProject.js';
import hiringProjectsService from '@/services/hiring-projects.service.js';
import userService from '@/services/user.service.js';

const route = useRoute();
const router = useRouter();
const { project, fetchProject, deleteProject, addMember, removeMember, error } = useHiringProject();
const isLoading = ref(false);
const loadError = ref('');

const isOwner = computed(() => project.value?.current_user_role === 'OWNER');

// --- Añadir miembro ---
const orgMembers = ref([]);
const showAddMemberModal = ref(false);
const selectedUserId = ref('');
const selectedRole = ref('RECRUITER');

const availableMembers = computed(() => {
  const currentIds = new Set((project.value?.members || []).map(m => m.user_id));
  return orgMembers.value.filter(u => !currentIds.has(u.id));
});

const openAddMemberModal = async () => {
  if (orgMembers.value.length === 0) {
    orgMembers.value = await userService.getOrgMembers();
  }
  selectedUserId.value = '';
  selectedRole.value = 'RECRUITER';
  showAddMemberModal.value = true;
};

const handleAddMember = async () => {
  if (!selectedUserId.value) return;
  try {
    await addMember(route.params.projectId, {
      user_id: Number(selectedUserId.value),
      role: selectedRole.value,
    });
    showAddMemberModal.value = false;
  } catch (e) {
    // error ya en `error.value`
  }
};

const handleRemoveMember = async (member) => {
  const confirmed = confirm(`¿Quitar a ${member.username} de este proyecto?`);
  if (!confirmed) return;
  try {
    await removeMember(route.params.projectId, member.id);
  } catch (e) {
    alert(error.value || 'No se pudo eliminar al miembro.');
  }
};

// --- Borrar proyecto ---
const handleDeleteProject = async () => {
  const confirmed = confirm('¿Seguro que quieres eliminar este proyecto? Esta acción no se puede deshacer.');
  if (!confirmed) return;
  try {
    await deleteProject(route.params.projectId);
    router.push({ name: 'Hiring Projects' });
  } catch (e) {
    alert(error.value || 'No se pudo eliminar el proyecto.');
  }
};

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
              <div class="d-flex justify-content-between align-items-center mb-3">
                <h3 class="h5 fw-bold mb-0">Equipo</h3>
                <button v-if="isOwner" class="btn btn-sm btn-outline-primary" @click="openAddMemberModal">
                  <i class="bi bi-person-plus me-1"></i> Añadir
                </button>
              </div>

              <div v-if="!project.members.length" class="text-muted">No hay miembros asignados.</div>
              <ul v-else class="list-group list-group-flush">
                <li
                    v-for="member in project.members"
                    :key="member.id"
                    class="list-group-item px-0 d-flex justify-content-between align-items-center"
                >
                  <div>
                    <div class="fw-semibold">
                      {{ member.username }}
                      <span v-if="member.role === 'OWNER'" class="badge bg-primary-subtle text-primary ms-1">Owner</span>
                    </div>
                    <small class="text-muted">{{ member.email }}</small>
                  </div>

                  <button
                      v-if="isOwner || member.role !== 'OWNER'"
                      class="btn btn-sm btn-outline-danger"
                      @click="handleRemoveMember(member)"
                      title="Quitar del proyecto"
                  >
                    <i class="bi bi-x-lg"></i>
                  </button>
                </li>
              </ul>
            </div>
          </section>

          <!-- Botón eliminar proyecto, solo owner -->
          <button v-if="isOwner" class="btn btn-outline-danger btn-sm mt-2" @click="handleDeleteProject">
            <i class="bi bi-trash me-1"></i> Eliminar proyecto
          </button>

          <!-- Modal añadir miembro -->
          <div
              v-if="showAddMemberModal"
              class="modal fade show d-block"
              style="background-color: rgba(0,0,0,0.5)"
          >
            <div class="modal-dialog modal-dialog-centered">
              <div class="modal-content border-0 shadow rounded-4">
                <div class="modal-header border-0">
                  <h5 class="fw-bold mb-0">Añadir miembro</h5>
                  <button class="btn-close" @click="showAddMemberModal = false"></button>
                </div>
                <div class="modal-body">
                  <div class="mb-3">
                    <label class="form-label small fw-bold">Usuario</label>
                    <select v-model="selectedUserId" class="form-select">
                      <option value="" disabled>Selecciona un usuario</option>
                      <option v-for="u in availableMembers" :key="u.id" :value="u.id">
                        {{ u.first_name }} {{ u.last_name }} — {{ u.email }}
                      </option>
                    </select>
                  </div>
                  <div class="mb-3">
                    <label class="form-label small fw-bold">Rol</label>
                    <select v-model="selectedRole" class="form-select">
                      <option value="RECRUITER">Recruiter</option>
                      <option value="OWNER">Owner</option>
                    </select>
                  </div>
                  <div v-if="error" class="alert alert-danger py-2 small">{{ error }}</div>
                  <div class="d-grid">
                    <button class="btn btn-primary" :disabled="!selectedUserId" @click="handleAddMember">
                      Añadir
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

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
