import os
import sys
import site

def force_patch():
    print("Attempting to patch basicsr/data/degradations.py...")
    
    # 1. Gather all possible site-packages paths
    paths = list(sys.path)
    paths.extend(site.getsitepackages())
    
    target_file = None
    
    # 2. Search for the file in all paths
    for path in paths:
        if not path or not os.path.exists(path):
            continue
            
        candidate = os.path.join(path, "basicsr", "data", "degradations.py")
        if os.path.exists(candidate):
            target_file = candidate
            print(f"Found target at: {target_file}")
            break
            
    if not target_file:
        # Fallback: Try relative to venv if easy to guess
        # Assuming we are in Backend_Upscaler/
        candidates = [
            os.path.join("venv", "Lib", "site-packages", "basicsr", "data", "degradations.py"),
            os.path.join("..", "venv", "Lib", "site-packages", "basicsr", "data", "degradations.py")
        ]
        for c in candidates:
            if os.path.exists(c):
                target_file = os.path.abspath(c)
                print(f"Found target at (fallback): {target_file}")
                break

    if not target_file:
        print("ERROR: Could not find basicsr installation. Is it installed in this venv?")
        return

    # 3. Patch it
    try:
        with open(target_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        # The fix
        old_import = "from torchvision.transforms.functional_tensor import rgb_to_grayscale"
        new_import = "from torchvision.transforms.functional import rgb_to_grayscale"
        
        if old_import not in content and new_import in content:
            print("File is already patched!")
            return

        if old_import in content:
            new_content = content.replace(old_import, new_import)
            with open(target_file, "w", encoding="utf-8") as f:
                f.write(new_content)
            print("SUCCESS: Patch applied.")
        else:
            print("WARNING: Could not find the specific import string. File might differ from expected version.")
            
    except Exception as e:
        print(f"Failed to write patch: {e}")

if __name__ == "__main__":
    force_patch()
