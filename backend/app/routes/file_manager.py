from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_db
from services.file_manager import file_manager
from core.security import require_recruiter

router = APIRouter(prefix="/filemanager", tags=["File Manager"])

@router.post("/upload")
async def upload_cv(
    file: UploadFile = File(...),
    folder: str = Form("General"),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_recruiter)
):
    org_id = db.info.get("organization_id")
    filename = file_manager.save_upload_file(file, org_id=org_id, folder=folder)
    return {"message": "Éxito", "filename": filename, "folder": folder}

@router.post("/create-folder")
async def create_folder(
    folder_name: str = Form(...),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_recruiter)
):
    org_id = db.info.get("organization_id")
    result = file_manager.create_folder(folder_name, org_id=org_id)
    return result

@router.get("/folders")
async def get_folders(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_recruiter)
):
    org_id = db.info.get("organization_id")
    folders = file_manager.get_folders(org_id=org_id)
    return {"folders": folders}

@router.get("/list")
async def list_cvs(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_recruiter)
):
    org_id = db.info.get("organization_id")
    files = file_manager.get_file_tree(org_id=org_id)
    return files

@router.get("/view/{folder}/{filename}")
async def view_cv(
    folder: str,
    filename: str,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_recruiter)
):
    org_id = db.info.get("organization_id")

    return file_manager.get_pdf_file_response(org_id=org_id, folder=folder, filename=filename)

# PDFs endpoint - handles paths like org_1/filename.pdf or org_1/folder/filename.pdf
pdfs_router = APIRouter(tags=["PDFs"])

@pdfs_router.get("/pdfs/{file_path:path}")
async def serve_pdf(
    file_path: str,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_recruiter)
):
    """
    Serve PDF files from the storage. Expects paths like:
    - org_1/filename.pdf
    - org_1/folder/filename.pdf
    """
    current_org_id = db.info.get("organization_id")
    return file_manager.get_pdf_file_by_relative_path(file_path, current_org_id=current_org_id)
