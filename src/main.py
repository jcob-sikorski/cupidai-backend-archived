from fastapi import FastAPI

import uvicorn

from web import (
    account, ai_verification, billing, bug, deepfake, earnings,
    file, history, mdj_progress, referral, social_account, team,
    two_factor_auth, usage, user
)


app = FastAPI()

app.include_router(account.router)
app.include_router(ai_verification.router)
app.include_router(billing.router)
app.include_router(bug.router)
app.include_router(deepfake.router)
app.include_router(earnings.router)
app.include_router(file.router)
app.include_router(history.router)
app.include_router(mdj_progress.router)
app.include_router(referral.router)
app.include_router(social_account.router)
app.include_router(team.router)
app.include_router(two_factor_auth.router)
app.include_router(usage.router)
app.include_router(user.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app",
        host="localhost", port=8000, reload=True)