# app/schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional, Any, Union

class PatientRequest(BaseModel):
    name: str = Field(..., min_length=2, description="Full name of the patient", example="Aman Kumar")
    mobile: str = Field(..., pattern="^[6-9]\\d{9}$", description="Indian mobile number", example="9876543210")
    message: str = Field(..., min_length=1, description="Message to classify", example="I need to consult urgently")

class PredictionResult(BaseModel):
    message: str = Field(..., description="Message that was classified", example="I want to talk to doctor")
    category: str = Field(..., description="Predicted triage category", example="follow-up")
    confidence: float = Field(..., description="Confidence score", example=0.8923)

class CurrentResult(BaseModel):
    category: str = Field(..., description="Predicted triage category", example="emergency")
    confidence: float = Field(..., description="Model confidence score (0 to 1)", example=0.9432)

class PatientResponse(BaseModel):
    current_result: CurrentResult = Field(..., description="Prediction for current message")
    history: List[PredictionResult] = Field(..., description="List of previous message classifications")

class StandardResponse(BaseModel):
    success: bool = Field(..., description="True if request was processed successfully")
    data: Optional[Union[PatientResponse, None]] = Field(
        None, description="Returned data if success=true"
    )
    error: Optional[Union[dict, None]] = Field(
        None, description="Error details if success=false"
    )