from typing import List, Optional

import importlib

import os

from model.image_generation import Settings

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
        self.preview_image1 = self.load_json("preview_image1")
        self.preview_image2 = self.load_json("preview_image2")

        self.used_components = set()

    def load_json(self, 
                  unit_name: str):
        # Import the JSON dictionary directly without decoding
        try:
            # Assuming all JSON data is stored in the JSONEngine module
            module = importlib.import_module("comfyui.JSONEngine")
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
            # print(component)
            component_data = getattr(self, component, None)
            # print(component_data)
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

    def connect_control_net(self, 
                            unit: int, 
                            image_path: str, 
                            strength: float = 1.0, 
                            start_percent: float = 0.0, 
                            end_percent: float = 1.0):
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

    def choose_output_size(self, 
                           int1: int, 
                           int2: int, 
                           image_path: str = ""):
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

    def connect_lora(self, 
                     count: int, 
                     models: List[str], 
                     strengths: List[str], 
                     enabled: List[bool]):
        """
        ################# CONNECT LORA #################
        (Optional) Connect lora to Efficient Loader
        1. Connect lora to lora_stack in Efficient Loader
        """
        if count:
            # Connect Lora to the lora_stack in efficient loader
            self.lora_stacker["207"]["inputs"]["lora_count"] = count

            for i in range(count):  # Assuming 'enabled' has 4 elements.
                if enabled[i]:
                    index = i + 1
                    self.lora_stacker["207"]["inputs"][f"lora_name_{index}"] = models[i]
                    self.lora_stacker["207"]["inputs"][f"model_str_{index}"] = strengths[i]

        self.efficient_loader["206"]["inputs"]["lora_stack"] = ["207", 0]
        self.used_components.add("lora_stacker")

    def connect_random_prompts(self, 
                               positive_prompt: str):
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

    def connect_efficient_loader(self, 
                                ckpt_name: str, 
                                negative_prompt: str, 
                                batch_size: int):
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

       # Set the batch size in efficient loader
        self.efficient_loader["206"]["inputs"]["batch_size"] = batch_size

        self.used_components.add("efficient_loader")

    def connect_ksampler_efficient1(self,
                                    steps: int, 
                                    cfg_scale: float, 
                                    denoise: float, 
                                    sampler: str, 
                                    ipa1_enabled: bool = False):
        """
        ################# CONNECT KSAMPLER EFFICENT 2 #################
        """
        # self.ksampler_efficient1["229"]["inputs"]["seed"] = seed
        self.ksampler_efficient1["229"]["inputs"]["steps"] = steps
        self.ksampler_efficient1["229"]["inputs"]["cfg"] = cfg_scale
        self.ksampler_efficient1["229"]["inputs"]["denoise"] = denoise
        self.ksampler_efficient1["229"]["inputs"]["sampler_name"] = sampler

        self.used_components.add("ksampler_efficient1")

        if ipa1_enabled:
            self.ksampler_efficient1["229"]["inputs"]["model"] = ["278", 0]
        else:
            self.ksampler_efficient1["229"]["inputs"]["model"] = ["206", 0]
            


    def connect_ip_adapter_1(self, 
                             image_path: str, 
                             model: str, 
                             weight: int = 1, 
                             noise: int = 0, 
                             weight_type: str = "original", 
                             start_at: int = 0, 
                             end_at: int = 1):
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
        self.ipa1["278"]["inputs"]["weight_type"] = weight_type
        self.ipa1["278"]["inputs"]["start_at"] = start_at
        self.ipa1["278"]["inputs"]["end_at"] = end_at

        self.ipa1["279"]["inputs"]["ipadapter_file"] = model

        self.used_components.add("ipa1")

    def connect_ksampler_efficient2(self, 
                                    seed: int, 
                                    steps: int, 
                                    cfg_scale: float, 
                                    denoise: float, 
                                    sampler: str, 
                                    ipa2_enabled: bool = True):
        """
        ################# CONNECT KSAMPLER EFFICENT 2 #################
        """

        self.ksampler_efficient2["246"]["inputs"]["seed"] = seed
        self.ksampler_efficient2["246"]["inputs"]["steps"] = steps
        self.ksampler_efficient2["246"]["inputs"]["cfg"] = cfg_scale
        self.ksampler_efficient2["246"]["inputs"]["denoise"] = denoise
        self.ksampler_efficient2["246"]["inputs"]["sampler_name"] = sampler

        self.used_components.add("ksampler_efficient2")

        if ipa2_enabled:
            self.ksampler_efficient2["246"]["inputs"]["model"] = ["284", 0]
        else:
            self.ksampler_efficient2["246"]["inputs"]["model"] = ["229", 0]

    def connect_ip_adapter_2(self, 
                             image_path: str, 
                             ipa_model: str, 
                             ckpt_model: str, 
                             weight: int = 1, 
                             noise: int = 0, 
                             weight_type: str = "original", 
                             start_at: int = 0, 
                             end_at: int = 1):
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

        self.ipa2["285"]["inputs"]["ipadapter_file"] = ipa_model
        
        # set parameters
        self.ipa2["284"]["inputs"]["weight"] = weight
        self.ipa2["284"]["inputs"]["noise"] = noise
        self.ipa2["284"]["inputs"]["weight_type"] = weight_type
        self.ipa2["284"]["inputs"]["start_at"] = start_at
        self.ipa2["284"]["inputs"]["end_at"] = end_at

        self.used_components.add("ipa2")

        if civitai_enabled:
            self.ipa2["251"]["inputs"]["ckpt_name"] = ckpt_model

            self.ipa2["284"]["inputs"]["model"] = ["251", 0]
        else:
            self.ipa2["284"]["inputs"]["model"] = ["229", 0]

    def connect_preview_image(self, refinement_enabled: bool = False):
        """
        ################# CONNECT PREVIEW IMAGE #################
        """

        if refinement_enabled:
            self.used_components.add("preview_image2")
        else:
            self.used_components.add("preview_image1")

def generate_workflow(settings: Settings, 
                      image_ids: List[str], 
                      image_formats: List[str]) -> Optional[dict]:
    try:
        print("INITIALIZING MODEL INTERFACE")
        model_interface = ModelInterface()

        predefined_path = os.getenv('COMFYUI_PREDEFINED_PATH')

        format_map = {"jpeg": ".jpeg",
                      "heic": ".heic",
                      "png": ".png"}

        if settings.controlnet_enabled:
            print("CONTROLNET ENABLED")
            file_extension = format_map[image_formats[2]]
            settings.controlnet_reference_image = predefined_path + "/" + image_ids[2] + file_extension
            model_interface.connect_control_net(unit=settings.controlnet_model, 
                                                image_path=settings.controlnet_reference_image, 
                                                strength=settings.controlnet_strength, 
                                                start_percent=settings.controlnet_start_percent, 
                                                end_percent=settings.controlnet_end_percent)

        print("CHOOSING OUTPUT SIZE")
        model_interface.choose_output_size(int1=settings.basic_width, 
                                           int2=settings.basic_height)

        if any(settings.lora_enabled):
            print("CONNECTING LORA")
            model_interface.connect_lora(count=settings.lora_count, 
                                         models=settings.lora_models, 
                                         strengths=settings.lora_strengths, 
                                         enabled=settings.lora_enabled)

        if settings.pos_prompt_enabled:
            print("POS PROMPT ENABLED")
            model_interface.connect_random_prompts(positive_prompt=settings.basic_pos_text_prompt)

        # print("SETTING UP EFFICIENT LOADER")
        # model_interface.set_up_efficient_loader(negative_prompt=settings.basic_neg_text_prompt, 
        #                                         ckpt_name=settings.basic_model, 
        #                                         batch_size=settings.basic_batch_size)

        # print("KSAMPLER EFFICIENT 1")
        # model_interface.set_up_ksampler_efficient1(steps=settings.basic_sampling_steps,
        #                                            sampler=settings.basic_sampler_method, 
        #                                            cfg_scale=settings.basic_cfg_scale, 
        #                                            denoise=settings.basic_denoise)

        # if settings.ipa_1_enabled:
        #     print("IPA 1 ENABLED")
        #     file_extension = format_map[image_formats[0]]
        #     settings.ipa_1_reference_image = predefined_path + "/" + image_ids[0] + file_extension
        #     model_interface.connect_ip_adapter_1(image_path=settings.ipa_1_reference_image, 
        #                                          model=settings.ipa_1_model, 
        #                                          weight=settings.ipa_1_weight, 
        #                                          noise=settings.ipa_1_noise, 
        #                                          weight_type=settings.ipa_1_weight_type, 
        #                                          start_at=settings.ipa_1_start_at, 
        #                                          end_at=settings.ipa_1_end_at)

        # if settings.refinement_enabled:
        #     print("KSAMPLER EFFICIENT 2")
        #     model_interface.connect_ksampler_efficient2(seed=settings.refinement_seed, 
        #                                                 sampler=settings.refinement_sampler, 
        #                                                 steps=settings.refinement_steps, 
        #                                                 cfg_scale=settings.refinement_cfg_scale, 
        #                                                 denoise=settings.refinement_denoise)


            # if settings.ipa_2_enabled:
            #     print("IPA 2 ENABLED") 
            #     file_extension = format_map[image_formats[1]]
            #     settings.ipa_2_reference_image = predefined_path + "/" + image_ids[1] + file_extension
            #     model_interface.connect_ip_adapter_2(image_path=settings.ipa_2_reference_image, 
            #                                          ipa_model=settings.ipa_2_model, 
            #                                          ckpt_model=settings.refinement_civitai_model, 
            #                                          weight=settings.ipa_2_weight, 
            #                                          noise=settings.ipa_2_noise, 
            #                                          weight_type=settings.ipa_2_weight_type, 
            #                                          start_at=settings.ipa_2_start_at, 
            #                                          end_at=settings.ipa_2_end_at)

        print("CONNECTING PREVIEW IMAGE")
        model_interface.connect_preview_image(settings.refinement_enabled)

        final_json = model_interface.finalize()

        return final_json

    except Exception as e:
        print(f"AN ERROR OCCURRED DURING WORKFLOW EXECUTION: {str(e)}")
        return None
