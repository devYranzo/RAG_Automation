import api from './client';

export default {
  async getStatus() {
    const response = await api.get('/index/status');
    return response.data;
  },

  async startIngest() {
    const response = await api.post('/index/start');
    return response.data;
  },

  async reindex() {
    const response = await api.post('/index/reindex');
    return response.data;
  },
};
