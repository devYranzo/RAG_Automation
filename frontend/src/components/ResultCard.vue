<script setup>
import MarkdownIt from 'markdown-it';
import searchService from '@/services/search.service';
import { ref, nextTick, watch } from 'vue';

const md = new MarkdownIt({ html: true, linkify: true, breaks: true });

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

const setupCVButtons = () => {
  if (!cardBodyRef.value) return;

  const buttons = cardBodyRef.value.querySelectorAll('[data-cv-file]');
  buttons.forEach((button) => {
    // Remove existing listeners by cloning the node
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
};

const renderizarRespuesta = (texto) => {
  if (!texto) return '';
  let html = md.render(texto);
  const regex = /\[BOTON_CV:(.*?)\]/g;
  return html.replace(
    regex,
    (match, ruta) => `
      <div class="mt-2 mb-4">
        <button class="btn btn-sm btn-outline-primary shadow-sm rounded-pill px-3" data-cv-file="${ruta.trim()}" type="button">
          <i class="bi bi-file-earmark-pdf-fill me-1" aria-hidden="false"></i> Abrir Curriculum Vitae
        </button>
      </div>
    `
  );
};

// Setup buttons after content updates
const updateButtons = async () => {
  await nextTick();
  setupCVButtons();
};

// Update buttons when respuesta changes
watch(() => props.respuesta, updateButtons);

defineExpose({ updateButtons });
</script>

<template>
  <transition name="slide">
    <div v-if="respuesta" class="row justify-content-center">
      <div class="col-lg-10">
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

@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
  100% {
    transform: scale(1);
  }
}

.slide-enter-active {
  transition: all 0.5s ease-out;
}
.slide-enter-from {
  transform: translateY(30px);
  opacity: 0;
}
</style>
