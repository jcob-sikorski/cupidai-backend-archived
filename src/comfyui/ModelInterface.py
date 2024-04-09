from typing import List

import importlib
import json

class ModelInterface():
    def __init__(self):
        self.open_pose_dwp = self.load_json("open_pose_dwp")
        self.canny = self.load_json("canny")
        self.midas_depth_map = self.load_json("midas_depth_map")
        self.ip2p = self.load_json("ip2p")
        self.lora_stacker = self.load_json("lora_stacker")
        self.image_size = self.load_json("image_size")
        self.get_image_size = self.load_json("get_image_size")
        self.random_prompts = self.load_json("random_prompts")
        self.ipa1 = self.load_json("ipa1")
        self.ipa2 = self.load_json("ipa2")
        self.efficient_loader = self.load_json("efficient_loader")
        self.ksampler_efficient1 = self.load_json("ksampler_efficient1")
        self.ksampler_efficient2 = self.load_json("ksampler_efficient2")

        self.used_components = set()

    def load_json(self, unit_name: str):
        # Import the JSON dictionary directly without decoding
        try:
            # Assuming all JSON data is stored in the JSONEngine module
            module = importlib.import_module("JSONEngine")
            json_dict = getattr(module, unit_name)
            # Directly return the dictionary without json.loads
            return json_dict
        except (ImportError, AttributeError) as e:
            print(f"Error processing unit {unit_name}: {str(e)}")
            return None

    def finalize(self):
        # Initialize an empty dictionary to hold the combined data
        combined_json = {}
        # Iterate through each used component
        for component in self.used_components:
            component_data = getattr(self, component, None)
            if isinstance(component_data, dict):
                # Merge the component's values into the combined_json
                for key, value in component_data.items():
                    combined_json[key] = value

        # Sort keys that are integer strings in ascending order
        combined_json_sorted = {}
        sorted_keys = sorted(combined_json.keys(), key=lambda x: int(x) if x.isdigit() else x)
        for key in sorted_keys:
            combined_json_sorted[key] = combined_json[key]

        return combined_json_sorted

    def connect_control_net(self, unit: int, image_path: str, strength: float = 1.0, start_percent: float = 0.0, end_percent: float = 1.0):
        """
        ################# CHOOSE CONTROLNET #################
        (Optional) Enable and choose ControlNet
        1. Select unit
        2. Then set the image path
        3. (Optional) set strength, set start percent, set end percent (0-1)
        4. Connect ControlNet to the cnet_stack in efficient loader
        """
        # Mapping unit numbers to unit names
        unit_names = {
            1: "open_pose_dwp",
            2: "midas_depth_map",
            3: "canny",
            4: "ip2p"
        }

        # Mapping unit names to their respective JSON keys
        json_keys = {
            "open_pose_dwp": ["210", "208"],
            "midas_depth_map": ["213", "211"],
            "canny": ["216", "214"],
            "ip2p": ["218", "217"]
        }

        # Select unit
        unit_name = unit_names.get(unit)
        
        # Get JSON keys based on unit name
        keys = json_keys.get(unit_name)
        
        json_dict = getattr(self, unit_name, "Variable not found")

        # Set image path
        json_dict[keys[0]]["inputs"]["image"] = image_path
        
        # Set strength, set start percent, set end percent (0-1)
        json_dict[keys[1]]["inputs"]["strength"] = strength
        json_dict[keys[1]]["inputs"]["start_percent"] = start_percent
        json_dict[keys[1]]["inputs"]["end_percent"] = end_percent

        self.used_components.add(unit_name)

        # Connect ControlNet to the cnet_stack in efficient loader
        self.efficient_loader["206"]["inputs"]["cnet_stack"] = [keys[1], 0]

    def choose_output_size(self, int1: int, int2: int, image_path: str = ""):
        """
        ################# CHOOSE OUTPUT SIZE #################
        (Optional) Choose image for size reference
        1. Set the output image size
        2. Connect the int1 to empty_latent_width in efficient loader
        3. Connect the int2 to empty_latent_height in efficient loader
        
        (Default) Choose height and width of the output image
        1. Set the int1 to empty_latent_width in efficient loader
        2. Connect the int2 to empty_latent_height in efficient loader
        """

        # set the output image size
        if image_path:
            self.used_components.discard("image_size")
            self.get_image_size["324"]["inputs"]["image"] = image_path
            self.used_components.add("get_image_size")
        else:
            self.used_components.discard("get_image_size")
            self.image_size["326"]["inputs"]["Number"] = int1
            self.image_size["327"]["inputs"]["Number"] = int2
            self.used_components.add("image_size")

        # Connect the int1, int2 to empty_latent_width/height in efficient loader
            
        self.efficient_loader["206"]["inputs"]["empty_latent_width"][0] = "325" if image_path else "326"
        self.efficient_loader["206"]["inputs"]["empty_latent_width"][1] = 0
    
        self.efficient_loader["206"]["inputs"]["empty_latent_height"][0] = "325" if image_path else "327"
        self.efficient_loader["206"]["inputs"]["empty_latent_height"][1] = 1 if image_path else 0

    def connect_lora(self, count: int, models: List[str], strengths: List[str], enabled: List[bool]):
        """
        ################# CONNECT LORA #################
        (Optional) Connect lora to Efficient Loader
        1. Connect lora to lora_stack in Efficient Loader
        """
        # Connect Lora to the lora_stack in efficient loader
        self.lora_stacker["207"]["inputs"]["lora_count"] = count

        for i in range(count):  # Assuming 'enabled' has 4 elements.
            if enabled[i]:
                index = i + 1
                self.lora_stacker["207"]["inputs"][f"lora_name_{index}"] = models[i]
                self.lora_stacker["207"]["inputs"][f"model_str_{index}"] = strengths[i]

        self.efficient_loader["206"]["inputs"]["lora_stack"] = ["207", 0]
        self.used_components.add("lora_stacker")

    def connect_random_prompts(self, positive_prompt: str):
        """
        ################# CONNECT RANDOM PROMPTS #################
        (Optional) Connect random prompts to the efficient loader
        1. Set the prompt
        2. Connect random prompts to the efficient loader as positive
        """
        # Set the pos prompt
        self.random_prompts["222"]["inputs"]["text"] = positive_prompt
        self.used_components.add("random_prompts")

        # Connect RandomPrompts to the efficient_loader
        self.efficient_loader["206"]["inputs"]["positive"] = ["222", 0]

    def set_up_efficient_loader(self, ckpt_name: str, negative_prompt: str):
        """
        ################# SET UP EFFICIENT LOADER #################
        (Default) Provide a configuration for the efficient loader
        1. Set the model
        2. Set the negative prompt
        3. (Optional) connect model to ApplyIpAdapter1
        4. (Default) connect model to model in KSamplerEfficient1
        """

        # Set the ckpt_name in efficient loader
        self.efficient_loader["206"]["inputs"]["ckpt_name"] = ckpt_name

        # Set the negative prompt in efficient loader
        self.efficient_loader["206"]["inputs"]["negative"] = negative_prompt

        self.used_components.add("efficient_loader")

    def set_up_ksampler_efficient1(self, seed: int, steps: int, cfg_scale: float, denoise: float, sampler: str, ipa1_enabled: bool = False):
        """
        ################# CONNECT KSAMPLER EFFICENT 2 #################
        """
        self.ksampler_efficient1["229"]["inputs"]["seed"] = seed
        self.ksampler_efficient1["229"]["inputs"]["steps"] = steps
        self.ksampler_efficient1["229"]["inputs"]["cfg"] = cfg_scale
        self.ksampler_efficient1["229"]["inputs"]["denoise"] = denoise
        self.ksampler_efficient1["229"]["inputs"]["sampler_name"] = sampler

        self.used_components.add("ksampler_efficient1")

        if not ipa1_enabled:
            # (Default) connect model to Efficient Loader model
            self.ksampler_efficient1["229"]["inputs"]["model"] = ["206", 0]


    def connect_ip_adapter_1(self, image_path: str, model: str, weight: int = 1, noise: int = 0, start_at: int = 0, end_at: int = 1):
        """
        ################# CONNECT IP ADAPTER 1 #################
        (Optional) Provide configuration for ip adapter 1, connect it to the KSamplerEfficient
        1. Set the image path for both (or the first one only) adapters
        2. Set the model for load ipadapter model
        3. (Optional) set weight, set noise, set weight_type, set start_at, set end_at
        4. Disconnect efficient loader model from ksamplerefficient, connect the 
        efficient loader’s model to apply adapter model and connect apply adapter
        model to ksamplerefficient model
        """
        # set the image path
        self.ipa1["390"]["inputs"]["image"] = image_path

        # set parameters
        self.ipa1["278"]["inputs"]["weight"] = weight
        self.ipa1["278"]["inputs"]["noise"] = noise
        self.ipa1["278"]["inputs"]["start_at"] = start_at
        self.ipa1["278"]["inputs"]["end_at"] = end_at

        self.ipa1["279"]["inputs"]["ipadapter_file"] = model

        self.used_components.add("ipa1")

        # connect apply ipadapter model to ksampler_efficient1 model
        self.ksampler_efficient1["229"]["inputs"]["model"] = ["278", 0]

    def connect_ksampler_efficient2(self, seed: int, steps: int, cfg_scale: float, denoise: float, sampler: str, ipa2_enabled: bool = True):
        """
        ################# CONNECT KSAMPLER EFFICENT 2 #################
        """

        self.ksampler_efficient2["246"]["inputs"]["seed"] = seed
        self.ksampler_efficient2["246"]["inputs"]["steps"] = steps
        self.ksampler_efficient2["246"]["inputs"]["cfg"] = cfg_scale
        self.ksampler_efficient2["246"]["inputs"]["denoise"] = denoise
        self.ksampler_efficient2["246"]["inputs"]["sampler_name"] = sampler

        self.used_components.add("ksampler_efficient2")

        if not ipa2_enabled:
            # (Default) connect model to the KSampler (Efficient) 1
            self.ksampler_efficient2["246"]["inputs"]["model"] = ["229", 0]
        else:
            self.ksampler_efficient2["246"]["inputs"]["model"] = ["284", 0]

    def connect_ip_adapter_2(self, image_path: str, weight: int = 1, noise: int = 0, weight_type: str = "original", start_at: int = 0, end_at: int = 1):
        """
        ################# CONNECT IP ADAPTER 2 #################
        (Optional) Provide configuration for ip adapter 2, connect it to the KSamplerEfficient
        1. (Optional) Set the second image path for the second one only adapter - disconnect the first image loader from apply ip adapter and connect the second one
        2. Set the model for load ipadapter model
        3. (Optional) set weight, set noise, set weight_type, set start_at, set end_at
        4. Set the civitai model
        5. Disconnect ksamplerefficient1 model entirely from ksamplerefficient2 model, connect the  applyipadapter2 model to ksamplerefficient model
        """
        if image_path:
            # set the image path for the second image loader
            self.ipa2["288"]["inputs"]["image"] = image_path

            # disconnect the first image loader from apply ip adapter and connect the second one
            self.ipa2["284"]["inputs"]["image"] = ["288", 0]
        else:
            # disconnect the second image loader from apply ip adapter and connect the first one
            self.ipa2["284"]["inputs"]["image"] = ["390", 0]


        # TODO: can user customize this model from a list of predefined models?
        # set the model for load ipadapter model
        self.ipa2["285"]["inputs"]["ipadapter_file"] = "ip-adapter-plus-face_sd15.bin"
        
        # set parameters
        self.ipa2["284"]["inputs"]["weight"] = weight
        self.ipa2["284"]["inputs"]["noise"] = noise
        self.ipa2["284"]["inputs"]["weight_type"] = weight_type
        self.ipa2["284"]["inputs"]["start_at"] = start_at
        self.ipa2["284"]["inputs"]["end_at"] = end_at

        self.used_components.add("ipa2")

        # set the civitai model
        # self.ipa2["251"]["inputs"]["ckpt_air"] = "{model_id}@{model_version}"

        # connect applyipadapter2 model to ksamplerefficient2 model
        self.ksampler_efficient2["246"]["inputs"]["model"] = ["284", 0]

    def connect_preview_image(self, refinement_enabled: bool = True):
        """
        ################# CONNECT PREVIEW IMAGE #################
        """

        if not refinement_enabled:
            self.used_components.add("preview_image1")
        else:
            self.used_components.add("preview_image2")

sample_settings = {
    # basic settings are for the first efficient loader / ksampler
    "basic_preset": "preset_1",
    "pos_prompt_enabled": False, 
    "basic_pos_text_prompt": "Pos text prompt", 
    "basic_neg_text_prompt": "Negative text prompt", 
    "basic_sampling_steps": 10, 
    "basic_sampler_method": "euler_ancestral", 
    "basic_model": "model_1", 
    "basic_width": 800, 
    "basic_height": 600, 
    "basic_cfg_scale": 0.5, 
    "basic_batch_size": 32, 
    "basic_batch_count": 5,
    "basic_denoise": 0.3, 

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

    "refinement_enabled": True, 
    "refinement_seed": 12345, 
    "refinement_steps": 20, 
    "refinement_cfg_scale": 0.7, 
    "refinement_denoise": 0.4, 
    "refinement_sampler": "sampler_1", 
    # "refinement_checkpoint": "checkpoint_1",

    "lora_count": 3, 
    "lora_models": ["lora_model_1", "lora_model_2", "lora_model_3"], 
    "lora_strengths": [0.5, 0.6, 0.7], 
    "lora_enabled": [True, False, True], 

    "controlnet_enabled": True, 
    "controlnet_model": 1, # maps to unit 
    "controlnet_reference_image": "controlnet_reference_image_1", 
    "controlnet_strength": 0.8, 
    "controlnet_start_at": 0.0, 
    "controlnet_end_at": 1.0, 
}


# TODO: generate image endpoint should now run this program and get the json to send to the comfyui server
# TODO: get the list of predefined models from David and install them to the custom nodes.
# TODO: check all the models and checkpoints and all the options for config for the user, preinstall them on the comfyui runpod server
# TODO: config the comfyui server so it has the endpoint which listens to the requests and runs the websocket for each request with predefined json file
#       and loads the images from CDN into the images path before sending a request to the comfyui - TODO: ensure that comfyui sees the images without a reload
if __name__ == "__main__":
    model_interface = ModelInterface()

    if sample_settings["controlnet_enabled"]:
        model_interface.connect_control_net(unit=sample_settings["controlnet_model"], image_path=sample_settings["controlnet_reference_image"], strength=sample_settings["controlnet_strength"], start_at=sample_settings["controlnet_start_at"], end_at=sample_settings["controlnet_end_at"])
    
    model_interface.choose_output_size(int1=sample_settings["basic_width"], int2=sample_settings["basic_height"])
    
    model_interface.connect_lora(count=sample_settings["lora_count"], models=sample_settings["lora_models"], stengths=sample_settings["lora_strengths"], enabled=sample_settings["lora_enabled"])
    
    if sample_settings["pos_prompt_enabled"]:
        model_interface.connect_random_prompts(text=sample_settings["basic_pos_text_prompt"]) # Optional

    model_interface.set_up_efficient_loader(negative=sample_settings["basic_neg_text_prompt"], ckpt_name=sample_settings["basic_model"], batch_size=sample_settings["basic_batch_size"])

    model_interface.set_up_ksampler_efficient1(steps=sample_settings["basic_sampling_steps"], sampler_name=sample_settings["basic_sampler_method"], cfg_scale=sample_settings["basic_cfg_scale"], denoise=sample_settings["basic_denoise"])

    if sample_settings["refinement_enabled"]:
        model_interface.connect_ksampler_efficient2(seed=sample_settings["refinement_seed"], steps=sample_settings["refinement_steps"], cfg_scale=sample_settings["refinement_cfg_scale"], denoise=sample_settings["refinement_denoise"], sampler_name=sample_settings["refinement_sampler"])

    model_interface.connect_preview_image(sample_settings["refinement_enabled"])

    if sample_settings["ipa_1_enabled"]:
        model_interface.connect_ip_adapter_1(image_path=sample_settings["ipa_1_reference_image"], model=sample_settings["ipa_1_model"], weight=sample_settings["ipa_1_weight"], noise=sample_settings["ipa_1_noise"], start_at=sample_settings["ipa_1_start_at"], end_at=sample_settings["ipa_1_end_at"])

    if sample_settings["ipa_2_enabled"]:
        model_interface.connect_ip_adapter_2(image_path=sample_settings["ipa_2_reference_image"], model=sample_settings["ipa_2_model"], weight=sample_settings["ipa_2_weight"], noise=sample_settings["ipa_2_noise"], start_at=sample_settings["ipa_2_start_at"], end_at=sample_settings["ipa_2_end_at"])

    final_json = model_interface.finalize()

    # TODO: return this file instead to the generate endpoint
    # Write the final JSON to a file
    with open('final_json_output.json', 'w') as json_file:
        json.dump(final_json, json_file, indent=4)