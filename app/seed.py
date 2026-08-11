from app.core.database import SessionLocal, Base, engine
from app.models.role import Role
from app.models.location import Location
from app.models.user import User
from passlib.context import CryptContext

Base.metadata.create_all(bind=engine)

db = SessionLocal()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


admin_role = db.query(Role).filter(Role.name == "Admin").first()

if not admin_role:
    admin_role = Role(name="Admin")
    db.add(admin_role)
    db.commit()
    db.refresh(admin_role)


locations = [
    "Backside Canteen",
    "PT Ground",
    "Backside Cafe",
    "Hostel Boys Area",
    "Hostel Girls Area"
]

for location_name in locations:
    existing_location = db.query(Location).filter(
        Location.location_name == location_name
    ).first()

    if not existing_location:
        db.add(Location(location_name=location_name))

db.commit()


existing_admin = db.query(User).filter(
    User.email == "admin@college.com"
).first()

if not existing_admin:
    admin_user = User(
        name="College Admin",
        email="admin@college.com",
        password=pwd_context.hash("admin123"),
        role_id=admin_role.id
    )

    db.add(admin_user)
    db.commit()


db.close()

print("Seed data added successfully.")