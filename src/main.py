from fastapi import FastAPI
from web import ai_verification, deepfake, user

app = FastAPI()

app.include_router(ai_verification.router)
app.include_router(deepfake.router)
app.include_router(user.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app",
        host="localhost", port=8000, reload=True)