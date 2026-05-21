<template>
  <div>
    <div class="d-flex align-items-center gap-2 mb-4">
      <span class="text-muted small">Período:</span>
      <select class="form-select form-select-sm w-auto" v-model="periodo" @change="cargarDatos">
        <option value="7">Últimos 7 días</option>
        <option value="30">Últimos 30 días</option>
        <option value="90">Últimos 90 días</option>
      </select>
      <select
        class="form-select form-select-sm w-auto"
        v-model="filtroUsuario"
        @change="cargarDatos"
      >
        <option value="">Todos los usuarios</option>
        <option v-for="u in usuarios" :key="u.id" :value="u.nombre">{{ u.nombre }}</option>
      </select>
      <button class="btn btn-sm btn-outline-secondary ms-auto" @click="cargarDatos">
        <i class="bi bi-arrow-clockwise me-1"></i>Actualizar
      </button>
    </div>

    <div class="row g-3 mb-4">
      <div class="col-6 col-md-3" v-for="m in metricas" :key="m.label">
        <div class="bg-light rounded-3 p-3 shadow-sm h-100 border-0">
          <div class="text-muted small mb-1">
            <i :class="['bi', m.icon, 'me-1']"></i>{{ m.label }}
          </div>
          <div class="fs-4 fw-bold text-dark lh-sm">{{ m.valor }}</div>
          <div class="small mt-1" :class="m.deltaPositivo ? 'text-success' : 'text-danger'">
            {{ m.delta }}
          </div>
        </div>
      </div>
    </div>

    <div class="row g-3 mb-4">
      <div class="col-md-7">
        <div class="bg-light rounded-3 p-4 shadow-sm h-100 border-0">
          <div class="fs-6 fw-bold text-dark mb-3">
            <i class="bi bi-bar-chart me-2"></i>Búsquedas por día
          </div>
          <div style="position: relative; height: 160px"><canvas ref="refVolumen"></canvas></div>
        </div>
      </div>
      <div class="col-md-5">
        <div class="bg-light rounded-3 p-4 shadow-sm h-100 border-0">
          <div class="fs-6 fw-bold text-dark mb-3">
            <i class="bi bi-pie-chart me-2"></i>Tipo de query
          </div>
          <div class="d-flex align-items-center gap-3">
            <div style="position: relative; width: 120px; height: 120px; flex-shrink: 0">
              <canvas ref="refTipo"></canvas>
            </div>
            <div class="d-flex flex-column gap-2 w-100 small">
              <div
                v-for="i in tipoQueryData"
                :key="i.label"
                class="d-flex align-items-center gap-2"
              >
                <span
                  class="rounded-1"
                  :style="{ background: i.color, width: '10px', height: '10px', flexShrink: 0 }"
                ></span>
                <span class="text-secondary flex-grow-1 text-truncate">{{ i.label }}</span>
                <span class="fw-bold text-dark">{{ i.pct }}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="bg-light rounded-3 p-4 shadow-sm mb-4 border-0">
      <div class="d-flex justify-content-between align-items-center mb-3">
        <div class="fs-6 fw-bold text-dark mb-0">
          <i class="bi bi-graph-up me-2"></i>Queries más frecuentes
        </div>
        <input
          v-model="busquedaFiltro"
          class="form-control form-control-sm w-auto"
          placeholder="Filtrar queries..."
          style="max-width: 180px"
        />
      </div>
      <div class="table-responsive">
        <table class="table table-hover align-middle mb-0 small">
          <thead
            class="table-light text-uppercase text-muted"
            style="font-size: 11px; letter-spacing: 0.04em"
          >
            <tr>
              <th
                v-for="h in ['Query', 'Habilidades', 'Búsquedas', 'Latencia', 'Caché', 'Última']"
                :key="h"
                @click="
                  h === 'Query'
                    ? sortBy('query')
                    : h === 'Búsquedas'
                      ? sortBy('count')
                      : h === 'Latencia'
                        ? sortBy('score')
                        : null
                "
                :class="[
                  'py-2',
                  {
                    'text-center': h !== 'Query' && h !== 'Habilidades',
                    'pointer-event': h === 'Query' || h === 'Búsquedas' || h === 'Latencia',
                  },
                ]"
                style="cursor: pointer; user-select: none"
              >
                {{ h }}
                <i
                  v-if="['Query', 'Búsquedas', 'Latencia'].includes(h)"
                  class="bi bi-chevron-expand ms-1 text-muted"
                ></i>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="q in queriesFiltradas" :key="q.id">
              <td>
                <div class="fw-semibold text-dark text-truncate" style="max-width: 260px">
                  {{ q.query }}
                </div>
                <div class="text-muted extra-small" style="font-size: 11px">{{ q.usuario }}</div>
              </td>
              <td>
                <span
                  v-for="tag in q.skills.slice(0, 3)"
                  :key="tag"
                  class="badge bg-success-subtle text-success border border-success-subtle rounded-pill me-1 px-2 py-1"
                  style="font-size: 11px; font-weight: 500"
                  >{{ tag }}</span
                >
                <span
                  v-if="q.skills.length > 3"
                  class="badge bg-light text-secondary rounded-pill px-2 py-1"
                  style="font-size: 11px"
                  >+{{ q.skills.length - 3 }}</span
                >
              </td>
              <td class="text-center fw-semibold text-dark">{{ q.count }}</td>
              <td class="text-center text-muted fw-semibold">{{ q.score.toFixed(2) }}s</td>
              <td class="text-center">
                <span
                  :class="[
                    'badge rounded-pill px-2 py-1',
                    q.cached ? 'bg-success-subtle text-success' : 'bg-light text-secondary',
                  ]"
                  style="font-size: 11px; font-weight: 500"
                  >{{ q.cached ? 'Sí' : 'No' }}</span
                >
              </td>
              <td class="text-center text-muted" style="font-size: 12px">{{ q.ultima }}</td>
            </tr>
            <tr v-if="queriesFiltradas.length === 0">
              <td colspan="6" class="text-center text-muted py-4">
                Sin resultados en este período
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="row g-3">
      <div class="col-md-5">
        <div class="bg-light rounded-3 p-4 shadow-sm h-100 border-0">
          <div class="fs-6 fw-bold text-dark mb-3">
            <i class="bi bi-cpu me-2"></i>Balance de Tokens (Uso)
          </div>
          <div class="d-flex align-items-center gap-4 pb-2">
            <div style="position: relative; width: 120px; height: 120px; flex-shrink: 0">
              <canvas ref="refTokensChart"></canvas>
            </div>
            <div class="d-flex flex-column gap-2 w-100 small">
              <div
                v-for="t in [
                  { l: 'Entrada:', v: tokensUsoData.input, c: '#378ADD' },
                  { l: 'Salida:', v: tokensUsoData.output, c: '#1a6f3c' },
                ]"
                :key="t.l"
                class="d-flex align-items-center gap-2"
              >
                <span
                  class="rounded-1"
                  :style="{ background: t.c, width: '10px', height: '10px' }"
                ></span>
                <span class="text-secondary flex-grow-1">{{ t.l }}</span>
                <span class="fw-bold text-dark text-end">{{ t.v.toLocaleString() }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-7">
        <div class="bg-light rounded-3 p-4 shadow-sm h-100 border-0">
          <div class="fs-6 fw-bold text-dark mb-3">
            <i class="bi bi-activity me-2"></i>Actividad reciente
          </div>
          <div class="d-flex flex-column">
            <div
              v-for="a in actividad"
              :key="a.id"
              class="d-flex align-items-center gap-3 py-2 border-bottom border-light"
            >
              <div
                class="rounded-circle bg-success-subtle text-success d-flex align-items-center justify-content-center fw-bold fs-6"
                style="width: 32px; height: 32px; font-size: 11px; flex-shrink: 0"
              >
                {{ initials(a.usuario) }}
              </div>
              <div class="flex-grow-1 min-w-0">
                <div class="text-dark fw-semibold text-truncate small">{{ a.query }}</div>
                <div class="text-muted extra-small text-truncate" style="font-size: 11px">
                  {{ a.usuario }} · {{ a.hace }} · {{ a.resultados }} candidatos
                </div>
              </div>
              <span class="text-muted small fw-semibold flex-shrink-0"
                >{{ a.score.toFixed(2) }}s</span
              >
            </div>
            <div v-if="actividad.length === 0" class="text-center text-muted py-4 small">
              No hay actividad reciente registrada
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onActivated, onDeactivated, nextTick } from 'vue';
import Chart from 'chart.js/auto';
import { analyticsService } from '@/services/analytics.service.js';

const periodo = ref('30');
const filtroUsuario = ref('');
const busquedaFiltro = ref('');
const sortKey = ref('count');
const sortDir = ref(-1);

const refVolumen = ref(null);
const refTipo = ref(null);
const refTokensChart = ref(null);

let chartVolumen = null;
let chartTipo = null;
let chartTokens = null;

const usuarios = ref([]);
const metricas = ref([]);
const tipoQueryData = ref([]);
const queries = ref([]);
const actividad = ref([]);
const volumenDiario = ref({ labels: [], data: [] });
const tokensUsoData = ref({ input: 0, output: 0 });

const queriesFiltradas = computed(() => {
  let lista = queries.value || [];
  if (busquedaFiltro.value) {
    const q = busquedaFiltro.value.toLowerCase();
    lista = lista.filter((i) => i.query?.toLowerCase().includes(q));
  }
  return [...lista].sort((a, b) => sortDir.value * (a[sortKey.value] > b[sortKey.value] ? 1 : -1));
});

const initials = (n) =>
  n
    ? n
        .split(' ')
        .map((p) => p[0])
        .slice(0, 2)
        .join('')
        .toUpperCase()
    : 'US';
const sortBy = (k) => {
  if (sortKey.value === k) sortDir.value *= -1;
  else {
    sortKey.value = k;
    sortDir.value = -1;
  }
};

function destruirGraficos() {
  chartVolumen?.destroy();
  chartTipo?.destroy();
  chartTokens?.destroy();
}

function iniciarGraficos() {
  destruirGraficos();
  if (!refVolumen.value || !refTipo.value || !refTokensChart.value) return;

  const tieneVol = volumenDiario.value?.labels?.length > 0;
  chartVolumen = new Chart(refVolumen.value, {
    type: 'line',
    data: {
      labels: tieneVol ? volumenDiario.value.labels : ['Sin datos'],
      datasets: [
        {
          data: tieneVol ? volumenDiario.value.data : [0],
          backgroundColor: '#0d6efd',
          borderRadius: 4,
          barPercentage: 0.6,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: { x: { grid: { display: false } }, y: { grid: { color: 'rgba(0,0,0,0.04)' } } },
    },
  });

  const tieneTipos = tipoQueryData.value?.length > 0;
  chartTipo = new Chart(refTipo.value, {
    type: 'doughnut',
    data: {
      labels: tieneTipos ? tipoQueryData.value.map((i) => i.label) : ['Sin datos'],
      datasets: [
        {
          data: tieneTipos ? tipoQueryData.value.map((i) => i.pct) : [100],
          backgroundColor: tieneTipos ? tipoQueryData.value.map((i) => i.color) : ['#f0f0f0'],
          borderWidth: 0,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: '70%',
      plugins: { legend: { display: false } },
    },
  });

  const totalT = tokensUsoData.value.input + tokensUsoData.value.output;
  chartTokens = new Chart(refTokensChart.value, {
    type: 'doughnut',
    data: {
      labels: ['Tokens Entrada', 'Tokens Salida'],
      datasets: [
        {
          data: totalT > 0 ? [tokensUsoData.value.input, tokensUsoData.value.output] : [1, 0],
          backgroundColor: totalT > 0 ? ['#378ADD', '#1a6f3c'] : ['#f0f0f0'],
          borderWidth: 0,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: '70%',
      plugins: { legend: { display: false } },
    },
  });
}

async function cargarDatos() {
  try {
    const data = await analyticsService.getSummary(periodo.value, filtroUsuario.value);
    metricas.value = data.metricas || [];
    volumenDiario.value = data.volumenDiario || { labels: ['Sin datos'], data: [0] };
    tipoQueryData.value = data.tipoQueryData || [];
    queries.value = data.queries || [];
    actividad.value = data.actividad || [];
    if (data.tokensUso) tokensUsoData.value = data.tokensUso;
    if (data.usuarios) usuarios.value = data.usuarios;
    await nextTick();
    iniciarGraficos();
  } catch (e) {
    console.error('Error cargando analíticas:', e);
  }
}

onMounted(() => {
  cargarDatos();
});
onActivated(() => {
  nextTick().then(iniciarGraficos);
});
onDeactivated(() => {
  destruirGraficos();
});
</script>
