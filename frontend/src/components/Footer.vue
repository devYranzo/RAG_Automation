<script setup>
import { ref, computed } from 'vue';
import { marked } from 'marked';
import DOMPurify from 'dompurify';

const currentYear = computed(() => new Date().getFullYear());

const tabActiva = ref('terminos');
const cargando = ref(false);

const documentosCache = ref({
  terminos: null,
  privacidad: null,
  cookies: null,
});

const secciones = [
  {
    id: 'terminos',
    titulo: 'Términos y Condiciones',
    icon: 'bi-file-text',
    archivo: '/legal/terms.md',
  },
  {
    id: 'privacidad',
    titulo: 'Tratamiento de Datos',
    icon: 'bi-shield-lock',
    archivo: '/legal/privacy.md',
  },
  {
    id: 'cookies',
    titulo: 'Política de Cookies',
    icon: 'bi-cookie',
    archivo: '/legal/cookies.md',
  },
];

const contenidoRenderizado = computed(() => {
  const markdown = documentosCache.value[tabActiva.value] || '';
  return DOMPurify.sanitize(marked.parse(markdown));
});

async function cargarDocumento(seccionId) {
  if (documentosCache.value[seccionId]) return;

  const seccion = secciones.find((s) => s.id === seccionId);
  if (!seccion) return;

  cargando.value = true;

  try {
    const response = await fetch(seccion.archivo);
    if (!response.ok) throw new Error(`No se pudo cargar ${seccion.archivo}`);

    documentosCache.value[seccionId] = await response.text();
  } catch (error) {
    documentosCache.value[seccionId] = `
# Error de carga

No fue posible cargar el documento legal.

**Detalle técnico:** ${error.message}
`;
  } finally {
    cargando.value = false;
  }
}
</script>

<template>
  <footer class="footer mt-auto py-3">
    <div class="container px-4">
      <div class="row align-items-center justify-content-between g-2 small">
        <div class="col-12 col-md-auto text-center text-md-start text-muted">
          <span> &copy; {{ currentYear }} Talent Finder. Todos los derechos reservados. </span>
        </div>

        <div class="col-12 col-md-auto text-center text-md-end">
          <div class="d-flex flex-wrap justify-content-center justify-content-md-end gap-3">
            <!-- TERMINOS -->
            <a
              href="#"
              class="text-secondary link-success text-decoration-none"
              data-bs-toggle="modal"
              data-bs-target="#legalModal"
              @click="
                tabActiva = 'terminos';
                cargarDocumento('terminos');
              "
            >
              Términos y Condiciones
            </a>

            <span class="text-black-50">|</span>

            <!-- PRIVACIDAD -->
            <a
              href="#"
              class="text-secondary link-success text-decoration-none"
              data-bs-toggle="modal"
              data-bs-target="#legalModal"
              @click="
                tabActiva = 'privacidad';
                cargarDocumento('privacidad');
              "
            >
              Tratamiento de Datos
            </a>

            <span class="text-black-50">|</span>

            <!-- COOKIES -->
            <a
              href="#"
              class="text-secondary link-success text-decoration-none"
              data-bs-toggle="modal"
              data-bs-target="#legalModal"
              @click="
                tabActiva = 'cookies';
                cargarDocumento('cookies');
              "
            >
              Política de Cookies
            </a>
          </div>
        </div>
      </div>
    </div>

    <!-- MODAL BOOTSTRAP NATIVO -->
    <div class="modal fade" id="legalModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-xl modal-dialog-centered modal-dialog-scrollable">
        <div class="modal-content border-0 shadow-lg rounded-4">
          <!-- HEADER -->
          <div class="modal-header bg-light border-bottom py-3">
            <h5 class="modal-title fw-bold">
              <i class="bi bi-shield-check text-success me-2"></i>
              Centro Legal y Cumplimiento
            </h5>

            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Cerrar"
            ></button>
          </div>

          <!-- BODY -->
          <div class="modal-body p-0">
            <div class="row g-0" style="min-height: 550px">
              <!-- SIDEBAR -->
              <div class="col-md-3 bg-light border-end p-3">
                <div class="nav flex-column nav-pills gap-2">
                  <button
                    v-for="tab in secciones"
                    :key="tab.id"
                    @click="
                      tabActiva = tab.id;
                      cargarDocumento(tab.id);
                    "
                    :class="[
                      'nav-link text-start border-0 rounded-3 py-2 px-3 small fw-medium',
                      tabActiva === tab.id
                        ? 'bg-primary text-white'
                        : 'bg-transparent text-secondary',
                    ]"
                  >
                    <i :class="['bi', tab.icon, 'me-2']"></i>
                    {{ tab.titulo }}
                  </button>
                </div>
              </div>

              <!-- CONTENT -->
              <div class="col-md-9 bg-white p-4" style="max-height: 600px; overflow-y: auto">
                <div v-if="cargando" class="text-center py-5 text-muted">
                  <div class="spinner-border spinner-border-sm text-success me-2"></div>
                  Cargando documentación legal...
                </div>

                <div v-else v-html="contenidoRenderizado"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>

<style scoped></style>
