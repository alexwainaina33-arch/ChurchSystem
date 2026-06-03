import asyncio, uuid, random
from datetime import date, timedelta
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

        members = await db.execute(text("SELECT id FROM members WHERE church_id=:c AND is_deleted=false"), {"c": CHURCH_ID})
        member_ids = [str(r.id) for r in members]
        print(f"Found {len(member_ids)} members")

        session_ids = []
        for i in range(5):
            sid = str(uuid.uuid4())
            sdate = date.today() - timedelta(weeks=i)
            sname = ["1st","2nd","3rd","4th","5th"][i]
            await db.execute(text("""
                INSERT INTO attendance_sessions (id, church_id, branch_id, session_date, session_type, service_name, total_count, adult_count, child_count, male_count, female_count, first_time_visitors, salvations, cars_count, motorbikes_count, total_offering_kes, total_tithe_kes, project_offering_kes, is_deleted, created_at, updated_at)
                VALUES (:id, :ch, :br, :sd, 'sunday_service', :sn, :tot, :ad, :ch2, :mc, :fc, :ft, :sv, :cars, :motos, :off, :tit, :proj, false, now(), now())
                ON CONFLICT DO NOTHING
            """), {"id": sid, "ch": CHURCH_ID, "br": BRANCH_ID, "sd": sdate,
                  "sn": f"Sunday {sname} Service",
                  "tot": random.randint(140,180), "ad": random.randint(100,140),
                  "ch2": random.randint(30,50), "mc": random.randint(60,90),
                  "fc": random.randint(70,100), "ft": random.randint(5,20),
                  "sv": random.randint(1,6), "cars": random.randint(10,30),
                  "motos": random.randint(5,20), "off": random.randint(30000,70000),
                  "tit": random.randint(60000,120000), "proj": random.randint(10000,30000)})
            session_ids.append(sid)
        print(f"Inserted {len(session_ids)} sessions")

        cat_list = [v for k,v in cat_map.items() if k in ("TITHE","OFFERING","PROJECT","THANKS")]
        count = 0
        for i in range(20):
            mid = random.choice(member_ids)
            cat = random.choice(cat_list)
            method = random.choice(["mpesa","mpesa","mpesa","cash","cash"])
            amount = random.choice([2000,3000,5000,7000,10000,15000,20000])
            mpesa = "QK" + str(random.randint(10000,99999)) if method == "mpesa" else None
            gid = str(uuid.uuid4())
            await db.execute(text("""
                INSERT INTO giving_records (id, church_id, branch_id, member_id, session_id, category_id, amount_kes, payment_method, mpesa_ref, is_deleted, created_at, updated_at)
                VALUES (:id, :ch, :br, :m, :s, :cat, :amt, :meth, :mp, false, now() - (:days * interval '1 day'), now())
                ON CONFLICT DO NOTHING
            """), {"id": gid, "ch": CHURCH_ID, "br": BRANCH_ID, "m": mid,
                  "s": random.choice(session_ids), "cat": cat, "amt": amount,
                  "meth": method, "mp": mpesa, "days": random.randint(0,30)})
            count += 1
        print(f"Inserted {count} giving records")
        await db.commit()
        print("DONE")

asyncio.run(seed())
