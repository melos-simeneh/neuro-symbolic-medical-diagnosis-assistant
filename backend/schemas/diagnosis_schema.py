from pydantic import BaseModel, validator
import re

class DiagnosisRequest(BaseModel):
    patient_name: str
    raw_symptoms: str
    
    @validator('patient_name')
    def validate_patient_name(cls, name):
        name = name.strip().capitalize()
        if not re.fullmatch(r'^[A-Za-z]+$', name):
            raise ValueError("Patient name must be a single first name (letters only)")
        return name