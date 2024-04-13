from typing import Dict, List, Optional

import re

import httpx

from error import NotAuthorized

from comfyui.ModelInterface import generate_workflow

import data.image_generation as data

from model.image_generation import Settings, Message

import service.billing as billing_service
import service.history as history_service

def webhook(message: Message) -> None:
    print(message)
    update_message(user_id=message.user_id, message_id=message.message_id, status=message.status, s3_uris=message.s3_uris)

    # TODO: this should only run once when the image generation completed successfully
    history_service.update('image_generation', message.user_id)

def check_settings(settings: Settings):
    samplers = [
        "euler",
        "euler_ancestral",
        "heun",
        "heunpp2",
        "dpm_2",
        "dpm_2_ancestral",
        "Ims",
        "dpm_fast",
        "dpm_adaptive",
        "dpmpp_2s_ancestral",
        "dpmpp_sde",
        "dpmpp_sde_gpu",
        "dpmpp_2m",
        "dpmpp_2m_sde",
        "dpmpp_2m_sde_gpu",
        "dpmpp_3m_sde",
        "dpmpp_3m_sde_gpu",
        "ddpm",
        "1cm",
        "ddim",
        "uni_pc",
        "uni_pc_bh2"
    ]

    checkpoint_models = [
        'amIReal_V44.safetensors', 
        'analogMadness_v60.safetensors', 
        'chilloutmix_NiPrunedFp32Fix.safetensors', 
        'consistentFactor_euclidV61.safetensors', 
        'devlishphotorealism_v40.safetensors', 
        'edgeOfRealism_eorV20Fp16BakedVAE.safetensors', 
        'epicphotogasm_lastUnicorn.safetensors', 
        'epicrealism_naturalSinRC1.safetensors', 
        'epicrealism_newCentury.safetensors', 
        'juggernaut_reborn.safetensors', 
        'metagodRealRealism_v10.safetensors', 
        'realismEngineSDXL_v10.safetensors', 
        'realisticVisionV51_v51VAE.safetensors', 
        'stablegramUSEuropean_v21.safetensors', 
        'uberRealisticPornMerge_urpmv13.safetensors', 
        'v1-5-pruned-emaonly.ckpt'
    ]

    lora_models = [
        "add_detail",
        "age_slider_v20",
        "analogFilmPhotography_10",
        "beard_slider_v10",
        "breasts_slider_v10",
        "clothing_slider_v19_000000030",
        "contrast_slider_v10",
        "curly_hair_slider_v1",
        "DarkLighting",
        "depth_of_field_slider_v1",
        "detail_slider_v4",
        "emotion_happy_slider_v1",
        "epiNoiseoffset_v2",
        "eyebrows_slider_v2",
        "filmgrain_slider_v1",
        "fisheye_slider_v10",
        "gender_slider_v1",
        "lora_perfecteyes_v1_from_v1_160",
        "muscle_slider_v1",
        "people_count_slider_v1",
        "skin_tone_slider_v1",
        "time_slider_v1",
        "Transparent_Clothes_V2",
        "weight_slider_v2"
    ]
    
    if settings.basic_sampling_steps is not None and settings.basic_sampling_steps > 120:
        return
    if settings.basic_sampler_method is not None and settings.basic_sampler_method not in samplers:
        return
    if settings.basic_model is not None and settings.basic_model not in checkpoint_models:
        return
    if settings.basic_cfg_scale is not None and settings.basic_cfg_scale > 100.0:
        return
    if settings.basic_batch_size is not None and not (1 <= settings.basic_batch_size <= 8):
        return
    if settings.basic_batch_count is not None and not (1 <= settings.basic_batch_count <= 4):
        return
    if settings.basic_denoise is not None and settings.basic_denoise > 1.0:
        return
    if settings.ipa_1_model is not None and settings.ipa_1_model not in checkpoint_models:
        return
    if settings.ipa_1_weight is not None and settings.ipa_1_weight < 1.0:
        return
    if settings.ipa_1_noise is not None and settings.ipa_1_noise > 1.0:
        return
    if settings.ipa_1_start_at is not None and settings.basic_sampling_steps and not (settings.basic_sampling_steps > settings.ipa_1_start_at):
        return
    if settings.ipa_1_end_at is not None and settings.basic_sampling_steps and not (settings.basic_sampling_steps >= settings.ipa_1_end_at):
        return
    if settings.ipa_2_model is not None and settings.ipa_2_model not in checkpoint_models:
        return
    if settings.ipa_2_weight is not None and settings.ipa_2_weight > 1.0:
        return
    if settings.ipa_2_noise is not None and settings.ipa_2_noise > 1.0:
        return
    if settings.ipa_2_start_at is not None and settings.basic_sampling_steps and not (settings.basic_sampling_steps > settings.ipa_2_start_at):
        return
    if settings.ipa_2_end_at is not None and settings.basic_sampling_steps and not (settings.basic_sampling_steps >= settings.ipa_2_end_at):
        return
    if settings.refinement_steps is not None and settings.refinement_steps > 120:
        return
    if settings.refinement_cfg_scale is not None and settings.refinement_cfg_scale > 100.0:
        return
    if settings.refinement_denoise is not None and settings.refinement_denoise > 1.0:
        return
    if settings.refinement_sampler is not None and settings.refinement_sampler not in samplers:
        return
    if settings.lora_count is not None and not (1 <= settings.lora_count <= 4):
        return
    if settings.lora_model is not None and settings.lora_model not in lora_models:
        return
    if settings.lora_strengths is not None and all(map(lambda x: x <= 10.0, settings.lora_strengths)):
        return
    if settings.controlnet_model is not None and settings.controlnet_model not in checkpoint_models:
        return
    if settings.controlnet_strength is not None and settings.controlnet_strength > 10.0:
        return
    if settings.controlnet_start_percent is not None and not (settings.controlnet_start_percent < 100.0):
        return
    if settings.controlnet_end_percent is not None and not (settings.controlnet_end_percent <= 100.0):
        return

def save_settings(settings: Settings):
    return data.save_settings(settings)

def update_message(user_id: str, status: Optional[str] = None, uploadcare_uris: Optional[Dict[str, str]] = None, message_id: Optional[str] = None, settings_id: Optional[str] = None, s3_uris: Optional[List[str]] = None):
    return data.update_message(user_id, status, uploadcare_uris, message_id, settings_id, s3_uris)

def extract_id_from_uri(uri):
    # Use regex to extract the UUID from the URI
    match = re.search(r"/([a-f0-9-]+)/-/", uri)
    if match:
        return match.group(1)
    else:
        return None

async def generate(settings: Settings, uploadcare_uris: Dict[str, str], user_id: str) -> None:
    if billing_service.has_permissions('image_generation', user_id):
        image_ids = {key: extract_id_from_uri(uri) for key, uri in uploadcare_uris.items()}

        settings_id = save_settings(settings)

        message_id = update_message(user_id, "started", uploadcare_uris, None, settings_id, None)

        workflow_json = generate_workflow(settings, image_ids)

        if workflow_json is None:
            update_message(user_id, message_id, "failed")
            return None

        # Define the URL of the server
        url = "https://native-goat-saved.ngrok-free.app/"

        # Define the headers for the request
        headers = {
            'Content-Type': 'application/json'
        }

        # Define the payload for the request
        payload = {
            'workflow': workflow_json,
            'uploadcare_uris': uploadcare_uris,
            'image_ids': image_ids,
            'message_id': message_id,
            'settings_id': settings_id,
            'user_id': user_id
        }

        # Send the POST request
        async with httpx.AsyncClient() as client:
            await client.post(url, headers=headers, json=payload)
    else:
        raise NotAuthorized(msg=f"Invalid permissions")