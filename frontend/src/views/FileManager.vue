<script setup>
import { ref, onMounted } from 'vue';
import { useFileManager } from '@/composables/useFileManager';

const {
  fileTree,
  folderList,
  selectedFile,
  selectedFolder,
  isUploading,
  isCreatingFolder,
  fetchFolders,
  fetchFiles,
  uploadFile,
  createFolder,
  openPDF,
} = useFileManager();

const onFileSelected = (event) => {
  selectedFile.value = event.target.files[0];
};

const fileInput = ref(null);
const newFolderName = ref('');
const createFolderMode = ref(false);
const showUploadModal = ref(false);
const statusMessage = ref('');
const statusType = ref(''); // 'success', 'error', or ''

const showStatus = (message, type = 'success') => {
  statusMessage.value = message;
  statusType.value = type;
  setTimeout(() => {
    statusMessage.value = '';
    statusType.value = '';
  }, 4000);
};

const openUploadModal = () => {
  showUploadModal.value = true;
};

const closeUploadModal = () => {
  showUploadModal.value = false;
  resetUploadForm();
};

const resetUploadForm = () => {
  selectedFile.value = null;
  selectedFolder.value = 'General';
  newFolderName.value = '';
  createFolderMode.value = false;
  if (fileInput.value) fileInput.value.value = '';
};

const handleUploadFile = async () => {
  if (!selectedFile.value) {
    showStatus('Por favor, selecciona un archivo.', 'error');
    return;
  }

  try {
    await uploadFile(selectedFile.value, selectedFolder.value);
    closeUploadModal();
    showStatus(`¡Archivo "${selectedFile.value.name}" subido con éxito!`, 'success');
    await fetchFiles();
  } catch (error) {
    showStatus('Error al subir el archivo.', 'error');
  }
};

const toggleCreateFolderMode = () => {
  createFolderMode.value = !createFolderMode.value;
  newFolderName.value = '';
};

const handleCreateNewFolder = async () => {
  if (!newFolderName.value.trim()) {
    showStatus('Por favor, ingresa un nombre para la carpeta.', 'error');
    return;
  }

  try {
    const result = await createFolder(newFolderName.value);
    selectedFolder.value = result.folderName;
    newFolderName.value = '';
    createFolderMode.value = false;
    showStatus(`¡Carpeta "${result.folderName}" creada con éxito!`, 'success');
    await fetchFolders();
    await fetchFiles();
  } catch (error) {
    showStatus('Error al crear la carpeta.', 'error');
  }
};

// List directories and CVs
const slugify = (text) => {
  return text
    .toString()
    .toLowerCase()
    .trim()
    .replace(/\s+/g, '-')
    .replace(/[^\w-]+/g, '');
};

onMounted(() => {
  fetchFolders();
  fetchFiles();
});
</script>

<template>
  <div class="container mt-4">
    <!-- Status Message with ARIA -->
    <div
      v-if="statusMessage"
      role="status"
      aria-live="polite"
      aria-atomic="true"
      :class="['alert mb-3', statusType === 'success' ? 'alert-success' : 'alert-danger']"
    >
      <i
        :class="[
          'bi',
          statusType === 'success' ? 'bi-check-circle me-2' : 'bi-exclamation-circle me-2',
        ]"
        aria-hidden="true"
      ></i>
      {{ statusMessage }}
    </div>

    <div class="row">
      <div class="col-12">
        <h1 class="mb-4 fs-5">
          <i class="bi bi-file-earmark-pdf" aria-hidden="true"></i> Gestión de Candidatos
        </h1>

        <div class="card shadow-sm mb-3">
          <div class="card-header bg-light d-flex justify-content-between align-items-center">
            <h2 class="mb-0 px-2 py-1 fs-6">Explorador de Candidatos</h2>
            <div class="d-flex gap-2">
              <button
                class="btn btn-sm btn-primary"
                @click="openUploadModal"
                aria-label="Subir nuevo archivo CV"
              >
                <i class="bi bi-cloud-arrow-up" aria-hidden="true"></i> Subir
              </button>
              <button
                class="btn btn-sm btn-outline-secondary"
                @click="fetchFiles"
                aria-label="Actualizar lista de archivos"
              >
                <i class="bi bi-arrow-clockwise" aria-hidden="true"></i> Actualizar
              </button>
            </div>
          </div>
          <div class="accordion accordion-flush shadow-sm border rounded" id="cvAccordion">
            <div class="accordion-item" v-for="(pdfList, folderName) in fileTree" :key="folderName">
              <h2 class="accordion-header">
                <button
                  class="accordion-button collapsed"
                  type="button"
                  data-bs-toggle="collapse"
                  :data-bs-target="'#id-' + slugify(folderName)"
                  aria-expanded="false"
                  :aria-controls="'id-' + slugify(folderName)"
                >
                  <i class="bi bi-folder-fill me-2 text-warning" aria-hidden="true"></i>
                  {{ folderName }}
                </button>
              </h2>

              <div
                :id="'id-' + slugify(folderName)"
                class="accordion-collapse collapse"
                data-bs-parent="#cvAccordion"
              >
                <div class="accordion-body p-0">
                  <ul class="list-group list-group-flush">
                    <li
                      v-for="pdfName in pdfList"
                      :key="pdfName"
                      class="list-group-item d-flex justify-content-between align-items-center py-2 px-4"
                    >
                      <div class="d-flex align-items-center">
                        <i
                          class="bi bi-file-earmark-pdf text-danger me-3 fs-5"
                          aria-hidden="true"
                        ></i>
                        <span class="">{{ pdfName }}</span>
                      </div>
                      <button
                        class="btn btn-sm btn-outline-primary rounded-pill px-3"
                        @click="openPDF(folderName, pdfName)"
                        :aria-label="'Ver currículum ' + pdfName"
                      >
                        <i class="bi bi-eye me-1" aria-hidden="true"></i> Ver
                      </button>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de Subida -->
    <div
      v-if="showUploadModal"
      class="modal fade show d-block"
      tabindex="-1"
      role="dialog"
      aria-modal="true"
      aria-labelledby="uploadModalTitle"
      style="background-color: rgba(0, 0, 0, 0.5)"
    >
      <div class="modal-dialog modal-dialog-centered" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="uploadModalTitle">
              <i class="bi bi-cloud-arrow-up me-2" aria-hidden="true"></i>Subir Currículum
            </h5>
            <button
              type="button"
              class="btn-close"
              aria-label="Cerrar"
              @click="closeUploadModal"
              :disabled="isUploading || isCreatingFolder"
            ></button>
          </div>

          <div class="modal-body">
            <!-- Selector de carpeta -->
            <div class="mb-3">
              <label v-if="!createFolderMode" for="folderSelect" class="form-label">
                <i class="bi bi-folder" aria-hidden="true"></i> Carpeta de destino
              </label>
              <label v-else for="newFolderInput" class="form-label">
                <i class="bi bi-folder" aria-hidden="true"></i> Nombre de la nueva carpeta
              </label>
              <div class="d-flex gap-2">
                <select
                  v-if="!createFolderMode"
                  v-model="selectedFolder"
                  class="form-select"
                  id="folderSelect"
                  :disabled="isUploading || isCreatingFolder"
                >
                  <option v-for="folder in folderList" :key="folder" :value="folder">
                    {{ folder }}
                  </option>
                </select>
                <input
                  v-else
                  v-model="newFolderName"
                  type="text"
                  class="form-control"
                  id="newFolderInput"
                  placeholder="Nombre de la nueva carpeta"
                  :disabled="isCreatingFolder"
                />
                <button
                  class="btn btn-outline-secondary"
                  type="button"
                  @click="toggleCreateFolderMode"
                  aria-label="Alternar creación de carpeta"
                  :disabled="isUploading || isCreatingFolder"
                >
                  <i
                    :class="createFolderMode ? 'bi bi-x-lg' : 'bi bi-plus-lg'"
                    aria-hidden="true"
                  ></i>
                </button>
                <button
                  v-if="createFolderMode"
                  class="btn btn-success"
                  type="button"
                  @click="handleCreateNewFolder"
                  :disabled="isCreatingFolder"
                >
                  <span
                    v-if="isCreatingFolder"
                    class="spinner-border spinner-border-sm me-2"
                    role="status"
                    aria-hidden="true"
                  ></span>
                  <i v-else class="bi bi-check-lg me-1" aria-hidden="true"></i>Crear
                </button>
              </div>
            </div>

            <!-- Input de archivo -->
            <div class="mb-3">
              <label class="form-label" for="cvFileInput">
                <i class="bi bi-file-pdf" aria-hidden="true"></i> Seleccionar archivo
              </label>
              <input
                type="file"
                class="form-control"
                id="cvFileInput"
                ref="fileInput"
                accept=".pdf"
                @change="onFileSelected"
                :disabled="isUploading || isCreatingFolder"
              />
              <small class="text-muted d-block mt-2">Solo archivos PDF. Máximo 10MB.</small>
              <div v-if="selectedFile" class="alert alert-info mt-2 mb-0" role="status">
                <i class="bi bi-info-circle me-2" aria-hidden="true"></i>
                <strong>Archivo seleccionado:</strong> {{ selectedFile.name }}
              </div>
            </div>
          </div>

          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              @click="closeUploadModal"
              :disabled="isUploading || isCreatingFolder"
            >
              Cancelar
            </button>
            <button
              type="button"
              class="btn btn-primary"
              @click="handleUploadFile"
              :disabled="!selectedFile || isUploading || isCreatingFolder"
            >
              <span v-if="isUploading" class="spinner-border spinner-border-sm me-2"></span>
              <i v-else class="bi bi-upload me-1"></i>
              {{ isUploading ? 'Subiendo...' : 'Subir' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
