from typing import List, Dict, Optional
from pydantic import BaseModel

class Settings(BaseModel):
    # Basic settings (mandatory)
    basic_preset: str
    pos_prompt_enabled: bool
    basic_pos_text_prompt: str
    basic_neg_text_prompt: str
    basic_sampling_steps: int
    basic_sampler_method: str
    basic_model: str
    basic_width: int
    basic_height: int
    basic_cfg_scale: float
    basic_batch_size: int
    basic_batch_count: int
    basic_denoise: float

    # IPA 1 settings (optional)
    ipa_1_enabled: bool = False
    ipa_1_model: Optional[str] = None
    ipa_1_reference_image: Optional[str] = None # TODO: map image_uris to the image path
    ipa_1_weight: Optional[float] = None
    ipa_1_noise: Optional[float] = None
    ipa_1_start_at: Optional[float] = None
    ipa_1_end_at: Optional[float] = None

    # IPA 2 settings (optional)
    ipa_2_enabled: bool = False
    ipa_2_model: Optional[str] = None
    ipa_2_reference_image: Optional[str] = None # TODO: map image_uris to the image path
    ipa_2_weight: Optional[float] = None
    ipa_2_noise: Optional[float] = None
    ipa_2_start_at: Optional[float] = None
    ipa_2_end_at: Optional[float] = None

    # Refinement settings (optional)
    refinement_enabled: bool = False
    refinement_seed: Optional[int] = None
    refinement_steps: Optional[int] = None
    refinement_cfg_scale: Optional[float] = None
    refinement_denoise: Optional[float] = None
    refinement_sampler: Optional[str] = None

    # Lora settings (optional)
    lora_count: Optional[int] = None
    lora_models: Optional[List[str]] = None
    lora_strengths: Optional[List[float]] = None
    lora_enabled: bool = False

    # ControlNet settings (optional)
    controlnet_enabled: bool = False
    controlnet_model: Optional[int] = None
    controlnet_reference_image: Optional[str] = None # TODO: map image_uris to the image path
    controlnet_strength: Optional[float] = None
    controlnet_start_at: Optional[float] = None
    controlnet_end_at: Optional[float] = None

class Message(BaseModel):
    user_id: Optional[str]
    status: Optional[str]
    image_uris: Optional[Dict[str, str]]
    created_at: Optional[str]
    settings_id: Optional[str]
    uploadcare_uuids: Optional[List[str]]