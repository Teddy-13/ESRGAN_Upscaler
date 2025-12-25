import os
import tarfile
import subprocess
import sys
import shutil

def install_basicsr():
    print(f"Using python: {sys.executable}")
    
    # 1. Download source
    print("Downloading basicsr 1.4.2 source...")
    try:
        # Added --no-build-isolation to prevent pip from creating a fresh build env with broken tools
        subprocess.check_call([sys.executable, "-m", "pip", "download", "basicsr==1.4.2", "--no-deps", "--no-binary", ":all:", "--no-build-isolation", "-d", "."])
    except subprocess.CalledProcessError:
        print("Failed to download basicsr. Check internet connection.")
        return

    # Find the tar.gz
    try:
        tar_file = [f for f in os.listdir(".") if f.startswith("basicsr-") and f.endswith(".tar.gz")][0]
    except IndexError:
        print("Could not find downloaded tar.gz file.")
        return
    
    # 2. Extract
    print(f"Extracting {tar_file}...")
    try:
        with tarfile.open(tar_file, "r:gz") as tar:
            tar.extractall(".")
    except Exception as e:
        print(f"Extraction failed: {e}")
        return
    
    dir_name = tar_file.replace(".tar.gz", "")
    
    if not os.path.exists(dir_name):
        # Fallback if directory name doesn't match
        possible_dirs = [d for d in os.listdir(".") if os.path.isdir(d) and d.startswith("basicsr")]
        if possible_dirs:
            dir_name = possible_dirs[0]
        else:
            print("Could not find extracted directory.")
            return

    # 3. Patch setup.py
    setup_path = os.path.join(dir_name, "setup.py")
    print(f"Patching {setup_path}...")
    
    if os.path.exists(setup_path):
        with open(setup_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Patch the specific failure point: locals()['__version__']
        # We assume version is 1.4.2 because we downloaded basicsr==1.4.2
        new_content = content.replace("return locals()['__version__']", "return '1.4.2'")
        
        with open(setup_path, "w", encoding="utf-8") as f:
            f.write(new_content)
    else:
        print("setup.py not found, skipping patch (strange).")
        
    # 4. Install
    print("Installing patched basicsr...")
    try:
        # Use --no-build-isolation to ensure it uses our current setuptools/environment
        # Use abspath to ensure pip treats it as a directory, not a package name
        subprocess.check_call([sys.executable, "-m", "pip", "install", os.path.abspath(dir_name), "--no-build-isolation"])
        print("Successfully installed basicsr!")
    except subprocess.CalledProcessError:
        print("Failed to install patched basicsr.")
    
    # 5. Patch degradations.py for torchvision compatibility
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
        print("basicsr not found in python path. Make sure it is installed.")
    except Exception as e:
        print(f"Failed to patch degradations.py: {e}")

    # 6. Cleanup
    print("Cleaning up...")
    try:
        if os.path.exists(tar_file):
            os.remove(tar_file)
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
    except Exception as e:
        print(f"Cleanup warning: {e}")

if __name__ == "__main__":
    install_basicsr()
