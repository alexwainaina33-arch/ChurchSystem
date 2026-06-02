import asyncio
import uuid
from app.database import AsyncSessionLocal
from app.models.church import Church, Branch, GivingCategory, Account

CHURCH_ID = uuid.UUID("00000000-0000-0000-0000-000000000001")
BRANCH_ID = uuid.UUID("00000000-0000-0000-0000-000000000002")

async def seed():
    async with AsyncSessionLocal() as db:
        from sqlalchemy import select
        existing = await db.execute(select(Church).where(Church.id == CHURCH_ID))
        if existing.scalar_one_or_none():
            print("Already seeded")
            return

        church = Church(id=CHURCH_ID, name="Grace Community Church", denomination="Pentecostal",
                        country="Kenya", city="Nairobi", phone="0700000001", email="admin@grace.church")
        db.add(church)

        branch = Branch(id=BRANCH_ID, church_id=CHURCH_ID, name="Nairobi Main Branch",
                        address="Westlands, Nairobi", pastor_name="Pastor John Kamau", phone="0700000002")
        db.add(branch)

        categories = [
            GivingCategory(church_id=CHURCH_ID, name="Tithe", code="TITHE", gl_debit_code="1000", gl_credit_code="4000"),
            GivingCategory(church_id=CHURCH_ID, name="Offering", code="OFFERING", gl_debit_code="1000", gl_credit_code="4010"),
            GivingCategory(church_id=CHURCH_ID, name="Project Offering", code="PROJECT", gl_debit_code="1000", gl_credit_code="4020"),
            GivingCategory(church_id=CHURCH_ID, name="Thanksgiving", code="THANKS", gl_debit_code="1000", gl_credit_code="4010"),
            GivingCategory(church_id=CHURCH_ID, name="Missions", code="MISSIONS", gl_debit_code="1000", gl_credit_code="4010"),
        ]
        for c in categories:
            db.add(c)

        accounts = [
            Account(church_id=CHURCH_ID, code="1000", name="Cash on Hand", type="asset"),
            Account(church_id=CHURCH_ID, code="1010", name="M-Pesa Account", type="asset"),
            Account(church_id=CHURCH_ID, code="1020", name="Bank Account", type="asset"),
            Account(church_id=CHURCH_ID, code="4000", name="Tithe Income", type="income"),
            Account(church_id=CHURCH_ID, code="4010", name="Offering Income", type="income"),
            Account(church_id=CHURCH_ID, code="4020", name="Project Offering Income", type="income"),
            Account(church_id=CHURCH_ID, code="5000", name="General Expenses", type="expense"),
            Account(church_id=CHURCH_ID, code="3000", name="Church Equity", type="equity"),
        ]
        for a in accounts:
            db.add(a)

        await db.commit()
        print("Seed complete — Church, Branch, Categories, Accounts all created")

if __name__ == "__main__":
    asyncio.run(seed())
