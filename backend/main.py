from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi import FastAPI
from hyperon import MeTTa
from fastapi.middleware.cors import CORSMiddleware
from typing import  Dict

from schemas.diagnosis_schema import DiagnosisRequest

from utils.lib import update_knowledge_base_with_symptoms, parse_diagnosed_diseases,extract_and_format_symptoms
from utils.metta_utils import load_diagnosis_components,generate_diagnosis

app = FastAPI(
    title="Neuro-Symbolic Medical Diagnosis API",
    description="Combines LLMs (Gemini) and symbolic reasoning (MeTTa) to infer likely diagnoses from symptoms.",
    version="1.0.0"
)

metta = MeTTa()

# Allow requests from your frontend origin
origins = [
    "http://localhost:5173",
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    print("[ERROR]: Http Exception Error: ",str(exc.detail))
    message = (
        "Internal Server Error"
        if exc.status_code == 500 else exc.detail
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": message
        },
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):

    def format_error(err: Dict) -> str:
        field_path = ".".join(str(loc) for loc in err.get("loc", []) if loc != "body")
        msg = err.get("msg", "Invalid input")
        return f"{field_path}: {msg}"

    formatted_errors = [format_error(error) for error in exc.errors()]
    print(f"[Validation Error]: {formatted_errors}")

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Validation error",
            "errors": formatted_errors
        },
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    print(f"[ERROR]: Unhandled server error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal Server Error",
        },
    )


@app.post("/diagnosis")
def diagnosis(data: DiagnosisRequest):
    symptoms=extract_and_format_symptoms(data.raw_symptoms)

    update_knowledge_base_with_symptoms(metta, data.patient_name, symptoms)
    
    load_diagnosis_components(metta)
    
    result = generate_diagnosis(metta,data.patient_name)
    diseases=parse_diagnosed_diseases(result,data.patient_name)

    capitalized_symptoms = [s.replace('_', ' ').capitalize() for s in symptoms]
    capitalized_diseases = [d.replace('_', ' ').capitalize() for d in diseases]

    return {
        "success":True,
        "patient_name": data.patient_name,
        "symptoms":capitalized_symptoms,
        "diagnosis_result": capitalized_diseases
    }
