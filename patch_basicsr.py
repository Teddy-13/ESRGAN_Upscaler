import os
import sys

def patch_basicsr():
    print("Patching basicsr/data/degradations.py for torchvision...")
    try:
        import basicsr
        basicsr_path = os.path.dirname(basicsr.__file__)
        degradations_path = os.path.join(basicsr_path, "data", "degradations.py")
        
        if os.path.exists(degradations_path):
            with open(degradations_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Replace the broken import
            new_content = content.replace(
                "from torchvision.transforms.functional_tensor import rgb_to_grayscale",
                "from torchvision.transforms.functional import rgb_to_grayscale"
            )
            
            with open(degradations_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print("Successfully patched degradations.py!")
        else:
            print(f"Could not find degradations.py at {degradations_path}")
            
    except ImportError:
        print("basicsr not found. Please install it first.")
    except Exception as e:
        print(f"Failed to patch: {e}")

if __name__ == "__main__":
    patch_basicsr()
