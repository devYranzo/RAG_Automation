import api from './client';

export default {
  async login(email, password) {
    return await api.post('/auth/login', { email, password });
  },

  async register(email, password, firstName = null, lastName = null) {
    return await api.post('/auth/register', {
      email,
      password,
      first_name: firstName,
      last_name: lastName,
    });
  },

  async getCurrentUserProfile() {
    return await api.get('/profile/me');
  },
};
