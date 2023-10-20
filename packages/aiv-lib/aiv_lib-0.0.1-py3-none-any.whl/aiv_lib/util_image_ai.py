import os
from diffusers import DiffusionPipeline
import torch
import gc
# shuffle the art types
import random

art_type_index = 0
device = torch.device("cuda" if torch.cuda.is_available() else "mps")

art_types = [
    " fantasy art",
    " abstract art",
    " surreal art",
    " impressionism",
    " expressionism",
    " pop art",
    " minimalism",
    " realism",
    " art nouveau",
    " cubism",
    "anime art",
    " conceptual art",
    " digital art",
    " street art",
    " fine art",
    " modern art",
    "cartoon art",
]



random.shuffle(art_types)

# check if os is windows
if os.name == "nt":
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
else:


def loadOpenVINO():
    from optimum.intel import OVStableDiffusionPipeline

    # Load and compile the pipeline for performance.
    name = "OpenVINO/stable-diffusion-pokemons-tome-quantized-aggressive"
    pipe = OVStableDiffusionPipeline.from_pretrained(name, compile=False)
    pipe.reshape(batch_size=1, height=512, width=512, num_images_per_prompt=1)
    pipe.compile()

    # Generate an image.
    prompt = " digital art Illustration of William James with a background depicting late 19th century America"
    output = pipe(prompt, num_inference_steps=50, output_type="pil").images[0]
    output.save("image.png")

# load both base & refiner
base = DiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16, variant="fp16", use_safetensors=True
)
base.to(device)  # Use 'metal' as the device name for Metal GPU on M1 Mac
refiner = DiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-refiner-1.0",
    text_encoder_2=base.text_encoder_2,
    vae=base.vae,
    torch_dtype=torch.float16,
    use_safetensors=True,
    variant="fp16",
)
refiner.to(device)  # Use 'metal' as the device name for Metal GPU on M1 Mac

# Define how many steps and what % of steps to be run on each experts (80/20) here
n_steps = 40
high_noise_frac = 0.8




def generateImageByPrompt(output_file_path, prompt):
    # run both experts
    image = base(
        prompt=prompt,
        num_inference_steps=n_steps,
        denoising_end=high_noise_frac,
        output_type="latent",
    ).images
    image = refiner(
        prompt=prompt,
        num_inference_steps=n_steps,
        denoising_start=high_noise_frac,
        image=image,
    ).images[0]
    image.save(output_file_path)
    print(f"Image saved to {output_file_path}")
    gc.collect()



def generateImages(output_folder, prompt, num_images_to_generate=1):
    global art_type_index  # Declare the variable as global

    # Get the count of images already in the output folder
    existing_images = len([f for f in os.listdir(output_folder) if os.path.isfile(os.path.join(output_folder, f)) and f.startswith("ai_")])

    for i in range(existing_images, existing_images + num_images_to_generate):
        # Check if the image already exists, if yes, skip the generation
        image_path = os.path.join(output_folder, f"ai_{i}.jpeg")
        if os.path.exists(image_path):
            print(f"Image {i} already exists, skipping...")
            continue

        art_type = art_types[art_type_index]
        complete_prompt = "illustration of " + prompt + ", " + art_type + ", ultra real, dramatic lighting, photorealistic, 4k"
        
        generateImageByPrompt(image_path, complete_prompt)
        print(f"Image {i} saved to {output_folder}")

        art_type_index = (art_type_index + 1) % len(art_types)  # Rotate the art type index

#


if __name__ == "__main__":
    output_folder = "/Users/yadubhushan/Documents/media/python_space/output/temp"
    ai_images_output_folder = os.path.join(output_folder, "ai_images")
    os.makedirs(ai_images_output_folder, exist_ok=True)
    output = generateImages(
       ai_images_output_folder,
        "little girl darkhair, kodak portra 100, split into multiple different images, shot from different angles",
        num_images_to_generate=1,
    )
    print(ai_images_output_folder)

