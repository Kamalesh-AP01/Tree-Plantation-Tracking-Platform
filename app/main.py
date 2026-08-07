from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Tree Plantation Tracking Platform"}
