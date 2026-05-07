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

  async logout() {
    // Limpiar token del localStorage
    localStorage.removeItem('authToken');
  },

  setToken(token) {
    localStorage.setItem('authToken', token);
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  },

  getToken() {
    return localStorage.getItem('authToken');
  },

  isAuthenticated() {
    return !!this.getToken();
  },
};
