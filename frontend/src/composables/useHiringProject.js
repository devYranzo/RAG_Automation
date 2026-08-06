import { ref } from "vue";
import hiringProjectsService from "@/services/hiring-projects.service.js";

export function useHiringProject() {
    const projectsList = ref([]);
    const project = ref(null);
    const loading = ref(false);
    const error = ref(null);

    const fetchProjects = async () => {
        try {
            projectsList.value = await hiringProjectsService.getProjects();
        } catch (err) {
            console.error('Error al obtener los proyectos', err);
            throw err;
        }
    };

    const fetchProject = async (projectId) => {
        try {
            project.value = await hiringProjectsService.getProject(projectId);
        } catch (err) {
            console.error('Error al obtener el proyecto', err);
            throw err;
        }
    };

    const createProject = async (payload) => {
        loading.value = true;
        error.value = null;
        try {
            return await hiringProjectsService.createProject(payload);
        } catch (err) {
            error.value = err.response?.data?.detail || 'No se pudo crear el proyecto.';
            throw err;
        } finally {
            loading.value = false;
        }
    };

    const updateProject = async (projectId, payload) => {
        error.value = null;
        try {
            await hiringProjectsService.updateProject(projectId, payload);
            await fetchProject(projectId);
        } catch (err) {
            error.value = err.response?.data?.detail || 'No se pudo actualizar el proyecto.';
            throw err;
        }
    };

    const deleteProject = async (projectId) => {
        error.value = null;
        try {
            await hiringProjectsService.deleteProject(projectId);
        } catch (err) {
            error.value = err.response?.data?.detail || 'No se pudo eliminar el proyecto.';
            throw err;
        }
    };

    // Fix reactividad: refetch explícito tras la mutación en vez de fiarnos
    // del objeto devuelto por el propio POST/DELETE.
    const addMember = async (projectId, userId) => {
        error.value = null;
        try {
            await hiringProjectsService.addMember(projectId, userId);
            await fetchProject(projectId);
        } catch (err) {
            error.value = err.response?.data?.detail || 'No se pudo añadir al miembro.';
            throw err;
        }
    };

    const removeMember = async (projectId, memberId) => {
        error.value = null;
        try {
            await hiringProjectsService.removeMember(projectId, memberId);
            await fetchProject(projectId);
        } catch (err) {
            error.value = err.response?.data?.detail || 'No se pudo eliminar al miembro.';
            throw err;
        }
    };

    return {
        projectsList,
        project,
        loading,
        error,
        fetchProjects,
        fetchProject,
        createProject,
        updateProject,
        deleteProject,
        addMember,
        removeMember,
    };
}