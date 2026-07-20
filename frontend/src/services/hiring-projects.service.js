import api from './client';

export default {
    async getProjects() {
        const response = await api.get('/projects/list');
        return response.data;
    },

    async getProject(projectId) {
        const response = await api.get(`/projects/${projectId}`);
        return response.data;
    },

    getPdfUrl(relativePath) {
        const encodedPath = relativePath
            .split('/')
            .map((pathPart) => encodeURIComponent(pathPart))
            .join('/');

        return `${api.defaults.baseURL}/pdfs/${encodedPath}`;
    }
};
