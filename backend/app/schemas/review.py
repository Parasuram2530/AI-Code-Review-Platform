from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class ReviewCreate(BaseModel):
    code: str
    language: str

class ReviewResponse(BaseModel):
    id: int
    user_id: int
    code: str
    language: str
    review_text: str
    score: int = Field(ge=0, le=100)
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ReviewSummary(BaseModel):
    id: int
    language: str
    score: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
