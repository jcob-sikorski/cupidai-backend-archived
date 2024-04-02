from fastapi import FastAPI
from web import deepfake, file, user

app = FastAPI()

app.include_router(user.router)
app.include_router(file.router)
app.include_router(deepfake.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app",
        host="localhost", port=8000, reload=True)