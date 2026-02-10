"""
Create Test User with Complete Medical Data
Simple version that uses only existing model fields
Run this script to populate the database with a test user for testing the agent
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime, timedelta
from passlib.context import CryptContext

# Add parent directory to path if needed
sys.path.insert(0, str(Path(__file__).parent))

from database import SessionLocal, engine
from models import (
    Base,
    User, 
    MedicalProfile,
    BloodType,
    Appointment, 
    Conversation, 
    Message, 
    MessageRole,
    MedicalDocument,
    DocumentType
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def init_db():
    """Ensure database tables exist"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def create_test_user():
    """Create a comprehensive test user with medical data"""
    
    print("🏥 Creating Test User with Medical Data...\n")
    
    async with SessionLocal() as db:
        try:
            # 1. Check if test user exists
            from sqlalchemy import select
            result = await db.execute(
                select(User).where(User.email == "testuser@example.com")
            )
            existing_user = result.scalar_one_or_none()
            
            if existing_user:
                print("⚠️  Test user already exists. Deleting old data...")
                await db.delete(existing_user)
                await db.commit()
            
            # 2. Create User Account
            print("👤 Creating user account...")
            hashed_password = pwd_context.hash("Test123!")
            
            test_user = User(
                email="testuser@example.com",
                name="Juan Pérez",
                password_hash=hashed_password,
                is_active=True
            )
            db.add(test_user)
            await db.flush()
            
            user_id = test_user.id
            print(f"   ✅ User created: {test_user.email} (ID: {user_id})")
            print(f"   🔑 Password: Test123!")
            
            # 3. Create Medical Profile
            print("\n📋 Creating medical profile...")
            medical_profile = MedicalProfile(
                user_id=user_id,
                date_of_birth=datetime(1978, 5, 15),  # 45 years old
                gender="male",
                blood_type=BloodType.O_POSITIVE,
                height_cm=175.0,
                weight_kg=82.0,
                
                # Allergies
                allergies="Penicillin (rash, moderate), Sulfa drugs (severe reaction - anaphylaxis history)",
                
                # Chronic Conditions
                chronic_conditions="Type 2 Diabetes Mellitus (diagnosed 2018, well-controlled with medication), Hypertension Stage 1 (mild, controlled)",
                
                # Current Medications
                current_medications="""
- Metformin 850mg: 2 times daily with meals (for diabetes)
- Lisinopril 10mg: 1 time daily in morning (for blood pressure)
- Atorvastatin 20mg: 1 time daily at bedtime (for cholesterol)
- Aspirin 81mg: 1 time daily (cardiovascular protection)
                """.strip(),
                
                # Past Surgeries
                past_surgeries="Appendectomy (2005), Inguinal hernia repair (2015)",
                
                # Family History
                family_history="Father: Type 2 Diabetes, Hypertension, died at 68 (heart attack). Mother: Hypertension, alive at 72. Brother: Pre-diabetes.",
                
                # Lifestyle
                smoking_status="former",  # Quit 5 years ago
                alcohol_consumption="occasional",  # 1-2 drinks per week
                exercise_frequency="moderate",  # 3 times per week, 30 minutes
                
                # Additional Notes
                notes="""
Patient is actively managing his diabetes and hypertension. Regular check-ups every 3 months.
Last HbA1c: 6.8% (good control). Blood pressure averaging 130/85.
Patient reports good compliance with medications. No recent hospitalizations.
Exercises regularly (walking, light cardio). Diet: Low carb, Mediterranean style.
                """.strip()
            )
            db.add(medical_profile)
            print("   ✅ Medical profile created")
            print(f"   📊 Age: 45 years, Blood Type: O+, BMI: {82/(1.75**2):.1f}")
            print(f"   ⚠️  Allergies: Penicillin, Sulfa drugs")
            print(f"   💊 Conditions: Type 2 Diabetes, Hypertension")
            print(f"   💉 Medications: Metformin, Lisinopril, Atorvastatin, Aspirin")
            
            # 4. Create Appointments (using simple description field)
            print("\n📅 Creating appointments...")
            
            appointments_descriptions = [
                f"Endocrinology - Dr. María González - {(datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')} - Diabetes follow-up and HbA1c check",
                f"Cardiology - Dr. Roberto Sánchez - {(datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')} - Cardiovascular risk assessment",
                f"Primary Care - Dr. Ana Martínez - {(datetime.now() + timedelta(days=21)).strftime('%Y-%m-%d')} - General check-up and prescription refills",
                f"Ophthalmology - Dr. Carlos Ruiz - {(datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d')} - Diabetic retinopathy screening",
                f"Endocrinology (Completed) - Dr. María González - {(datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')} - Quarterly diabetes check-up. HbA1c: 6.8%",
                f"Primary Care (Completed) - Dr. Ana Martínez - {(datetime.now() - timedelta(days=180)).strftime('%Y-%m-%d')} - Annual physical. BP: 132/84"
            ]
            
            for desc in appointments_descriptions:
                appointment = Appointment(
                    user_id=user_id,
                    description=desc
                )
                db.add(appointment)
                print(f"   ✅ {desc[:80]}...")
            
            # 5. Create Medical Documents
            print("\n📄 Creating medical documents...")
            
            documents = [
                {
                    "title": "Laboratory Results - January 2024",
                    "file_name": "lab_results_2024_01.pdf",
                    "document_type": DocumentType.LAB_RESULT,
                    "description": "Metabolic panel and kidney function tests",
                    "content": """
LAB RESULTS - January 2024
Patient: Juan Pérez
Date: 2024-01-15

METABOLIC PANEL:
- Glucose (fasting): 118 mg/dL (target: <126)
- HbA1c: 6.8% (target: <7.0% for diabetics)
- Total Cholesterol: 185 mg/dL
- LDL: 110 mg/dL (target: <100)
- HDL: 48 mg/dL
- Triglycerides: 135 mg/dL

KIDNEY FUNCTION:
- Creatinine: 0.9 mg/dL (normal)
- eGFR: 92 mL/min (normal kidney function)
- Microalbumin/Creatinine ratio: 18 mg/g (normal)

INTERPRETATION:
Diabetes well-controlled. Cholesterol slightly elevated but acceptable.
Kidney function normal (important for diabetics).
Continue current medications.
                    """.strip()
                },
                {
                    "title": "Blood Pressure Log 2024",
                    "file_name": "blood_pressure_log_2024.pdf",
                    "document_type": DocumentType.MEDICAL_REPORT,
                    "description": "Home blood pressure monitoring log",
                    "content": """
BLOOD PRESSURE MONITORING LOG
Patient: Juan Pérez
Period: January - February 2024

Home BP readings (morning):
2024-01-05: 128/82
2024-01-12: 135/88
2024-01-19: 130/84
2024-01-26: 132/86
2024-02-02: 129/83
2024-02-09: 127/81
2024-02-16: 131/85

Average: 130/84 mmHg
Target: <130/80 mmHg

NOTES:
BP well-controlled with current Lisinopril dose.
One reading elevated (135/88) - patient had stressful day at work.
Continue current regimen.
                    """.strip()
                },
                {
                    "title": "Current Medications",
                    "file_name": "medication_list_current.pdf",
                    "document_type": DocumentType.PRESCRIPTION,
                    "description": "Current medication list with dosing instructions",
                    "content": """
CURRENT MEDICATION LIST
Patient: Juan Pérez
Updated: February 2024

1. METFORMIN 850mg
   Purpose: Type 2 Diabetes control
   Dose: 1 tablet twice daily with meals
   Prescriber: Dr. María González (Endocrinology)
   Refills: 3 remaining
   Notes: May cause stomach upset initially

2. LISINOPRIL 10mg
   Purpose: Hypertension, Kidney protection
   Dose: 1 tablet once daily in morning
   Prescriber: Dr. Ana Martínez (Primary Care)
   Refills: 5 remaining
   Notes: May cause dry cough (report if persistent)

3. ATORVASTATIN 20mg
   Purpose: High cholesterol, Cardiovascular protection
   Dose: 1 tablet once daily at bedtime
   Prescriber: Dr. Ana Martínez (Primary Care)
   Refills: 5 remaining
   Notes: Report muscle pain or weakness

4. ASPIRIN 81mg (Low-dose)
   Purpose: Cardiovascular protection
   Dose: 1 tablet once daily
   Prescriber: Dr. Ana Martínez (Primary Care)
   Refills: Over-the-counter
   Notes: Take with food to reduce stomach irritation

ALLERGIES:
⚠️  PENICILLIN - Moderate rash
⚠️  SULFA DRUGS - Severe reaction (anaphylaxis)

PHARMACY: MedPlus Pharmacy, Main St.
Phone: (555) 123-4567
                    """.strip()
                },
                {
                    "title": "Diabetes Management Guidelines",
                    "file_name": "diabetes_education_materials.pdf",
                    "document_type": DocumentType.OTHER,
                    "description": "Diabetes management education materials",
                    "content": """
DIABETES MANAGEMENT GUIDELINES
For Type 2 Diabetes Patients

MEDICATION:
- Take Metformin with meals to reduce stomach upset
- Never skip doses
- If you miss a dose, take it as soon as you remember (unless close to next dose)

DIET:
- Limit carbohydrates: 45-60g per meal
- Focus on complex carbs (whole grains, vegetables)
- Avoid sugary drinks and desserts
- Eat regular meals (don't skip meals)

EXERCISE:
- Target: 150 minutes per week (30 min, 5 days)
- Walking, swimming, cycling are good choices
- Check blood sugar before and after exercise

MONITORING:
- Check blood sugar as directed by your doctor
- Record readings in a log
- Watch for symptoms of low blood sugar (hypoglycemia)

WARNING SIGNS:
- Very high blood sugar (>300 mg/dL)
- Symptoms of DKA: thirst, frequent urination, fatigue, nausea
- Low blood sugar symptoms: shaking, sweating, confusion
- Foot problems: numbness, cuts that won't heal

CALL DOCTOR IF:
- Blood sugar consistently high or low
- Frequent hypoglycemic episodes
- New symptoms or concerns
                    """.strip()
                }
            ]
            
            for doc_data in documents:
                doc = MedicalDocument(
                    user_id=user_id,
                    title=doc_data["title"],
                    file_name=doc_data["file_name"],
                    file_path=f"/uploads/test_user/{doc_data['file_name']}",  # Mock path
                    mime_type="application/pdf",
                    document_type=doc_data["document_type"],
                    file_size=len(doc_data["content"]),
                    extracted_text=doc_data["content"],
                    description=doc_data.get("description", ""),
                    is_processed=True,
                    document_date=datetime.now() - timedelta(days=30)
                )
                db.add(doc)
                print(f"   ✅ {doc_data['file_name']}")
            
            # 6. Create Conversation History
            print("\n💬 Creating conversation history...")
            
            conversation = Conversation(
                user_id=user_id,
                title="Diabetes Management Questions"
            )
            db.add(conversation)
            await db.flush()
            
            messages = [
                {
                    "role": MessageRole.USER,
                    "content": "What should my target blood sugar be?"
                },
                {
                    "role": MessageRole.ASSISTANT,
                    "content": "For someone with Type 2 Diabetes like you, the target blood sugar levels are:\n\n- Fasting (before meals): 80-130 mg/dL\n- 2 hours after meals: Less than 180 mg/dL\n- HbA1c: Less than 7.0%\n\nYour recent HbA1c of 6.8% shows good control! Keep up the good work with your Metformin and healthy lifestyle."
                },
                {
                    "role": MessageRole.USER,
                    "content": "Can I take ibuprofen with my medications?"
                },
                {
                    "role": MessageRole.ASSISTANT,
                    "content": "You should be cautious with ibuprofen because you're taking Lisinopril for blood pressure. NSAIDs like ibuprofen can:\n\n1. Reduce the effectiveness of Lisinopril\n2. Increase blood pressure\n3. Potentially affect kidney function\n\nFor occasional pain relief, acetaminophen (Tylenol) is usually safer. However, always check with your doctor before taking any new medications, especially given your medical conditions and current medications."
                },
                {
                    "role": MessageRole.USER,
                    "content": "Do I need to check my feet regularly?"
                },
                {
                    "role": MessageRole.ASSISTANT,
                    "content": "Yes, absolutely! Daily foot checks are very important for people with diabetes. Here's why and what to look for:\n\n**Why it matters:**\n- Diabetes can reduce blood flow and cause nerve damage in feet\n- You might not feel small cuts or injuries\n- Minor problems can become serious infections\n\n**Daily foot check:**\n- Look for cuts, blisters, redness, swelling\n- Check between toes for moisture or cracks\n- Feel for warm spots or tenderness\n- Look for changes in color or temperature\n\n**Foot care tips:**\n- Wash feet daily with mild soap\n- Dry thoroughly, especially between toes\n- Moisturize (but not between toes)\n- Wear comfortable, well-fitting shoes\n- Never walk barefoot\n\n**When to call doctor:**\n- Any cut or blister that doesn't heal in 2-3 days\n- Signs of infection (redness, warmth, pus)\n- Numbness or tingling\n- Color changes\n\nYour upcoming ophthalmology appointment is also important - diabetic complications can affect eyes too!"
                }
            ]
            
            for msg_data in messages:
                message = Message(
                    conversation_id=conversation.id,
                    role=msg_data["role"],
                    content=msg_data["content"]
                )
                db.add(message)
            
            print(f"   ✅ Conversation created with {len(messages)} messages")
            
            # Commit all changes
            await db.commit()
            
            print("\n" + "="*60)
            print("✅ TEST USER CREATED SUCCESSFULLY!")
            print("="*60)
            print(f"\n📧 Email: testuser@example.com")
            print(f"🔑 Password: Test123!")
            print(f"\n👤 User ID: {user_id}")
            print(f"📋 Medical Profile: ✅")
            print(f"📅 Appointments: {len(appointments_descriptions)}")
            print(f"📄 Documents: {len(documents)}")
            print(f"💬 Conversation Messages: {len(messages)}")
            
            print("\n" + "="*60)
            print("🧪 READY TO TEST!")
            print("="*60)
            print("\n1. Login with: testuser@example.com / Test123!")
            print("2. Try agent queries like:")
            print("   - What are my current medications?")
            print("   - Show my upcoming appointments")
            print("   - Search my lab results for glucose levels")
            print("   - What should I know about my diabetes medications?")
            print("\n3. Test individual tools:")
            print("   - GET /agent/capabilities")
            print("   - POST /agent/test-tool/get_user_medical_profile")
            print("   - POST /agent/test-tool/search_medical_documents")
            
        except Exception as e:
            print(f"\n❌ Error creating test user: {e}")
            import traceback
            traceback.print_exc()
            await db.rollback()


async def main():
    """Main entry point"""
    # Initialize database if not already done
    print("🔄 Initializing database...")
    await init_db()
    print("✅ Database initialized\n")
    
    # Create test user
    await create_test_user()


if __name__ == "__main__":
    asyncio.run(main())
