import re

from .metta_utils  import add_symptom_to_kb, get_patient_symptoms_from_kb, remove_symptom_from_kb
from .gemini_client import extract_symptoms_from_raw_data

def flatten_symptom_results(nested_list):
    flat = [str(item).strip("()' ") for sublist in nested_list for item in sublist]
    return [symptom for symptom in flat if symptom]

def add_symptoms_to_knowledge_base(metta, patient_name, symptoms):
    existing_symptoms = get_patient_symptoms_from_kb(metta, patient_name)
    existing_flat = flatten_symptom_results(existing_symptoms)
    
    symptom_id=len(existing_flat)

    symptoms_to_add = [sym for sym in symptoms if sym not in existing_flat]
    symptoms_to_remove = [sym for sym in existing_flat if sym not in symptoms]

    if not symptoms_to_add:
        print(f"\nℹ️ All symptoms for {patient_name} are already recorded in the KB.\n")
        return

    for symptom in symptoms_to_remove:
        remove_symptom_from_kb(metta, patient_name, symptom)

    for symptom in symptoms_to_add:
        symptom_id+=1
        add_symptom_to_kb(metta,symptom_id,patient_name,symptom)

    if symptoms_to_add:
        symptoms_formatted = "\n".join(f"  • {symptom}" for symptom in symptoms_to_add)
        print(f"\n➕ Added new symptoms for {patient_name}:\n{symptoms_formatted}\n")
    
    if symptoms_to_remove:
        removed_formatted = "\n".join(f"  • {symptom}" for symptom in symptoms_to_remove)
        print(f"\n❌ Removed outdated symptoms for {patient_name}:\n{removed_formatted}\n")

def extract_and_format_symptoms(raw_symptoms):
    extracted_raws: str = extract_symptoms_from_raw_data(raw_symptoms)
    symptom_list = [
        s.strip().replace(' ', '_') 
        for s in extracted_raws.split(',') 
        if s.strip()
    ]
    return symptom_list


def update_knowledge_base_with_symptoms(metta, patient_name, symptoms):
    add_symptoms_to_knowledge_base(metta, patient_name, symptoms)

    matched_symptoms = get_patient_symptoms_from_kb(metta, patient_name)
    flat_results = flatten_symptom_results(matched_symptoms)

    print(f"\n📋 Current symptoms for {patient_name} in the KB:")
    for symptom in flat_results:
        print(f"  • {symptom}")

    missing_symptoms = [sym for sym in symptoms if sym not in flat_results]
    if missing_symptoms:
        print(f"\n❗ ERROR: The following symptoms were NOT found in the KB for {patient_name}:")
        for missing in missing_symptoms:
            print(f"  • {missing}")

def parse_diagnosed_diseases(result, patient_name):
    result_str=str(result)
    pattern = r"\(Result has_disease " + re.escape(patient_name) + r" (\w+)\)"
    
    matches = re.findall(pattern, result_str)
    

    unique_diseases = list(set(matches))
    return unique_diseases



