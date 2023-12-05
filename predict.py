# Prediction interface for Cog ⚙️
# https://github.com/replicate/cog/blob/main/docs/python.md

from cog import BasePredictor, Input, Path
import os
import sys
import re
sys.path.extend(['/src/magic-animate'])

class Predictor(BasePredictor):
    def setup(self) -> None:
        """Load the model into memory to make running multiple predictions efficient"""
        # link pretrained_models to /src/magic-animate/pretrained_models
        # os.system("ln -s /src/pretrained_models /src/magic-animate/pretrained_models")

    def predict(
        self,
        image: Path = Input(description="Input image"),
        video: Path = Input(description="Input motion video"),
        num_inference_steps: int = Input(
            description="Number of denoising steps", ge=1, le=200, default=25
        ),
        guidance_scale: float = Input(
            description="Scale for classifier-free guidance", ge=1, le=50, default=7.5
        ),
        seed: int = Input(
            description="Random seed. Leave blank to randomize the seed", default=None
        ),
    ) -> Path:
        """Run a single prediction on the model"""
        if seed is None:
            seed = int.from_bytes(os.urandom(2), "big")
        print(f"Using seed: {seed}")
        
        # system change directory to /src/magic-animate
        os.chdir("/src/magic-animate")

        # Clean up past runs (just in case)
        output_dir = "samples/"
        os.system("rm -rf " + output_dir)
        os.system("mkdir -p " + output_dir)

        # Create a config.yaml file with the following content:
        config_data = f"""
pretrained_model_path: "/src/pretrained_models/stable-diffusion-v1-5"
pretrained_vae_path: "/src/pretrained_models/sd-vae-ft-mse"
pretrained_controlnet_path: "/src/pretrained_models/MagicAnimate/densepose_controlnet"
pretrained_appearance_encoder_path: "/src/pretrained_models/MagicAnimate/appearance_encoder"
pretrained_unet_path: ""
motion_module: "/src/pretrained_models/MagicAnimate/temporal_attention/temporal_attention.ckpt"
savename: null
fusion_blocks: "midup"
seed:           [{seed}]
steps:          {num_inference_steps}
guidance_scale: {guidance_scale}
source_image:
  - "{image}"
video_path:
  - "{video}"
inference_config: "configs/inference/inference.yaml"
size: 512
L:    16
S:    1 
I:    0
clip: 0
offset: 0
max_length: null
video_type: "condition"
invert_video: false
save_individual_videos: false
        """
        with open("configs/config.yaml", "w") as file:
            file.write(config_data)

        # run the following: python -m magicanimate.pipelines.animation --config config.yaml
        os.system("python -m magicanimate.pipelines.animation --config configs/config.yaml")

        #find a file ending in .mp4 in samples/config-*/video and return it
        base_dir = 'samples/'
        pattern = re.compile(r'^config-.*$')
        for folder in os.listdir(base_dir):
            if pattern.match(folder):
                video_dir = os.path.join(base_dir, folder, 'videos')
                if os.path.exists(video_dir):
                    for file in os.listdir(video_dir):
                        if file.endswith('.mp4'):
                           video_path = os.path.join("/src/magic-animate/", video_dir, file)
                           print(video_path)
                           return Path(video_path)
        return "No video found"