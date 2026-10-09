
from passlib.context import CryptContext

import app.main

from app.core.database import SessionLocal
from app.models.role import Role
from app.models.user import User


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)

db = SessionLocal()

try:
    admin_role = (
        db.query(Role)
        .filter(Role.name == "Admin")
        .first()
    )

    if admin_role is None:
        admin_role = Role(name="Admin")
        db.add(admin_role)
        db.commit()
        db.refresh(admin_role)

    user_role = (
        db.query(Role)
        .filter(Role.name == "User")
        .first()
    )

    if user_role is None:
        user_role = Role(name="User")
        db.add(user_role)
        db.commit()
        db.refresh(user_role)

    test_users = [
        (
            "College Admin",
            "admin@college.com",
            "admin123",
            admin_role.id,
        ),
        (
            "Test User",
            "testuser@gmail.com",
            "test123",
            user_role.id,
        ),
    ]

    for name, email, password, role_id in test_users:
        existing_user = (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

        if existing_user is None:
            existing_user = User(
                name=name,
                email=email,
                password=pwd_context.hash(password),
                role_id=role_id,
            )
            db.add(existing_user)
        else:
            existing_user.name = name
            existing_user.password = pwd_context.hash(password)
            existing_user.role_id = role_id

    db.commit()
    print("GitHub Actions test data prepared successfully.")

finally:
    db.close()