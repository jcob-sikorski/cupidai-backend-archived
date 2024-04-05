from fastapi import APIRouter, Depends

from auth import VerifyToken

router = APIRouter(prefix = "/billing")

auth = VerifyToken()

@router.get("/download-history", status_code=200)  # Downloads billing history

@router.get("/history", status_code=200)  # Retrieves billing history

@router.patch("/pay-with-coinbase", status_code=200)  # Pays using Coinbase for billing

@router.post("/terms-of-service", status_code=201)  # Accepts terms of service for billing

@router.get("/current-plan", status_code=200)  # Retrieves current billing plan

@router.post("/", status_code=201)  # Creates a new billing record, status 201 for Created