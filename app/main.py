from datetime import date

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from passlib.context import CryptContext

from app.core.database import Base, engine, SessionLocal
from app.models import (
    role,
    user,
    tree,
    location as location_model,
    plantation,
    growth_record,
)

# =========================================================
# CREATE FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="Tree Plantation Tracking Platform",
    description="Backend API for tracking tree plantations",
    version="1.0.0",
)

# =========================================================
# CORS
# Allows React frontend to communicate with FastAPI
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================================
# SESSION SUPPORT
# =========================================================

app.add_middleware(
    SessionMiddleware,
    secret_key="tree-plantation-secret-key",
    same_site="lax",
    https_only=False,
)

# =========================================================
# CREATE DATABASE TABLES
# =========================================================

Base.metadata.create_all(bind=engine)

# =========================================================
# PASSWORD HASHING
# =========================================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)

# =========================================================
# ROOT / API CHECK
# =========================================================

@app.get("/")
def home():
    return {
        "message": "Tree Plantation Tracking Platform API is running",
        "status": "success",
    }


# =========================================================
# REGISTER USER
# =========================================================

@app.post("/register")
def register(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
):
    db = SessionLocal()

    try:
        # Check whether email already exists
        existing_user = (
            db.query(user.User)
            .filter(user.User.email == email)
            .first()
        )

        if existing_user:
            return JSONResponse(
                content={
                    "success": False,
                    "message": "Email already registered",
                },
                status_code=400,
            )

        # Find the normal User role
        user_role = (
            db.query(role.Role)
            .filter(role.Role.name == "User")
            .first()
        )

        if not user_role:
            return JSONResponse(
                content={
                    "success": False,
                    "message": "User role not found",
                },
                status_code=500,
            )

        # Hash password
        hashed_password = pwd_context.hash(password)

        # Create new user
        new_user = user.User(
            name=name,
            email=email,
            password=hashed_password,
            role_id=user_role.id,
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "success": True,
            "message": "Registration successful",
            "user_id": new_user.id,
        }

    except Exception as error:
        db.rollback()

        return JSONResponse(
            content={
                "success": False,
                "message": "Registration failed",
                "error": str(error),
            },
            status_code=500,
        )

    finally:
        db.close()


# =========================================================
# LOGIN
# =========================================================

@app.post("/login")
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
):
    db = SessionLocal()

    try:
        user_data = (
            db.query(user.User)
            .filter(user.User.email == email)
            .first()
        )

        # Check user and password
        if user_data and pwd_context.verify(
            password,
            user_data.password,
        ):
            # Store login information in session
            request.session["user_id"] = user_data.id
            request.session["user_name"] = user_data.name
            request.session["role_id"] = user_data.role_id

            return JSONResponse(
                content={
                    "success": True,
                    "message": "Login successful",
                    "user_id": user_data.id,
                    "user_name": user_data.name,
                    "role_id": user_data.role_id,
                }
            )

        return JSONResponse(
            content={
                "success": False,
                "message": "Invalid email or password",
            },
            status_code=401,
        )

    finally:
        db.close()


# =========================================================
# LOGOUT
# =========================================================

@app.post("/logout")
def logout(request: Request):
    request.session.clear()

    return {
        "success": True,
        "message": "Logged out successfully",
    }


# =========================================================
# GET CURRENT USER
# =========================================================

@app.get("/me")
def get_current_user(request: Request):

    if "user_id" not in request.session:
        return JSONResponse(
            content={
                "logged_in": False,
                "message": "User is not logged in",
            },
            status_code=401,
        )

    return {
        "logged_in": True,
        "user_id": request.session.get("user_id"),
        "user_name": request.session.get("user_name"),
        "role_id": request.session.get("role_id"),
    }


# =========================================================
# GET LOCATIONS
# =========================================================

@app.get("/locations")
def get_locations():

    db = SessionLocal()

    try:
        locations = (
            db.query(location_model.Location)
            .order_by(location_model.Location.id)
            .all()
        )

        return [
            {
                "id": location.id,
                "name": location.location_name,
            }
            for location in locations
        ]

    finally:
        db.close()


# =========================================================
# PLANT A TREE
# =========================================================

@app.post("/plant-tree")
def plant_tree(
    request: Request,
    tree_name: str = Form(...),
    location_id: int = Form(...),
    planting_date: str = Form(...),
):

    # Check login
    if "user_id" not in request.session:
        return JSONResponse(
            content={
                "success": False,
                "message": "Please login first",
            },
            status_code=401,
        )

    db = SessionLocal()

    try:

        # -------------------------------------------------
        # Check whether the tree already exists
        # -------------------------------------------------

        existing_tree = (
            db.query(tree.Tree)
            .filter(tree.Tree.tree_name == tree_name)
            .first()
        )

        if existing_tree:
            tree_data = existing_tree

        else:
            tree_data = tree.Tree(
                tree_name=tree_name
            )

            db.add(tree_data)
            db.commit()
            db.refresh(tree_data)

        # -------------------------------------------------
        # Create plantation record
        # -------------------------------------------------

        plantation_data = plantation.Plantation(
            user_id=request.session["user_id"],
            tree_id=tree_data.id,
            location_id=location_id,
            planting_date=date.fromisoformat(planting_date),
        )

        db.add(plantation_data)
        db.commit()
        db.refresh(plantation_data)

        return {
            "success": True,
            "message": "Tree planted successfully!",
            "plantation_id": plantation_data.id,
            "tree_id": tree_data.id,
        }

    except ValueError:
        db.rollback()

        return JSONResponse(
            content={
                "success": False,
                "message": "Invalid planting date",
            },
            status_code=400,
        )

    except Exception as error:
        db.rollback()

        return JSONResponse(
            content={
                "success": False,
                "message": "Could not plant the tree",
                "error": str(error),
            },
            status_code=500,
        )

    finally:
        db.close()


# =========================================================
# DASHBOARD DATA
# =========================================================

@app.get("/dashboard")
def dashboard(request: Request):

    # Check login
    if "user_id" not in request.session:
        return JSONResponse(
            content={
                "success": False,
                "message": "Please login first",
            },
            status_code=401,
        )

    db = SessionLocal()

    try:

        # Total plantations / trees planted
        total_trees = (
            db.query(plantation.Plantation)
            .count()
        )

        # Total users
        total_users = (
            db.query(user.User)
            .count()
        )

        # Total locations
        total_locations = (
            db.query(location_model.Location)
            .count()
        )

        return {
            "success": True,
            "user_name": request.session.get("user_name"),
            "trees_planted": total_trees,
            "total_users": total_users,
            "total_locations": total_locations,
        }

    finally:
        db.close()


# =========================================================
# GET PLANTATION RECORDS
# =========================================================

@app.get("/plantations")
def get_plantations(request: Request):

    if "user_id" not in request.session:
        return JSONResponse(
            content={
                "success": False,
                "message": "Please login first",
            },
            status_code=401,
        )

    db = SessionLocal()

    try:

        plantations = (
            db.query(plantation.Plantation)
            .order_by(
                plantation.Plantation.id.desc()
            )
            .all()
        )

        result = []

        for record in plantations:

            tree_data = (
                db.query(tree.Tree)
                .filter(tree.Tree.id == record.tree_id)
                .first()
            )

            location_data = (
                db.query(location_model.Location)
                .filter(
                    location_model.Location.id
                    == record.location_id
                )
                .first()
            )

            user_data = (
                db.query(user.User)
                .filter(user.User.id == record.user_id)
                .first()
            )

            result.append(
                {
                    "id": record.id,
                    "tree_name": (
                        tree_data.tree_name
                        if tree_data
                        else "Unknown"
                    ),
                    "location": (
                        location_data.location_name
                        if location_data
                        else "Unknown"
                    ),
                    "planted_by": (
                        user_data.name
                        if user_data
                        else "Unknown"
                    ),
                    "planting_date": str(
                        record.planting_date
                    ),
                }
            )

        return {
            "success": True,
            "plantations": result,
        }

    finally:
        db.close()