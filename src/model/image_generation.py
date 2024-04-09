from typing import List
from pydantic import BaseModel

class Settings(BaseModel):
    settings_id: str
    # basic settings
    basic_preset: str
    basic_post_text_prompt: str
    basic_neg_text_prompt: str
    basic_sampling_steps: int
    basic_model: str
    basic_width: int
    basic_height: int
    basic_cfg_scale: float
    basic_batch_size: int
    basic_batch_count: int
    basic_denoise: float

    # ipa 1 settings
    ipa_1_enabled: bool
    ipa_1_model: str
    ipa_1_reference_image: str
    ipa_1_weight: float
    ipa_1_noise: float
    ipa_1_start_at: float
    ipa_1_end_at: float

    # ipa 2 settings
    ipa_2_enabled: bool
    ipa_2_model: str
    ipa_2_reference_image: str
    ipa_2_weight: float
    ipa_2_noise: float
    ipa_2_start_at: float
    ipa_2_end_at: float

    # refinement settings
    refinement_seed: int
    refinement_steps: int
    refinement_cfg_scale: float
    refinement_denoise: float
    refinement_sampler: str
    refinement_checkpoint: str

    # lora settings
    lora_count: int
    lora_models: List[str]
    lora_strengths: List[float]
    lora_enabled: List[bool]

    # controlnet settings
    controlnet_model: str
    controlnet_reference_image: str
    controlnet_strength: float
    controlnet_start_at: float
    controlnet_end_at: float

class Message(BaseModel):
    message_id: str
    user_id: str
    status: str
    image_uris: List[str]
    created_at: str
    settings_id: str