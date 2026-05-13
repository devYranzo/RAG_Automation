import api from './client';

export default {
  async getAllUsers() {
    const response = await api.get('/users/list');
    return response.data;
  },
};
