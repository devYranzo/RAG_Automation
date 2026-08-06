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

    async createProject(payload) {
        const response = await api.post('/projects/create', payload);
        return response.data;
    },

    async updateProject(projectId, payload) {
        const response = await api.patch(`/projects/${projectId}`, payload);
        return response.data;
    },

    async deleteProject(projectId) {
        const response = await api.delete(`/projects/${projectId}`);
        return response.data;
    },

    async addMember(projectId, userId) {
        const response = await api.post(`/projects/${projectId}/members`, { user_id: userId });
        return response.data;
    },

    async removeMember(projectId, memberId) {
        const response = await api.delete(`/projects/${projectId}/members/${memberId}`);
        return response.data;
    },

    async addDocument(projectId, payload) {
        const response = await api.post(`/projects/${projectId}/documents`, payload);
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