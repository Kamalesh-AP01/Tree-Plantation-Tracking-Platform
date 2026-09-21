from app.models import user


def get_user_by_email(db, email):
    return (
        db.query(user.User)
        .filter(user.User.email == email)
        .first()
    )