def load_diagnosis_components(metta):
    metta.run("!(import! &self metta:main)")

def generate_diagnosis(metta, patient_name, depth=3):
    query=f"!(syn &self (fromNumber {depth}) (: $prf (Result has_disease {patient_name} $disease)))"
    return metta.run(query)

def add_symptom_to_kb(metta,sym_id,patient_name,symptom):
    symptom_id=f"{str(patient_name).upper()}_SYM{sym_id}"
    metta_code = f"!(add-atom &self (: {symptom_id} (Evaluation has_symptom {patient_name} {symptom})))"
    metta.run(metta_code)

def remove_symptom_from_kb(metta,patient_name,symptom):
    metta_code = f"!(remove-atom &self (: $x (Evaluation has_symptom {patient_name} {symptom})))"
    metta.run(metta_code)
    
def get_patient_symptoms_from_kb(metta, patient_name):
    query = f"!(match &self (: $x (Evaluation has_symptom {patient_name} $y)) $y)"
    return metta.run(query)


