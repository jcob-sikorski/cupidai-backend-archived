from fastapi import APIRouter, Depends



router = APIRouter(prefix = "/referral")

# @router.post("/links/", status_code=201)  # Generates a new link

# @router.get("/links/{link_id}", status_code=200)  # Retrieves a specific link

# @router.post("/payouts/request", status_code=201)  # Requests a payout

# @router.get("/payouts/{payout_id}", status_code=200)  # Retrieves a specific payout

# @router.get("/statistics", status_code=200)  # Retrieves statistics

# @router.get("/payouts/history", status_code=200)  # Retrieves payout history