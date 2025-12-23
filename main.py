# main.py
# Example usage of the reusable Real-ESRGAN model

from upscaler import RealESRGANUpscaler
import random

def main():
    upscaler = RealESRGANUpscaler(
        tile=256  # safer for GPUs with limited VRAM
    )

    num=random.randint(1,10)

    input_image = "input.jpg"     # put your image here
    output_image = f"output_{num}.jpg"

    upscaler.upscale_and_save(
        input_image,
        output_image
    )

    print(f"Upscaled image saved as {output_image}")

if __name__ == "__main__":
    main()
