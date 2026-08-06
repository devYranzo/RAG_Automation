from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class HiringProjectMemberResponse(BaseModel):
    id: int
    user_id: int
    username: str
    email: str
    role: str

    model_config = ConfigDict(from_attributes=True)


class HiringProjectDocumentResponse(BaseModel):
    id: int
    filename: str
    relative_path: str
    status: str
    added_by: Optional[int]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class HiringProjectListResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    documents_count: int
    members_count: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class HiringProjectDetailResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    search_prompt: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime
    members: List[HiringProjectMemberResponse]
    documents: List[HiringProjectDocumentResponse]
    current_user_role: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# ==========================
# CREATE / UPDATE
# ==========================

class HiringProjectCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=200)
    description: Optional[str] = None
    search_prompt: Optional[str] = None


class HiringProjectUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=2, max_length=200)
    description: Optional[str] = None
    search_prompt: Optional[str] = None
    status: Optional[Literal["ACTIVE", "DRAFT", "ARCHIVED"]] = None


class HiringProjectMemberCreate(BaseModel):
    user_id: int
    role: Literal["OWNER", "RECRUITER"] = "RECRUITER"