
import re


def create_search_text(doc):
    parts = [
        f"Hospital: {doc.get('hospital', '')}",
        f"Patient: {doc.get('patient_name', '')}",
        f"Diagnosis: {doc.get('diagnosis', '')}",
        f"Chief Complaint: {doc.get('chief_complaint', '')}",
        f"History: {doc.get('history_of_present_illness', '')}",
        f"Hospital Course: {doc.get('hospital_course', '')}",
        f"Procedures: {', '.join(doc.get('procedures', []))}",
        f"Medications: {', '.join(doc.get('medications', []))}",
        f"Follow Up: {doc.get('follow_up', '')}",
        f"Allergies: {doc.get('allergies', '')}"
    ]

    return "\n".join(parts)


def format_patient_response(response):
    field_labels = {
        "name": "Name",
        "hospital": "Hospital",
        "diagnosis": "Diagnosis",
        "chief complaint": "Chief complaint",
        "history": "History",
        "hospital course": "Hospital course",
        "procedures": "Procedures",
        "medications": "Medications",
        "follow up": "Follow-up",
        "follow-up": "Follow-up",
        "allergies": "Allergies",
        "summary": "Summary",
    }
    labels = "|".join(re.escape(label) for label in sorted(field_labels, key=len, reverse=True))
    field_pattern = re.compile(rf"(?<![\w*])[ \t]*(?P<label>{labels})[ \t]*:", re.IGNORECASE)
    patient_pattern = re.compile(r"(?im)^\s*(Patient\s+\d+)\s*:?\s*$")
    separator_pattern = re.compile(r"(?m)^\s*[-=_]{3,}\s*$")

    def format_field(match):
        label = field_labels[match.group("label").lower()]
        return f"\n- **{label}:**"

    formatted = separator_pattern.sub("", response)
    formatted = patient_pattern.sub(lambda match: f"\n\n### {match.group(1)}\n", formatted)
    formatted = field_pattern.sub(format_field, formatted)
    formatted = re.sub(r"[ \t]+\n", "\n", formatted)
    return re.sub(r"\n{3,}", "\n\n", formatted).strip()


def query_builder(query, retrival_result):

    prompt = f"""
You are an expert medical AI assistant.

You have been provided with the top 5 retrieved medical document chunks from a Retrieval-Augmented Generation (RAG) system.

Instructions:
1. Carefully analyze all retrieved document chunks.
2. Identify each unique patient present in the retrieved context.
3. For EACH patient, create a separate summary.
4. Do NOT merge information from different patients.
5. Use ONLY the information provided in the retrieved context.
6. If some information is missing for a patient, write "Not Available" for that field instead of making assumptions.
7. Do not generate or infer information that is not explicitly present in the context.
8. If none of the retrieved documents contain information relevant to the user's question, respond:
   "The requested information is not available in the retrieved documents."

Retrieved Context:
{retrival_result}

User Question:
{query}

Return only Markdown using this format, with every field on its own bullet line:

## Patient 1
- **Name:** ...
- **Hospital:** ...
- **Diagnosis:** ...
- **Chief complaint:** ...
- **Hospital course:** ...
- **Procedures:** ...
- **Medications:** ...
- **Follow-up:** ...
- **Summary:** ...

## Patient 2
- **Name:** ...
- **Hospital:** ...
- **Diagnosis:** ...
- **Chief complaint:** ...
- **Hospital course:** ...
- **Procedures:** ...
- **Medications:** ...
- **Follow-up:** ...
- **Summary:** ...

Continue the same format for every unique patient found in the retrieved context.

Do not put multiple fields on the same line.
"""

    return prompt


