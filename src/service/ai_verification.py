import httpx
import os

import data.ai_verification as data

from model.ai_verification import TextToImage, GeneratedImage

from model.user import User

from error import NotAutorized

MIDJOURNEY_TOKEN = os.getenv("MIDJOURNEY_TOKEN")

async def text_to_image(prompt: TextToImage, user: User) -> GeneratedImage:
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

        # TODO call the api and provide with it a webhook url
        # TODO set up the webhook which can receive the responses about the progress and update the db
        # TODO on successful run update the usage
        url = "https://api.mymidjourney.ai/api/v1/midjourney/imagine"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {MIDJOURNEY_TOKEN}",
        }
        data = {
            "prompt": ,
            "ref": ,
            "webhookOverride": 
        }

        # TODO are waiting here for the response or what?
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, headers=headers, json=data)

        if resp.status_code != 200:
            raise HTTPException(status_code=400, detail="Image generation failed")

        # TODO what are we returning here?
        return {"url": resp.json()["image_url"]}
    else:
        raise NotAutorized(msg=f"Invalid permissions")