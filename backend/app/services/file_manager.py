import os
import shutil
from pathlib import Path

from fastapi import HTTPException, UploadFile
from fastapi.responses import FileResponse

from config import settings


class FileManager:
    def __init__(self):
        self.base_storage_path = Path(settings.PDF_PATH).resolve()
        self.max_pdf_upload_size = settings.MAX_PDF_UPLOAD_SIZE_MB * 1024 * 1024

    def _validate_path_segment(self, value: str | None, field_name: str) -> str:
        safe_value = (value or "").strip()

        if (
            not safe_value
            or safe_value in {".", ".."}
            or "/" in safe_value
            or "\\" in safe_value
            or Path(safe_value).name != safe_value
        ):
            raise HTTPException(status_code=400, detail=f"{field_name} invalido.")

        return safe_value

    def _validate_pdf_filename(self, filename: str | None) -> str:
        safe_filename = self._validate_path_segment(filename, "Nombre de archivo")

        if not safe_filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Solo se permiten archivos PDF.")

        return safe_filename

    def _validate_pdf_content_type(self, upload_file: UploadFile):
        allowed_content_types = {"application/pdf", "application/x-pdf"}

        if upload_file.content_type not in allowed_content_types:
            raise HTTPException(status_code=400, detail="El archivo debe ser un PDF valido.")

    def _resolve_inside(self, base_path: Path, *parts: str) -> Path:
        resolved_base = base_path.resolve()
        resolved_path = resolved_base.joinpath(*parts).resolve()

        try:
            resolved_path.relative_to(resolved_base)
        except ValueError:
            raise HTTPException(status_code=403, detail="Acceso denegado.")

        return resolved_path

    # =========================
    # PATH RESOLVER (NO SIDE EFFECTS)
    # =========================
    def _get_tenant_path(self, org_id: int) -> Path:
        """Solo calcula la ruta de la organizacion (NO crea carpetas)."""
        if not org_id:
            raise HTTPException(
                status_code=400,
                detail="ID de organizacion invalido para el almacenamiento."
            )

        return self._resolve_inside(self.base_storage_path, f"org_{org_id}")

    # =========================
    # LIFECYCLE STORAGE
    # =========================
    def create_org_storage(self, org_id: int) -> str:
        """Crea la carpeta raiz de la organizacion."""
        path = self._get_tenant_path(org_id)
        path.mkdir(parents=True, exist_ok=True)
        return str(path)

    def delete_org_storage(self, org_id: int):
        """Elimina completamente la carpeta de la organizacion."""
        path = self._get_tenant_path(org_id)

        if path.exists():
            shutil.rmtree(path)

    # =========================
    # FILE UPLOAD
    # =========================
    def save_upload_file(self, upload_file: UploadFile, org_id: int, folder: str = "General") -> str:
        """Guarda un archivo PDF dentro del storage de la organizacion."""
        filename = self._validate_pdf_filename(upload_file.filename)
        self._validate_pdf_content_type(upload_file)
        temp_file_path: Path | None = None

        try:
            tenant_storage = self._get_tenant_path(org_id)

            if folder and folder != "General":
                safe_folder = self._validate_path_segment(folder, "Nombre de carpeta")
                folder_path = self._resolve_inside(tenant_storage, safe_folder)
            else:
                folder_path = tenant_storage

            folder_path.mkdir(parents=True, exist_ok=True)
            file_path = self._resolve_inside(folder_path, filename)
            temp_file_path = self._resolve_inside(folder_path, f".{filename}.uploading")

            bytes_written = 0
            header = upload_file.file.read(5)

            if header != b"%PDF-":
                raise HTTPException(status_code=400, detail="El archivo debe ser un PDF valido.")

            with open(temp_file_path, "wb") as buffer:
                buffer.write(header)
                bytes_written += len(header)

                while True:
                    chunk = upload_file.file.read(1024 * 1024)
                    if not chunk:
                        break

                    bytes_written += len(chunk)
                    if bytes_written > self.max_pdf_upload_size:
                        buffer.close()
                        temp_file_path.unlink(missing_ok=True)
                        raise HTTPException(
                            status_code=413,
                            detail=f"El PDF no puede superar {settings.MAX_PDF_UPLOAD_SIZE_MB} MB."
                        )

                    buffer.write(chunk)

            temp_file_path.replace(file_path)
            return filename

        except HTTPException:
            if temp_file_path is not None:
                temp_file_path.unlink(missing_ok=True)
            raise
        except Exception as e:
            if temp_file_path is not None:
                temp_file_path.unlink(missing_ok=True)
            print(f"Error al guardar archivo PDF: {e}")
            raise HTTPException(
                status_code=500,
                detail="Error al guardar archivo."
            )

    # =========================
    # FOLDERS
    # =========================
    def create_folder(self, folder_name: str, org_id: int) -> dict:
        """Crea una carpeta dentro de la organizacion."""
        if not folder_name or folder_name == "General":
            raise HTTPException(status_code=400, detail="Nombre de carpeta invalido.")

        try:
            tenant_storage = self._get_tenant_path(org_id)
            safe_folder = self._validate_path_segment(folder_name, "Nombre de carpeta")
            folder_path = self._resolve_inside(tenant_storage, safe_folder)
            folder_path.mkdir(parents=True, exist_ok=True)

            return {
                "success": True,
                "message": f"Carpeta '{safe_folder}' creada."
            }

        except HTTPException:
            raise
        except Exception as e:
            print(f"Error al crear carpeta: {e}")
            raise HTTPException(
                status_code=500,
                detail="Error al crear carpeta."
            )

    def get_folders(self, org_id: int) -> list:
        """Lista carpetas de la organizacion."""
        folders = set(["General"])

        try:
            target_path = self._get_tenant_path(org_id)

            if target_path.exists():
                for item in os.listdir(target_path):
                    item_path = target_path / item
                    if item_path.is_dir():
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
                pdfs = [f for f in files if f.lower().endswith(".pdf")]

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
            safe_filename = self._validate_pdf_filename(filename)

            if folder and folder != "General":
                safe_folder = self._validate_path_segment(folder, "Nombre de carpeta")
                file_path = self._resolve_inside(tenant_storage, safe_folder, safe_filename)
            else:
                file_path = self._resolve_inside(tenant_storage, safe_filename)

            if not file_path.is_file():
                raise HTTPException(
                    status_code=404,
                    detail="El archivo no existe o no tienes permisos."
                )

            return FileResponse(file_path, media_type="application/pdf")

        except HTTPException:
            raise
        except Exception as e:
            print(f"Error al recuperar el archivo: {e}")
            raise HTTPException(
                status_code=500,
                detail="Error al recuperar el archivo."
            )

    def get_pdf_file_by_relative_path(self, relative_path: str, current_org_id: int) -> FileResponse:
        """Serve seguro por path relativo con validacion de tenant."""
        try:
            parts = relative_path.split("/", 1)

            if not parts or not parts[0].startswith("org_"):
                raise HTTPException(status_code=400, detail="Ruta invalida.")

            org_prefix = parts[0]

            try:
                path_org_id = int(org_prefix.split("_")[1])
            except (IndexError, ValueError):
                raise HTTPException(status_code=400, detail="Ruta invalida.")

            if path_org_id != current_org_id:
                raise HTTPException(status_code=403, detail="Sin permisos.")

            tenant_storage = self._get_tenant_path(current_org_id)
            remaining_path = parts[1] if len(parts) > 1 else ""
            safe_parts = [
                self._validate_path_segment(part, "Ruta")
                for part in remaining_path.split("/")
                if part
            ]

            if not safe_parts:
                raise HTTPException(status_code=400, detail="Ruta invalida.")

            file_path = self._resolve_inside(tenant_storage, *safe_parts)

            if not file_path.is_file():
                raise HTTPException(status_code=404, detail="Archivo no existe.")

            return FileResponse(file_path, media_type="application/pdf")

        except HTTPException:
            raise
        except Exception as e:
            print(f"Error al recuperar archivo: {e}")
            raise HTTPException(
                status_code=500,
                detail="Error al recuperar archivo."
            )


file_manager = FileManager()
