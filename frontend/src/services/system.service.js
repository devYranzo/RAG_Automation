import api from './client';

export default {
  async getStats() {
    const response = await api.get('/system/stats');
    return response.data;
  },
};
