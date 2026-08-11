from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext

from app.core.database import Base, engine, SessionLocal
from app.models import role, user, tree, location, plantation, growth_record


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={}
    )


@app.post("/login", response_class=HTMLResponse)
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):
    db = SessionLocal()

    user_data = db.query(user.User).filter(
        user.User.email == email
    ).first()

    if user_data and pwd_context.verify(password, user_data.password):
        user_name = user_data.name
        db.close()

        return templates.TemplateResponse(
            request=request,
            name="dashboard.html",
            context={"user_name": user_name}
        )

    db.close()

    return HTMLResponse(
        content="<h3>Invalid email or password</h3><a href='/'>Go back</a>",
        status_code=401
    )