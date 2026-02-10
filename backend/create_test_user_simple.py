"""
Create Simple Test User - Fixed Version
Creates minimal test user with correct field types
"""
import asyncio
import sys
from pathlib import Path
from datetime import datetime, timedelta
from passlib.context import CryptContext

sys.path.insert(0, str(Path(__file__).parent))

from database import SessionLocal, engine
from models import (
    Base, User, MedicalProfile, BloodType,
    MedicalDocument, DocumentType,
    Conversation, Message, MessageRole,
    Appointment
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def create_test_user():
    print("🏥 Creating Test User...\n")
    
    async with SessionLocal() as db:
        try:
            from sqlalchemy import select
            
            # Delete existing test user
            result = await db.execute(
                select(User).where(User.email == "testuser@example.com")
            )
            existing = result.scalar_one_or_none()
            if existing:
                print("⚠️  Deleting existing test user...")
                await db.delete(existing)
                await db.commit()
            
            # Create user
            print("👤 Creating user...")
            user = User(
                name="Juan Pérez",
                email="testuser@example.com",
                password_hash=pwd_context.hash("Test123!"),
                is_active=True
            )
            db.add(user)
            await db.flush()
            uid = user.id
            print(f"   ✅ User: testuser@example.com (ID: {uid})")
            print("   🔑 Password: Test123!")
            
            # Medical profile
            print("\n📋 Creating medical profile...")
            profile = MedicalProfile(
                user_id=uid,
                blood_type=BloodType.O_POSITIVE,
                height_cm=175,
                weight_kg=82,
                date_of_birth=datetime(1978, 5, 15),
                allergies=["Penicillin (rash)", "Sulfa drugs (severe)"],
                chronic_conditions=["Type 2 Diabetes Mellitus", "Hypertension Stage 1"],
                current_medications=[
                    {"name": "Metformin", "dosage": "850mg", "frequency": "2x daily"},
                    {"name": "Lisinopril", "dosage": "10mg", "frequency": "daily"},
                    {"name": "Atorvastatin", "dosage": "20mg", "frequency": "daily"}
                ],
                past_surgeries=[
                    {"name": "Appendectomy", "date": "2005"},
                    {"name": "Hernia repair", "date": "2015"}
                ],
                family_history={"diabetes": ["father"], "hypertension": ["father", "mother"]},
                smoking_status="former",
                alcohol_consumption="occasional",
                exercise_frequency="moderate",
                notes="Well-controlled diabetes and hypertension. Regular check-ups every 3 months."
            )
            db.add(profile)
            print("   ✅ Profile: Age 45, O+, BMI 26.8")
            print("   ⚠️  Allergies: Penicillin, Sulfa drugs")
            print("   💊 Conditions: Diabetes, Hypertension")
           
            # Appointments
            print("\n📅 Creating appointments...")
            appointments = [
                f"Endocrinology - Dr. González - {(datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')} - Diabetes follow-up",
                f"Cardiology - Dr. Sánchez - {(datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')} - BP assessment",
                f"Primary Care - Dr. Martínez - {(datetime.now() + timedelta(days=21)).strftime('%Y-%m-%d')} - General check-up"
            ]
            for apt in appointments:
                db.add(Appointment(user_id=uid, description=apt))
            print(f"   ✅ {len(appointments)} appointments")
            
            # Documents
            print("\n📄 Creating documents...")
            docs = [
                {
                    "title": "Lab Results Jan 2024",
                    "file_name": "labs_2024_01.pdf",
                    "type": DocumentType.LAB_RESULT,
                    "text": "HbA1c: 6.8% | Glucose: 118 mg/dL | Cholesterol: 185 mg/dL | HDL: 48 | LDL: 110"
                },
                {
                    "title": "BP Monitoring Log",
                    "file_name": "bp_log.pdf",
                    "type": DocumentType.MEDICAL_REPORT,
                    "text": "Blood Pressure Log:\n2024-01-05: 128/82\n2024-01-12: 135/88\n2024-01-19: 130/84\nAverage: 130/84"
                },
                {
                    "title": "Current Medications",
                    "file_name": "medications.pdf",
                    "type": DocumentType.PRESCRIPTION,
                    "text": "Metformin 850mg 2x daily\nLisinopril 10mg daily\nAtorv Atorvastatin 20mg daily\nAspirin 81mg daily"
                }
            ]
            for d in docs:
                db.add(MedicalDocument(
                    user_id=uid,
                    title=d["title"],
                    file_name=d["file_name"],
                    file_path=f"/uploads/test/{d['file_name']}",
                    mime_type="application/pdf",
                    document_type=d["type"],
                    file_size=len(d["text"]),
                    extracted_text=d["text"],
                    is_processed=True,
                    document_date=datetime.now() - timedelta(days=30)
                ))
            print(f"   ✅ {len(docs)} documents")
            
            # Conversation
            print("\n💬 Creating conversation...")
            conv = Conversation(user_id=uid, title="Diabetes Questions")
            db.add(conv)
            await db.flush()
            
            messages = [
                (MessageRole.USER, "What should my blood sugar target be?"),
                (MessageRole.ASSISTANT, "For Type 2 Diabetes: Fasting 80-130 mg/dL, Post-meal <180 mg/dL, HbA1c <7%. Your 6.8% is great!"),
                (MessageRole.USER, "Can I take ibuprofen?"),
                (MessageRole.ASSISTANT, "Use caution - ibuprofen can reduce Lisinopril effectiveness. Acetaminophen is safer. Check with your doctor first.")
            ]
            for role, text in messages:
                db.add(Message(conversation_id=conv.id, role=role, content=text))
            print(f"   ✅ {len(messages)} messages")
            
            await db.commit()
            
            print("\n" + "="*60)
            print("✅ TEST USER CREATED!")
            print("="*60)
            print("\n📧 Email: testuser@example.com")
            print("🔑 Password: Test123!")
            print(f"\n👤 User ID: {uid}")
            print(f"📋 Medical Profile: ✅")
            print(f"📅 Appointments: {len(appointments)}")
            print(f"📄 Documents: {len(docs)}")
            print(f"💬 Messages: {len(messages)}")
            
            print("\n🧪 READY TO TEST!")
            print("\nTry these agent queries:")
            print("  - What are my current medications?")
            print("  - Show my upcoming appointments")
            print("  - Search my lab results for glucose")
            print("  - What is my HbA1c?")
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            await db.rollback()


async def main():
    print("🔄 Initializing database...\n")
    await init_db()
    await create_test_user()


if __name__ == "__main__":
    asyncio.run(main())
