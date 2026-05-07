import api from './client';

export default {
  async login(data) {
    return await api.post('/login', data);
  },
};
