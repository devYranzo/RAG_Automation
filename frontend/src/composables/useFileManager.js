import { ref } from 'vue';
import filemanagerService from '@/services/filemanager.service';
import apiClient from '@/services/client';

export function useFileManager() {
  const fileTree = ref({});
  const folderList = ref([]);
  const selectedFile = ref(null);
  const selectedFolder = ref('General');
  const isUploading = ref(false);
  const isCreatingFolder = ref(false);

  const fetchFolders = async () => {
    try {
      folderList.value = await filemanagerService.getFolders();
    } catch (error) {
      console.error('Error al obtener carpetas:', error);
      throw error;
    }
  };

  const fetchFiles = async () => {
    try {
      const data = await filemanagerService.listFiles();
      fileTree.value = data;
    } catch (error) {
      console.error('Error al obtener archivos:', error);
      throw error;
    }
  };

  const uploadFile = async (file, folder = 'General') => {
    if (!file) {
      throw new Error('Por favor, selecciona un archivo.');
    }

    isUploading.value = true;
    try {
      await filemanagerService.uploadFile(file, folder);
      await fetchFiles();
      return { success: true };
    } catch (error) {
      console.error('Error al subir el archivo:', error);
      throw error;
    } finally {
      isUploading.value = false;
    }
  };

  const createFolder = async (folderName) => {
    if (!folderName || !folderName.trim()) {
      throw new Error('Por favor, ingresa un nombre para la carpeta.');
    }

    isCreatingFolder.value = true;
    try {
      await filemanagerService.createFolder(folderName);
      await fetchFolders();
      return { success: true, folderName };
    } catch (error) {
      console.error('Error al crear la carpeta:', error);
      throw error;
    } finally {
      isCreatingFolder.value = false;
    }
  };

  const getFileUrl = (folder, fileName) => {
    const relativePath = folder === 'General' ? fileName : `${folder}/${fileName}`;
    const encodedPath = relativePath
      .split('/')
      .map((part) => encodeURIComponent(part))
      .join('/');
    return `${apiClient.defaults.baseURL}/pdfs/${encodedPath}`;
  };

  const openPDF = async (folder, fileName) => {
    try {
      await filemanagerService.viewFile(folder, fileName);
    } catch (error) {
      console.error('Error al abrir el PDF desde el composable:', error);
    }
  };

  return {
    fileTree,
    folderList,
    selectedFile,
    selectedFolder,
    isUploading,
    isCreatingFolder,
    fetchFolders,
    fetchFiles,
    uploadFile,
    createFolder,
    getFileUrl,
    openPDF,
  };
}
