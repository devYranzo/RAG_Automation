import api from './client';

export default {
  async login(email, password) {
    return await api.post('/auth/login', { email, password });
  },

  async register(formData) {
    return await api.post('/auth/register-company', formData);
  },

  async logout() {
    await api.post('/auth/logout');
  },

  async getCurrentUserProfile() {
    return await api.get('/profile/me');
  },

  async changePassword(currentPassword, newPassword) {
    return await api.post('/auth/change-password', {
      current_password: currentPassword,
      new_password: newPassword,
    });
  },
};
