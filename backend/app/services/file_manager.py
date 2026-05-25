import os
import shutil
from fastapi import UploadFile, HTTPException
from fastapi.responses import FileResponse
from config import settings

class FileManager:
    def __init__(self):
        self.base_storage_path = settings.PDF_PATH

    def _get_tenant_path(self, org_id: int) -> str:
        """Genera y asegura la ruta raíz privada para una organización específica."""
        if not org_id:
            raise HTTPException(status_code=400, detail="ID de organización inválido para el almacenamiento.")

        tenant_path = os.path.join(self.base_storage_path, f"org_{org_id}")
        os.makedirs(tenant_path, exist_ok=True)
        return tenant_path

    def save_upload_file(self, upload_file: UploadFile, org_id: int, folder: str = "General") -> str:
        """Guarda un archivo subido en la carpeta especificada dentro del espacio de la organización."""
        filename = upload_file.filename

        if not filename:
            raise HTTPException(status_code=400, detail="El archivo no tiene nombre.")

        if not filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Solo se permiten archivos PDF.")

        try:
            tenant_storage = self._get_tenant_path(org_id)

            if folder and folder != "General":
                folder_path = os.path.join(tenant_storage, folder)
            else:
                folder_path = tenant_storage

            os.makedirs(folder_path, exist_ok=True)
            file_path = os.path.join(folder_path, filename)

            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(upload_file.file, buffer)

            return filename
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al guardar archivo: {str(e)}")

    def create_folder(self, folder_name: str, org_id: int) -> dict:
        """Crea una nueva carpeta en el almacenamiento privado de la organización."""
        if not folder_name or folder_name == "General":
            raise HTTPException(status_code=400, detail="Nombre de carpeta inválido.")

        try:
            tenant_storage = self._get_tenant_path(org_id)
            folder_path = os.path.join(tenant_storage, folder_name)
            os.makedirs(folder_path, exist_ok=True)
            return {"success": True, "message": f"Carpeta '{folder_name}' creada."}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al crear carpeta: {str(e)}")

    def get_folders(self, org_id: int) -> list:
        """Devuelve una lista de todas las carpetas del espacio privado de la organización."""
        folders = set(["General"])

        try:
            target_path = self._get_tenant_path(org_id)

            if os.path.exists(target_path):
                for item in os.listdir(target_path):
                    item_path = os.path.join(target_path, item)
                    if os.path.isdir(item_path):
                        folders.add(item)
            return sorted(list(folders))
        except Exception as e:
            return ["General"]

    def get_file_tree(self, org_id: int) -> dict:
        """Devuelve el árbol de archivos PDF aislados de la organización."""
        tree = {}

        try:
            target_path = self._get_tenant_path(org_id)

            for root, dirs, files in os.walk(target_path):
                pdfs = [f for f in files if f.lower().endswith('.pdf')]
                if pdfs:
                    rel_path = os.path.relpath(root, target_path)
                    folder_key = "General" if rel_path == "." else rel_path
                    tree[folder_key] = sorted(pdfs)
            return tree
        except Exception as e:
            return {}

    def get_pdf_file_response(self, org_id: int, folder: str, filename: str) -> FileResponse:
        """
        Busca el archivo en el almacenamiento privado del tenant
        y devuelve un FileResponse seguro listo para el navegador.
        """
        try:
            tenant_storage = self._get_tenant_path(org_id)

            if folder and folder != "General":
                file_path = os.path.join(tenant_storage, folder, filename)
            else:
                file_path = os.path.join(tenant_storage, filename)

            if not os.path.exists(file_path):
                raise HTTPException(
                    status_code=404,
                    detail="El archivo no existe o no tienes permisos para visualizarlo."
                )

            return FileResponse(file_path, media_type="application/pdf")

        except HTTPException as he:
            raise he
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al recuperar el archivo: {str(e)}")

    def get_pdf_file_by_relative_path(self, relative_path: str, current_org_id: int) -> FileResponse:
        """
        Serve PDF files using relative paths like org_1/filename.pdf or org_1/folder/filename.pdf
        Validates that the current user has access to the organization in the path.
        """
        try:
            # Parse the org_id from the path
            path_parts = relative_path.split("/", 1)
            if not path_parts or not path_parts[0].startswith("org_"):
                raise HTTPException(
                    status_code=400,
                    detail="Ruta de archivo inválida."
                )

            org_prefix = path_parts[0]
            try:
                path_org_id = int(org_prefix.split("_")[1])
            except (IndexError, ValueError):
                raise HTTPException(
                    status_code=400,
                    detail="Ruta de archivo inválida."
                )

            # Verify that the current user has access to this organization
            if path_org_id != current_org_id:
                raise HTTPException(
                    status_code=403,
                    detail="No tienes permisos para acceder a este archivo."
                )

            # Construct the full file path
            base_storage_path = self.base_storage_path
            file_path = os.path.join(base_storage_path, relative_path)

            # Security check: ensure the resolved path is within the storage directory
            real_path = os.path.realpath(file_path)
            real_storage = os.path.realpath(base_storage_path)
            if not real_path.startswith(real_storage):
                raise HTTPException(
                    status_code=403,
                    detail="Acceso denegado."
                )

            if not os.path.exists(file_path):
                raise HTTPException(
                    status_code=404,
                    detail="El archivo no existe."
                )

            return FileResponse(file_path, media_type="application/pdf")

        except HTTPException as he:
            raise he
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al recuperar el archivo: {str(e)}")

file_manager = FileManager()
