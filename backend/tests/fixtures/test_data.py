"""
Test Data and Fixtures
Shared test data for creating consistent test scenarios
"""
from datetime import datetime, timedelta
from models import BloodType, DocumentType


# Sample user data
SAMPLE_USERS = [
    {
        "name": "John Doe",
        "email": "john@example.com",
        "password": "SecurePass123!"
    },
    {
        "name": "Jane Smith",
        "email": "jane@example.com",
        "password": "AnotherPass456!"
    }
]


# Sample medical profile data
SAMPLE_MEDICAL_PROFILE = {
    "blood_type": BloodType.O_POSITIVE,
    "height_cm": 175,
    "weight_kg": 75,
    "date_of_birth": datetime(1985, 3, 15),
    "allergies": [
        "Penicillin (moderate rash)",
        "Peanuts (anaphylaxis)"
    ],
    "chronic_conditions": [
        "Type 2 Diabetes",
        "Hypertension"
    ],
    "current_medications": [
        {
            "name": "Metformin",
            "dosage": "500mg",
            "frequency": "twice daily"
        },
        {
            "name": "Lisinopril",
            "dosage": "10mg",
            "frequency": "once daily"
        }
    ],
    "past_surgeries": [
        {
            "name": "Appendectomy",
            "date": "2010"
        }
    ],
    "smoking_status": "former",
    "alcohol_consumption": "occasional",
    "exercise_frequency": "moderate"
}


# Sample appointments
SAMPLE_APPOINTMENTS = [
    f"Cardiology - Dr. Smith - {(datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')} - Regular checkup",
    f"Endocrinology - Dr. Johnson - {(datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')} - Diabetes follow-up",
    f"Primary Care - Dr. Brown - {(datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')} - Annual physical"
]


# Sample medical documents
SAMPLE_DOCUMENTS = [
    {
        "title": "Lab Results - Blood Work",
        "file_name": "lab_results_2024.pdf",
        "document_type": DocumentType.LAB_RESULT,
        "description": "Complete blood count and metabolic panel",
        "extracted_text": """
LABORATORY RESULTS
Patient: Test Patient
Date: 2024-01-15

COMPLETE BLOOD COUNT:
- WBC: 7.2 K/uL (Normal)
- RBC: 4.8 M/uL (Normal)
- Hemoglobin: 14.5 g/dL (Normal)
- Hematocrit: 42% (Normal)

METABOLIC PANEL:
- Glucose: 105 mg/dL (Slightly elevated)
- BUN: 18 mg/dL (Normal)
- Creatinine: 1.0 mg/dL (Normal)
- Sodium: 140 mEq/L (Normal)

INTERPRETATION: Results generally within normal limits. 
Glucose slightly elevated - continue monitoring.
        """.strip()
    },
    {
        "title": "Prescription Record",
        "file_name": "prescription_2024.pdf",
        "document_type": DocumentType.PRESCRIPTION,
        "description": "Current medication prescriptions",
        "extracted_text": """
PRESCRIPTION RECORD
Patient: Test Patient
Date: 2024-02-01

ACTIVE PRESCRIPTIONS:
1. Metformin 500mg - Take twice daily with meals
2. Lisinopril 10mg - Take once daily in the morning
3. Atorvastatin 20mg - Take once daily at bedtime

Allergies: Penicillin (rash)
        """.strip()
    }
]


# Sample chat messages
SAMPLE_CHAT_MESSAGES = [
    {
        "role": "user",
        "content": "What are my current medications?"
    },
    {
        "role": "assistant",
        "content": "Based on your medical profile, you are currently taking:\n1. Metformin 500mg - twice daily\n2. Lisinopril 10mg - once daily"
    },
    {
        "role": "user",
        "content": "Can I take ibuprofen?"
    },
    {
        "role": "assistant",
        "content": "Since you're taking Lisinopril, you should use ibuprofen with caution. NSAIDs can reduce the effectiveness of blood pressure medications. Consider acetaminophen instead, but consult your doctor first."
    }
]
