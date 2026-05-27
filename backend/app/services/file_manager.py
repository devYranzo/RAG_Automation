import os
import shutil
from fastapi import UploadFile, HTTPException
from fastapi.responses import FileResponse
from config import settings


class FileManager:
    def __init__(self):
        self.base_storage_path = settings.PDF_PATH

    # =========================
    # PATH RESOLVER (NO SIDE EFFECTS)
    # =========================
    def _get_tenant_path(self, org_id: int) -> str:
        """Solo calcula la ruta de la organización (NO crea carpetas)."""
        if not org_id:
            raise HTTPException(
                status_code=400,
                detail="ID de organización inválido para el almacenamiento."
            )

        return os.path.join(self.base_storage_path, f"org_{org_id}")

    # =========================
    # LIFECYCLE STORAGE
    # =========================
    def create_org_storage(self, org_id: int) -> str:
        """Crea la carpeta raíz de la organización."""
        path = self._get_tenant_path(org_id)
        os.makedirs(path, exist_ok=True)
        return path

    def delete_org_storage(self, org_id: int):
        """Elimina completamente la carpeta de la organización."""
        path = self._get_tenant_path(org_id)

        if os.path.exists(path):
            shutil.rmtree(path)

    # =========================
    # FILE UPLOAD
    # =========================
    def save_upload_file(self, upload_file: UploadFile, org_id: int, folder: str = "General") -> str:
        """Guarda un archivo PDF dentro del storage de la organización."""

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
            raise HTTPException(
                status_code=500,
                detail=f"Error al guardar archivo: {str(e)}"
            )

    # =========================
    # FOLDERS
    # =========================
    def create_folder(self, folder_name: str, org_id: int) -> dict:
        """Crea una carpeta dentro de la organización."""

        if not folder_name or folder_name == "General":
            raise HTTPException(status_code=400, detail="Nombre de carpeta inválido.")

        try:
            tenant_storage = self._get_tenant_path(org_id)
            folder_path = os.path.join(tenant_storage, folder_name)
            os.makedirs(folder_path, exist_ok=True)

            return {
                "success": True,
                "message": f"Carpeta '{folder_name}' creada."
            }

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error al crear carpeta: {str(e)}"
            )

    def get_folders(self, org_id: int) -> list:
        """Lista carpetas de la organización."""
        folders = set(["General"])

        try:
            target_path = self._get_tenant_path(org_id)

            if os.path.exists(target_path):
                for item in os.listdir(target_path):
                    item_path = os.path.join(target_path, item)
                    if os.path.isdir(item_path):
                        folders.add(item)

            return sorted(list(folders))

        except Exception:
            return ["General"]

    # =========================
    # FILE TREE
    # =========================
    def get_file_tree(self, org_id: int) -> dict:
        """Devuelve estructura de PDFs por carpeta."""
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

        except Exception:
            return {}

    # =========================
    # FILE SERVING
    # =========================
    def get_pdf_file_response(self, org_id: int, folder: str, filename: str) -> FileResponse:
        """Devuelve un PDF seguro desde storage."""

        try:
            tenant_storage = self._get_tenant_path(org_id)

            if folder and folder != "General":
                file_path = os.path.join(tenant_storage, folder, filename)
            else:
                file_path = os.path.join(tenant_storage, filename)

            if not os.path.exists(file_path):
                raise HTTPException(
                    status_code=404,
                    detail="El archivo no existe o no tienes permisos."
                )

            return FileResponse(file_path, media_type="application/pdf")

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error al recuperar el archivo: {str(e)}"
            )

    def get_pdf_file_by_relative_path(self, relative_path: str, current_org_id: int) -> FileResponse:
        """Serve seguro por path relativo con validación de tenant."""

        try:
            parts = relative_path.split("/", 1)

            if not parts or not parts[0].startswith("org_"):
                raise HTTPException(status_code=400, detail="Ruta inválida.")

            org_prefix = parts[0]

            try:
                path_org_id = int(org_prefix.split("_")[1])
            except (IndexError, ValueError):
                raise HTTPException(status_code=400, detail="Ruta inválida.")

            if path_org_id != current_org_id:
                raise HTTPException(status_code=403, detail="Sin permisos.")

            file_path = os.path.join(self.base_storage_path, relative_path)

            real_path = os.path.realpath(file_path)
            real_base = os.path.realpath(self.base_storage_path)

            if not real_path.startswith(real_base):
                raise HTTPException(status_code=403, detail="Acceso denegado.")

            if not os.path.exists(file_path):
                raise HTTPException(status_code=404, detail="Archivo no existe.")

            return FileResponse(file_path, media_type="application/pdf")

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error al recuperar archivo: {str(e)}"
            )


file_manager = FileManager()
