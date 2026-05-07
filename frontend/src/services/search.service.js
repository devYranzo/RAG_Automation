import api from './client';

export default {
  async buscarCandidatos(query) {
    return await api.post('/query', { question: query });
  },

  getPdfUrl(ruta) {
    const rutaLimpia = ruta.replace(/^CVs\//, '');
    return `${api.defaults.baseURL}/pdfs/${rutaLimpia}`;
  },
};
