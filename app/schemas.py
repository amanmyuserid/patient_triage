from pydantic import BaseModel, Field
from typing import List, Optional, Any

class PatientRequest(BaseModel):
    name: str = Field(..., min_length=2)
    mobile: str = Field(..., pattern="^[6-9]\\d{9}$")
    message: str = Field(..., min_length=1)

class PredictionResult(BaseModel):
    message: str
    category: str
    confidence: float

class CurrentResult(BaseModel):
    category: str
    confidence: float

class PatientResponse(BaseModel):
    current_result: CurrentResult
    history: List[PredictionResult]

class StandardResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    error: Optional[dict] = None