import re

def extract_discharge_summary(text):
    """
    Extract structured information from a discharge summary OCR text.
    Input:
        text (str): OCR extracted text
    Output:
        dict: Structured discharge summary
    """

    # Hospital
    hospital = re.search(r'^(.*)', text)
    hospital = hospital.group(1).strip() if hospital else None

    # Patient Name
    patient = re.search(
        r'Patient:\s*MRN:\s*DOB:\s*\n([A-Za-z ]+)\s+MRN-',
        text,
        re.MULTILINE
    )
    patient_name = patient.group(1).strip() if patient else None

    # MRN
    mrn = re.search(r'(MRN-\d+)', text)
    mrn = mrn.group(1) if mrn else None

    # Date of Birth
    dob = re.search(r'(\d{4}-\d{2}-\d{2})', text)
    dob = dob.group(1) if dob else None

    # Chief Complaint
    chief = re.search(
        r'Patient presented.*?consistent with (.*?)\.',
        text,
        re.DOTALL
    )
    chief_complaint = chief.group(1).strip() if chief else None

    # History of Present Illness
    history = re.search(
        r'1\. CHIEF COMPLAINT.*?\n\n(.*?)\n\n2\.',
        text,
        re.DOTALL
    )
    history = history.group(1).strip() if history else None

    # Diagnosis
    diagnosis = re.search(
        r'2\. ADMISSION DIAGNOSIS\s*\n\n(.*?)\s*\(ICD-10',
        text,
        re.DOTALL
    )
    diagnosis = diagnosis.group(1).strip() if diagnosis else None

    # ICD-10
    icd = re.search(
        r'ICD-10:\s*([A-Z]\d+\.\d+)',
        text
    )
    icd10 = icd.group(1) if icd else None

    # Hospital Course
    course = re.search(
        r'3\. HOSPITAL COURSE\s*\n\n(.*?)\n\n4\.',
        text,
        re.DOTALL
    )
    hospital_course = course.group(1).strip() if course else None

    # Procedures
    procedures_match = re.search(
        r'4\. PERTINENT LABS & IMAGING\s*\n\n.*?:\s*(.*?)\.',
        text,
        re.DOTALL
    )

    if procedures_match:
        procedures = [
            p.strip()
            for p in procedures_match.group(1).split(",")
        ]
    else:
        procedures = []

    # Medications
    medications = re.findall(
        r'\*\s*(.*)',
        text
    )

    # Diet
    diet = re.search(
        r'DIET:\s*(.*?)\.',
        text
    )
    diet = diet.group(1).strip() if diet else None

    # Activity
    activity = re.search(
        r'ACTIVITY:\s*(.*?)\.',
        text
    )
    activity = activity.group(1).strip() if activity else None

    # Follow Up
    follow = re.search(
        r'FOLLOW-UP:\s*(.*?)Return',
        text,
        re.DOTALL
    )
    follow_up = follow.group(1).strip() if follow else None

    # Emergency Instructions
    emergency = re.search(
        r'Return.*?if you experience(.*?)\.',
        text,
        re.DOTALL
    )
    emergency = emergency.group(1).strip() if emergency else None

    # Allergies
    allergy = re.search(
        r'Allergies:\s*(.*?)\.',
        text
    )
    allergies = allergy.group(1).strip() if allergy else None

    # Code Status
    code = re.search(
        r'Code Status:\s*(.*?)\.',
        text
    )
    code_status = code.group(1).strip() if code else None

    # Doctor
    doctor = re.search(
        r'Electronically Signed By:.*?\n\n(.*?)\s+\d{2}/\d{2}/\d{4}',
        text,
        re.DOTALL
    )
    doctor = doctor.group(1).strip() if doctor else None

    # Discharge Date
    discharge = re.search(
        r'(\d{2}/\d{2}/\d{4})',
        text
    )
    discharge_date = discharge.group(1) if discharge else None

    return {
        "hospital": hospital,
        "patient_name": patient_name,
        "mrn": mrn,
        "dob": dob,
        "chief_complaint": chief_complaint,
        "history_of_present_illness": history,
        "diagnosis": diagnosis,
        "icd10": icd10,
        "hospital_course": hospital_course,
        "procedures": procedures,
        "medications": medications,
        "diet": diet,
        "activity": activity,
        "follow_up": follow_up,
        "emergency_instructions": emergency,
        "allergies": allergies,
        "code_status": code_status,
        "doctor": doctor,
        "discharge_date": discharge_date
    }