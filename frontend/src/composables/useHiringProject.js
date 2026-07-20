import {ref} from "vue";
import hiringProjectsService from "@/services/hiring-projects.service.js";

export function useHiringProject() {
    const projectsList = ref([]);
    const project = ref(null);

    const fetchProjects = async () => {
        try {
            projectsList.value = await hiringProjectsService.getProjects();
        } catch (error) {
            console.error('Error al obtener los proyectos', error);
            throw error;
        }
    }

    const fetchProject = async (projectId) => {
        try {
            project.value = await hiringProjectsService.getProject(projectId);
        } catch (error) {
            console.error('Error al obtener el proyecto', error);
            throw error;
        }
    };

    return {
        projectsList,
        project,
        fetchProjects,
        fetchProject
    };
}
