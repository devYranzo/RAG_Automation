import api from './client.js';

export const analyticsService = {
  async getSummary(periodo = 30, usuarioFiltro = '') {
    try {
      const response = await api.get('/analytics/summary', {
        params: {
          periodo: periodo,
          usuario_filtro: usuarioFiltro,
        },
      });

      return response.data;
    } catch (error) {
      console.error(
        'Error en la petición de analyticsService:',
        error.response?.data || error.message
      );
      throw error;
    }
  },
};
