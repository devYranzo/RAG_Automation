import api from './client';

export default {
  async login(email, password) {
    return await api.post('/auth/login', { email, password });
  },

  async register(formData) {
    return await api.post('/auth/register', formData);
  },

  async logout() {
    await api.post('/auth/logout');
  },

  async getCurrentUserProfile() {
    return await api.get('/profile/me');
  },
};
