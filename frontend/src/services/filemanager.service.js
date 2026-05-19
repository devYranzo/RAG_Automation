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

  async viewFile(folder, filename) {
    try {
      const response = await api.get(`/filemanager/view/${folder}/${filename}`, {
        responseType: 'blob',
      });

      const blobUrl = window.URL.createObjectURL(
        new Blob([response.data], { type: 'application/pdf' })
      );

      window.open(blobUrl, '_blank');

      setTimeout(() => window.URL.revokeObjectURL(blobUrl), 1000);
    } catch (error) {
      console.error('Error al intentar visualizar el PDF:', error);
      alert('No se pudo cargar el archivo.');
    }
  },
};
