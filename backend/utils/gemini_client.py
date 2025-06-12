import os
from dotenv import load_dotenv
from fastapi import HTTPException
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None


def extract_symptoms_from_raw_data(raw_symptoms: str) -> str:
    if not client:
        raise HTTPException(
            status_code=500,
            detail="Gemini client not initialized. Ensure the GEMINI_API_KEY environment variable is correctly set."
        )

    try:
        prompt = (
            "You are a medical diagnosis assistant. "
            "Extract all relevant symptoms from the following raw medical input. "
            "Correct any spelling mistakes in the symptoms before extracting them. "
            "Return only the symptoms as a comma-separated list. "
            "If you are unable to extract any symptoms, return only the string 'No Symptoms'."
            f"Raw data: {raw_symptoms}"
        )

        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=prompt
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while calling the Gemini API: {str(e)}"
        )
    
    extracted = str(response.text).strip().lower()
    print(f"\n🩺 [Gemini Extracted Symptoms]: {extracted}")

    if not extracted or extracted in {"empty", "no symptoms"}:

            raise HTTPException(
                status_code=400,
                detail=(
                    "I am unable to identify any recognizable symptoms from the provided input."
                )
            )

    return extracted
