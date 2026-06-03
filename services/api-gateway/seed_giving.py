import asyncio, uuid, random
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

DATABASE_URL = "postgresql+asyncpg://church_user:church_pass_2024@postgres:5432/churchdb"
engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

CHURCH_ID = "00000000-0000-0000-0000-000000000001"
BRANCH_ID = "00000000-0000-0000-0000-000000000002"

async def seed():
    async with AsyncSessionLocal() as db:
        cats = await db.execute(text("SELECT id, code FROM giving_categories WHERE church_id=:c"), {"c": CHURCH_ID})
        cat_map = {r.code: str(r.id) for r in cats}
        print("Categories:", list(cat_map.keys()))

        members = await db.execute(text("SELECT id FROM members WHERE church_id=:c AND is_deleted=false"), {"c": CHURCH_ID})
        member_ids = [str(r.id) for r in members]
        print(f"Members: {len(member_ids)}")

        sessions = await db.execute(text("SELECT id FROM attendance_sessions WHERE church_id=:c AND is_deleted=false"), {"c": CHURCH_ID})
        session_ids = [str(r.id) for r in sessions]
        print(f"Sessions: {len(session_ids)}")

        cat_list = [v for k,v in cat_map.items() if k in ("TITHE","OFFERING","PROJECT","THANKSGIVING","MISSIONS")]
        if not cat_list:
            cat_list = list(cat_map.values())

        count = 0
        for mid in member_ids:
            for _ in range(random.randint(3, 6)):
                method = random.choice(["mpesa","mpesa","mpesa","cash","cash"])
                amount = random.choice([2000,3000,5000,7000,10000,15000,20000])
                mpesa = "QK" + str(random.randint(10000,99999)) if method == "mpesa" else None
                gid = str(uuid.uuid4())
                await db.execute(text("""
                    INSERT INTO giving_records (id, church_id, branch_id, member_id, session_id, category_id, amount_kes, payment_method, mpesa_ref, is_deleted, created_at, updated_at)
                    VALUES (:id, :ch, :br, :m, :s, :cat, :amt, :meth, :mp, false, now() - (:days * interval '1 day'), now())
                """), {"id": gid, "ch": CHURCH_ID, "br": BRANCH_ID, "m": mid,
                      "s": random.choice(session_ids), "cat": random.choice(cat_list),
                      "amt": amount, "meth": method, "mp": mpesa,
                      "days": random.randint(0, 30)})
                count += 1

        await db.commit()
        print(f"Inserted {count} giving records")

        total = await db.execute(text("SELECT COUNT(*) as c, SUM(amount_kes) as s FROM giving_records WHERE church_id=:c AND is_deleted=false"), {"c": CHURCH_ID})
        row = total.fetchone()
        print(f"Total giving records: {row.c}, Total KES: {row.s:,.0f}")

asyncio.run(seed())
