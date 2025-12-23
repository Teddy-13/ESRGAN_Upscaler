ESRGAN Upscaler
A high-performance image upscaling tool using Real-ESRGAN and PyTorch.

Quick Start
1. Prerequisites
Python: 3.11.x (Required for compatibility)

GPU: NVIDIA RTX 

Drivers: CUDA 12.4+ compatible

2. Installation
PowerShell

# Create and activate environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install GPU-accelerated PyTorch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124

3. Essential Fix
To resolve the ModuleNotFoundError in basicsr:

Open venv/Lib/site-packages/basicsr/data/degradations.py.

Line 8: Change functional_tensor to functional.

Usage
Place RealESRGAN_x4plus.pth in the weights/ folder.

Place your image (e.g., input.jpg) in the project root.

Run the upscaler:

PowerShell

python main.py input.jpg
📦 Repository Info
Main Script: main.py

Logic: upscaler.py

Ignore: venv/ and weights/*.pth are excluded from Git to save space.