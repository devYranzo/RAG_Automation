import api from './client';

export default {
  async getAllUsers() {
    const response = await api.get('/users/list');
    return response.data;
  },

  async createUser(userData) {
    const response = await api.post('/users/create', userData);
    return response.data;
  },

  async editUser(userData) {
    const { id, ...dataToUpdate } = userData;

    const response = await api.patch(`/users/edit/${id}`, dataToUpdate);
    return response.data;
  },

  async deleteUser(userId) {
    const response = await api.delete(`/users/delete/${userId}`);
    return response.data;
  },
};
