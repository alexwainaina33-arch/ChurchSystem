import asyncio, uuid
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

DATABASE_URL = "postgresql+asyncpg://church_user:church_pass_2024@postgres:5432/churchdb"
engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

CHURCH_ID = "00000000-0000-0000-0000-000000000001"
BRANCH_ID = "00000000-0000-0000-0000-000000000002"

members_data = [
    ("Mary","Wanjiku","0722100001","female","married"),
    ("Peter","Mwangi","0722100002","male","single"),
    ("Grace","Akinyi","0722100003","female","married"),
    ("James","Ochieng","0722100004","male","married"),
    ("Ruth","Kamau","0722100005","female","single"),
    ("David","Njoroge","0722100006","male","married"),
    ("Esther","Wambui","0722100007","female","married"),
    ("Samuel","Otieno","0722100008","male","single"),
    ("Faith","Muthoni","0722100009","female","married"),
    ("Joseph","Kariuki","0722100010","male","married"),
]

async def seed():
    async with AsyncSessionLocal() as db:
        inserted = 0
        for fn, ln, ph, gender, marital in members_data:
            existing = await db.execute(text("SELECT id FROM members WHERE phone=:ph"), {"ph": ph})
            if existing.fetchone():
                continue
            mid = str(uuid.uuid4())
            await db.execute(text("""
                INSERT INTO members (id, church_id, branch_id, first_name, last_name, phone, gender, marital_status, membership_status, membership_date, is_active, is_deleted, created_at, updated_at)
                VALUES (:id, :ch, :br, :fn, :ln, :ph, :g, :m, 'active', '2024-01-01', true, false, now(), now())
            """), {"id": mid, "ch": CHURCH_ID, "br": BRANCH_ID, "fn": fn, "ln": ln, "ph": ph, "g": gender, "m": marital})
            inserted += 1
        await db.commit()
        print(f"Inserted {inserted} new members")

        members = await db.execute(text("SELECT id, first_name FROM members WHERE church_id=:c AND is_deleted=false"), {"c": CHURCH_ID})
        rows = members.fetchall()
        print(f"Total members now: {len(rows)}")
        for r in rows:
            print(f"  {r.first_name} — {r.id}")

asyncio.run(seed())
