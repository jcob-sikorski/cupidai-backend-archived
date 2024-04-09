from fastapi import APIRouter, Depends

from model.image_generation import Settings

from comfyui import generate_workflow

def generate(settings: Settings, user_id: str) -> None:
    # 1. based on the json settings create the request using the compiler for json
    workflow_json = generate_workflow(settings)

    pass


sample_settings = {
    # basic settings are for the first efficient loader
    "basic_preset": "preset_1",
    "pos_prompt_enabled": False,
    "basic_pos_text_prompt": "Pos text prompt", ✅
    "basic_neg_text_prompt": "Negative text prompt", ✅
    "basic_sampling_steps": 10, ✅
    "basic_sampler_method": "euler_ancestral", ✅
    "basic_model": "model_1", ✅
    "basic_width": 800, ✅
    "basic_height": 600, ✅
    "basic_cfg_scale": 0.5, ✅
    "basic_batch_size": 32, ✅
    "basic_batch_count": 5,
    "basic_denoise": 0.3, ✅

    "ipa_1_enabled": True,
    "ipa_1_model": "ipa_model_1",
    "ipa_1_reference_image": "ipa_reference_image_1",
    "ipa_1_weight": 0.7,
    "ipa_1_noise": 0.2,
    "ipa_1_start_at": 0.0,
    "ipa_1_end_at": 1.0,

    "ipa_2_enabled": False,
    "ipa_2_model": "",
    "ipa_2_reference_image": "",
    "ipa_2_weight": 0.0,
    "ipa_2_noise": 0.0,
    "ipa_2_start_at": 0.0,
    "ipa_2_end_at": 0.0,

    "refinement_seed": 12345,
    "refinement_steps": 20,
    "refinement_cfg_scale": 0.7,
    "refinement_denoise": 0.4,
    "refinement_sampler": "sampler_1",
    "refinement_checkpoint": "checkpoint_1",

    "lora_count": 3,
    "lora_models": ["lora_model_1", "lora_model_2", "lora_model_3"],
    "lora_strengths": [0.5, 0.6, 0.7],
    "lora_enabled": [True, False, True],

    "controlnet_model": "controlnet_model_1",
    "controlnet_reference_image": "controlnet_reference_image_1",
    "controlnet_strength": 0.8,
    "controlnet_start_at": 0.0,
    "controlnet_end_at": 1.0,
}
