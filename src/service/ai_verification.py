from fastapi import HTTPException

import httpx
import os

import data.ai_verification as data

from model.ai_verification import Settings, Prompt, Progress, Response

from model.user import User

from error import NotAutorized

MIDJOURNEY_TOKEN = os.getenv("MIDJOURNEY_TOKEN")

def webhook(progress: Progress) -> None:
    data.update_progress(progress)

def create_prompt_string(prompt: Prompt) -> str:
    attributes = ["prompt", "generation_speed", "engine_version", "style", "aspect_ratio", "step_stop", "stylize", "seed"]
    prompt_string = " ".join([str(getattr(prompt, attr)) for attr in attributes if getattr(prompt, attr) is not None])
    return prompt_string

async def imagine(prompt: Prompt, user: User) -> Response:
    if data.has_permissions(user):
        # docs: (https://docs.midjourney.com/docs/)
        #
        # prompt: image_urls (optional) text_prompt parameters (--parameter1 --parameter2)
        # parameters:
        # - generation speed: --fast --turbo or --relax  ; paramters are only available for the pro or mega plan - call the api before doing the actual call
        # - engine version: --version x    ; accepts the values 1, 2, 3, 4, 5, 5.0, 5.1, 5.2, and 6.
        # - style: --style raw  ; Model Versions 6, 5.2, 5.1 and Niji 6 accept this parameter
        # - aspect ratio: --aspect x:y  ; where x and y are numbers for all the ratios
        # - step/stop:   ????
        # - stylize: --stylize x   ; default value is 100 and accepts integer values 0–1000
        # - seed: --seed x  ; accepts whole numbers 0–4294967295

        url = "https://api.mymidjourney.ai/api/v1/midjourney/imagine"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {MIDJOURNEY_TOKEN}",
        }
        data = {
            "prompt": create_prompt_string(prompt),
            "ref": user.id,
            "webhookOverride": "http://194.15.120.110/ai-verification/webhook"
        }

        async with httpx.AsyncClient() as client:
            resp = await client.post(url, headers=headers, json=data)
            response_data = Response.parse_raw(resp.text)

        if response_data.success:
            data.update_usage(user)

        if resp.status_code != 200 or response_data.error:
            raise HTTPException(status_code=400, detail="Imagine failed")
        
        return response_data
    else:
        raise NotAutorized(msg=f"Invalid permissions")
    
async def faceswap(source_uri: str, target_uri: str, user: User) -> Response:
    if data.has_permissions(user):
        url = "https://api.mymidjourney.ai/api/v1/midjourney/faceswap"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {MIDJOURNEY_TOKEN}",
        }
        data = {
            "source": source_uri,
            "target": target_uri,
            "ref": user.id,
            "webhookOverride": "http://194.15.120.110/ai-verification/webhook"
        }

        async with httpx.AsyncClient() as client:
            resp = await client.post(url, headers=headers, json=data)
            response_data = Response.parse_raw(resp.text)

        if response_data.success:
            data.update_usage(user)

        if resp.status_code != 200 or response_data.error:
            raise HTTPException(status_code=400, detail="Faceswap failed")
        
        return response_data
    else:
        raise NotAutorized(msg=f"Invalid permissions")
    
async def action(message_id: str, button: str, user: User) -> Response:
    if data.has_permissions(user):
        url = "https://api.mymidjourney.ai/api/v1/midjourney/button"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {MIDJOURNEY_TOKEN}",
        }
        data = {
            "message_id": message_id,
            "button": button,
            "ref": user.id,
            "webhookOverride": "http://194.15.120.110/ai-verification/webhook"
        }

        async with httpx.AsyncClient() as client:
            resp = await client.post(url, headers=headers, json=data)
            response_data = Response.parse_raw(resp.text)

        if response_data.success:
            data.update_usage(user)

        if resp.status_code != 200 or response_data.error:
            raise HTTPException(status_code=400, detail="Action failed")
        
        return response_data
    else:
        raise NotAutorized(msg=f"Invalid permissions")
    
async def cancel_job(message_id: str, user: User) -> Response:
    url = "https://api.mymidjourney.ai/api/v1/midjourney/button"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {MIDJOURNEY_TOKEN}",
    }
    data = {
        "message_id": message_id,
        "button": "Cancel Job",
        "ref": user.id,
        "webhookOverride": "http://194.15.120.110/ai-verification/webhook"
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post(url, headers=headers, json=data)
        response_data = Response.parse_raw(resp.text)

    if resp.status_code != 200 or response_data.error:
        raise HTTPException(status_code=400, detail="Action failed")
        
    return response_data

# def update_settings(settings: Settings, user: User) -> :
#     data.update_settings(settings, user)