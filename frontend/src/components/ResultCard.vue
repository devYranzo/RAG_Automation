<script setup>
import MarkdownIt from 'markdown-it';
import DOMPurify from 'dompurify';
import searchService from '@/services/search.service';
import hiringProjectsService from '@/services/hiring-projects.service';
import { useAuthStore } from '@/stores/authStore';
import { ref, nextTick, watch } from 'vue';

const md = new MarkdownIt({ html: false, linkify: true, breaks: true });
const authStore = useAuthStore();

const props = defineProps({
  respuesta: String,
  copiado: Boolean,
});

defineEmits(['copiar']);

const cardBodyRef = ref(null);
const openPdfMessage = ref('');

const abrirArchivoCV = (ruta) => {
  const url = searchService.getPdfUrl(ruta);
  window.open(url, '_blank');
  openPdfMessage.value = `Abriendo CV: ${ruta}`;
  setTimeout(() => {
    openPdfMessage.value = '';
  }, 3000);
};

// --- Añadir candidato a un hiring project ---
const projectsList = ref([]);
const showAddCandidateModal = ref(false);
const candidateFilePath = ref('');
const selectedProjectId = ref('');
const addCandidateError = ref('');
const addCandidateSuccess = ref('');

const loadProjectsIfNeeded = async () => {
  if (!authStore.requireAtLeastRecruiter) return;
  if (projectsList.value.length > 0) return;
  try {
    projectsList.value = await hiringProjectsService.getProjects();
  } catch (error) {
    console.error('Error al cargar hiring projects:', error);
  }
};

const abrirModalAgregarCandidato = async (ruta) => {
  candidateFilePath.value = ruta;
  selectedProjectId.value = '';
  addCandidateError.value = '';
  await loadProjectsIfNeeded();
  showAddCandidateModal.value = true;
};

const confirmarAgregarCandidato = async () => {
  if (!selectedProjectId.value) return;
  addCandidateError.value = '';
  try {
    await hiringProjectsService.addDocument(selectedProjectId.value, {
      relative_path: candidateFilePath.value,
    });
    showAddCandidateModal.value = false;
    addCandidateSuccess.value = 'Candidato añadido al proyecto.';
    setTimeout(() => {
      addCandidateSuccess.value = '';
    }, 3000);
  } catch (error) {
    addCandidateError.value = error.response?.data?.detail || 'No se pudo añadir el candidato.';
  }
};

const setupCVButtons = () => {
  if (!cardBodyRef.value) return;

  // Botones "Abrir CV"
  const cvButtons = cardBodyRef.value.querySelectorAll('[data-cv-file]');
  cvButtons.forEach((button) => {
    const newButton = button.cloneNode(true);
    const file = newButton.getAttribute('data-cv-file');

    newButton.addEventListener('click', () => abrirArchivoCV(file));
    newButton.addEventListener('keypress', (e) => {
      if (e.key === 'Enter' || e.code === 'Space') {
        e.preventDefault();
        abrirArchivoCV(file);
      }
    });

    button.parentNode.replaceChild(newButton, button);
  });

  // Botones "Añadir a proyecto"
  const addButtons = cardBodyRef.value.querySelectorAll('[data-add-candidate]');
  addButtons.forEach((button) => {
    const newButton = button.cloneNode(true);
    const file = newButton.getAttribute('data-add-candidate');

    newButton.addEventListener('click', () => abrirModalAgregarCandidato(file));
    newButton.addEventListener('keypress', (e) => {
      if (e.key === 'Enter' || e.code === 'Space') {
        e.preventDefault();
        abrirModalAgregarCandidato(file);
      }
    });

    button.parentNode.replaceChild(newButton, button);
  });
};

const renderizarRespuesta = (texto) => {
  if (!texto) return '';
  let html = md.render(texto);
  const regex = /\[BOTON_CV:(.*?)\]/g;
  const puedeAgregarCandidatos = authStore.requireAtLeastRecruiter;

  const htmlWithButtons = html.replace(regex, (match, ruta) => {
    const rutaLimpia = ruta.trim();
    const botonAgregar = puedeAgregarCandidatos
        ? `
        <button class="btn btn-sm btn-outline-success shadow-sm rounded-pill px-3" data-add-candidate="${rutaLimpia}" type="button">
          <i class="bi bi-person-plus-fill me-1" aria-hidden="true"></i> Añadir a proyecto
        </button>
      `
        : '';

    return `
      <div class="mt-2 mb-4 d-flex gap-2 flex-wrap">
        <button class="btn btn-sm btn-outline-primary shadow-sm rounded-pill px-3" data-cv-file="${rutaLimpia}" type="button">
          <i class="bi bi-file-earmark-pdf-fill me-1" aria-hidden="true"></i> Abrir Curriculum Vitae
        </button>
        ${botonAgregar}
      </div>
    `;
  });

  return DOMPurify.sanitize(htmlWithButtons, {
    ADD_ATTR: ['data-cv-file', 'data-add-candidate'],
  });
};

const updateButtons = async () => {
  await nextTick();
  setupCVButtons();
};

watch(() => props.respuesta, updateButtons);

defineExpose({ updateButtons });
</script>

<template>
  <transition name="slide">
    <div v-if="respuesta" class="row justify-content-center">
      <div class="col-lg-10">
        <div v-if="addCandidateSuccess" class="alert alert-success py-2 mb-2" role="status">
          <i class="bi bi-check-circle me-2"></i>{{ addCandidateSuccess }}
        </div>

        <div class="card shadow-lg border-0 rounded-4 overflow-hidden result-card mb-5">
          <div
              class="card-header bg-primary text-white py-3 px-4 d-flex align-items-center justify-content-between"
          >
            <div class="d-flex align-items-center">
              <i class="bi bi-stars fs-4 me-2" aria-hidden="true"></i>
              <h2 class="mb-0 fw-bold fs-5">Top 5 Mejores Candidatos</h2>
            </div>

            <button
                @click="$emit('copiar')"
                :aria-label="
                copiado
                  ? 'Resultados copiados al portapapeles'
                  : 'Copiar resultados al portapapeles'
              "
                class="btn btn-sm btn-light rounded-pill px-3 fw-bold shadow-sm d-flex align-items-center"
                :class="{ 'btn-success text-white': copiado }"
            >
              <i
                  :class="['bi me-2', copiado ? 'bi-check-lg' : 'bi-clipboard-plus']"
                  aria-hidden="true"
              ></i>
              {{ copiado ? '¡Copiado!' : 'Copiar' }}
            </button>
          </div>

          <div class="card-body p-4 px-md-5" ref="cardBodyRef">
            <div aria-live="polite" aria-atomic="true" class="visually-hidden">
              {{ openPdfMessage }}
            </div>
            <div
                class="markdown-body"
                v-html="renderizarRespuesta(respuesta)"
                @update="updateButtons"
            ></div>
          </div>
        </div>
      </div>
    </div>
  </transition>

  <!-- Modal: añadir candidato a hiring project -->
  <div
      v-if="showAddCandidateModal"
      class="modal fade show d-block"
      tabindex="-1"
      role="dialog"
      style="background-color: rgba(0, 0, 0, 0.5)"
  >
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content border-0 shadow rounded-4">
        <div class="modal-header border-0">
          <h5 class="fw-bold mb-0">Añadir candidato al proyecto</h5>
          <button type="button" class="btn-close" @click="showAddCandidateModal = false"></button>
        </div>
        <div class="modal-body">
          <p class="text-muted small mb-3">
            <i class="bi bi-file-earmark-pdf text-danger me-1"></i>{{ candidateFilePath }}
          </p>

          <div v-if="projectsList.length === 0" class="alert alert-warning py-2 small mb-0">
            No perteneces a ningún hiring project todavía.
          </div>

          <div v-else class="mb-3">
            <label class="form-label small fw-bold">Hiring Project</label>
            <select v-model="selectedProjectId" class="form-select">
              <option value="" disabled>Selecciona un proyecto</option>
              <option v-for="p in projectsList" :key="p.id" :value="p.id">
                {{ p.title }}
              </option>
            </select>
          </div>

          <div v-if="addCandidateError" class="alert alert-danger py-2 small">
            {{ addCandidateError }}
          </div>

          <div v-if="projectsList.length > 0" class="d-grid">
            <button
                class="btn btn-primary"
                :disabled="!selectedProjectId"
                @click="confirmarAgregarCandidato"
            >
              Añadir candidato
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.markdown-body:deep(h3) {
  font-size: 1.4rem;
  color: #0d6efd;
  border-bottom: 2px solid #f0f4f8;
  padding-bottom: 0.5rem;
  margin-top: 2rem;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
}

.markdown-body:deep(h3::before) {
  content: 'Candidato';
  font-size: 0.7rem;
  text-transform: uppercase;
  background: #0d6efd;
  color: white;
  padding: 2px 8px;
  border-radius: 4px;
  margin-right: 10px;
}

.markdown-body:deep(ul) {
  padding-left: 1.2rem;
  margin-bottom: 1.5rem;
}

.markdown-body:deep(li) {
  margin-bottom: 0.4rem;
  position: relative;
}

.slide-enter-active {
  transition: all 0.5s ease-out;
}
.slide-enter-from {
  transform: translateY(30px);
  opacity: 0;
}
</style>