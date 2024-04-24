from fastapi import FastAPI
from dotenv import load_dotenv
import uvicorn
import sys

from web import (
    account, ai_verification, billing, bug, deepfake,
    history, image_generation, midjourney, referral, social_account, 
    team
)

def load_env_file(environment):
    """Load environment variables from corresponding file"""

    if environment == "production":
        dotenv_path = ".env.production"
    elif environment == "development":
        dotenv_path = ".env.development"
    else:
        raise ValueError("Invalid environment specified")

    load_dotenv(dotenv_path)

environment = sys.argv[1] if len(sys.argv) > 1 else "development"
load_env_file(environment)

app = FastAPI()

app.include_router(account.router)
app.include_router(ai_verification.router)
app.include_router(billing.router)
app.include_router(bug.router)
app.include_router(deepfake.router)
app.include_router(history.router)
app.include_router(image_generation.router)
app.include_router(midjourney.router)
app.include_router(referral.router)
app.include_router(social_account.router)
# app.include_router(team.router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=(environment == "development"))