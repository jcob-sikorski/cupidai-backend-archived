uploadcarefrom typing import List, Dict, Optional
from pydantic import BaseModel

class Settings(BaseModel):
    # Basic settings (mandatory)
    basic_preset: str
    pos_prompt_enabled: bool
    basic_pos_text_prompt: str
    basic_neg_text_prompt: str
    basic_sampling_steps: int # max is 120
    basic_sampler_method: str # methods from comfy
    basic_model: str # in checkpoint txt
    basic_width: int
    basic_height: int
    basic_cfg_scale: float  # check in comfy
    basic_batch_size: int # range is 1-8
    basic_batch_count: int # range is 1-4
    basic_denoise: float # check in comfy

    # IPA 1 settings (optional)
    ipa_1_enabled: bool = False
    ipa_1_model: Optional[str] = None # in checkpoint txt
    ipa_1_reference_image: Optional[str] = None
    ipa_1_weight: Optional[float] = None # in checkpoint txt
    ipa_1_noise: Optional[float] = None  # check in comfy
    ipa_1_start_at: Optional[float] = None # in range of sampling steps
    ipa_1_end_at: Optional[float] = None # in range of sampling steps

    # IPA 2 settings (optional)
    ipa_2_enabled: bool = False
    ipa_2_model: Optional[str] = None # in checkpoint txt
    ipa_2_reference_image: Optional[str] = None
    ipa_2_weight: Optional[float] = None # in checkpoint txt
    ipa_2_noise: Optional[float] = None  # check in comfy
    ipa_2_start_at: Optional[float] = None # in range of sampling steps
    ipa_2_end_at: Optional[float] = None # in range of sampling steps

    # Refinement settings (optional)
    refinement_enabled: bool = False
    refinement_seed: Optional[int] = None
    refinement_steps: Optional[int] = None # max is 120
    refinement_cfg_scale: Optional[float] = None # check in comfy
    refinement_denoise: Optional[float] = None # check in comfy
    refinement_sampler: Optional[str] = None # check in comfy

    # Lora settings (optional)
    lora_count: Optional[int] = None # range is 1-4
    lora_models: Optional[List[str]] = None # in lora txt
    lora_strengths: Optional[List[float]] = None # check in comfy
    lora_enabled: List[bool] = [False, False, False, False]

    # ControlNet settings (optional)
    controlnet_enabled: bool = False
    controlnet_model: Optional[int] = None # in checkpoint txt
    controlnet_reference_image: Optional[str] = None
    controlnet_strength: Optional[float] = None # check in comfy
    controlnet_start_at: Optional[float] = None # in the range of smapling steps
    controlnet_end_at: Optional[float] = None

class Message(BaseModel):
    user_id: Optional[str]
    status: Optional[str]
    uploadcare_uris: Optional[Dict[str, str]]
    created_at: Optional[str]
    settings_id: Optional[str]
    s3_uris: Optional[List[str]]