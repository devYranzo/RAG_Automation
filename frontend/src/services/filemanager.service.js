import api from './client';

export default {
  async listFiles() {
    const response = await api.get('/filemanager/list');
    return response.data;
  },

  async getFolders() {
    const response = await api.get('/filemanager/folders');
    return response.data.folders;
  },

  async uploadFile(file, folder = 'General') {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('folder', folder);

    const response = await api.post('/filemanager/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });

    return response.data;
  },

  async createFolder(folderName) {
    const formData = new FormData();
    formData.append('folder_name', folderName);

    const response = await api.post('/filemanager/create-folder', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });

    return response.data;
  },
};
