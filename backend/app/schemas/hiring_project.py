from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict

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

    model_config = ConfigDict(from_attributes=True)