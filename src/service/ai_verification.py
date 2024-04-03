from fastapi import HTTPException

import httpx
import os

import data.ai_verification as data

from model.ai_verification import Prompt, Progress, ImagineResponse

from model.user import User

from error import NotAutorized

MIDJOURNEY_TOKEN = os.getenv("MIDJOURNEY_TOKEN")

def imagine_webhook(progress: Progress) -> None:
    data.update_progress_imagine(progress)

def create_prompt_string(prompt: Prompt) -> str:
    attributes = ["prompt", "generation_speed", "engine_version", "style", "aspect_ratio", "step_stop", "stylize", "seed"]
    prompt_string = " ".join([str(getattr(prompt, attr)) for attr in attributes if getattr(prompt, attr) is not None])
    return prompt_string

async def imagine(prompt: Prompt, user: User) -> ImagineResponse:
    if data.has_permissions_imagine(user):
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
            "webhookOverride": "http://194.15.120.110/ai-verification/imagine-webhook"
        }

        async with httpx.AsyncClient() as client:
            resp = await client.post(url, headers=headers, json=data)
            response_data = ImagineResponse.parse_raw(resp.text)

        if response_data.success:
            data.update_usage_imagine(user)

        if resp.status_code != 200 or response_data.error:
            raise HTTPException(status_code=400, detail="Image generation failed")
        
        return response_data
    else:
        raise NotAutorized(msg=f"Invalid permissions")