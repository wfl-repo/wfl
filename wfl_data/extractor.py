import logging
import shutil
import getpass
import subprocess
import json
from pathlib import Path

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def get_nas_path():
    """Reads NAS_PATH from config.json located in the wfl package directory."""
    config_file = Path(__file__).parent / "config.json"
    if not config_file.exists():
        logging.error(f"config.json not found at {config_file}. Please create one with a 'NAS_PATH' key.")
        return None
    try:
        with open(config_file, "r") as f:
            data = json.load(f)
            return data.get("NAS_PATH")
    except Exception as e:
        logging.error(f"Error reading config.json: {e}")
        return None

def authenticate_nas(nas_path: str, username: str, password: str) -> bool:
    """Authenticates to the NAS using Windows 'net use' command."""
    subprocess.run(f'net use "{nas_path}" /delete /y', shell=True, capture_output=True)
    command = f'net use "{nas_path}" "{password}" /user:"{username}" /persistent:no'
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            logging.info(f"Successfully connected to the NAS at {nas_path}.")
            return True
        else:
            logging.error(f"Failed to connect to NAS. Check your password. Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        logging.error(f"Error executing net use: {e}")
        return False

def disconnect_nas(nas_path: str) -> None:
    """Disconnects from the NAS to clean up."""
    command = f'net use "{nas_path}" /delete /y'
    subprocess.run(command, shell=True, capture_output=True)
    logging.info(f"Disconnected from NAS at {nas_path}.")

def extract_modalities(output_dir: str | Path, modalities: list[str]) -> None:
    """
    Extracts multiple modalities (e.g., ['audio', 'thermal', 'rgb']) from each subject's directory
    on a NAS and copies them to the output directory.

    Args:
        output_dir (str | Path): Local destination directory.
        modalities (list[str]): List of modality folder names to extract.
    """
    NAS_PATH = get_nas_path()
    if not NAS_PATH:
        logging.error("Cannot proceed without a valid NAS_PATH in config.json.")
        return

    print(f"\n--- NAS Authentication ---")
    print(f"Connecting to: {NAS_PATH}")
    
    username = input("Enter NAS username: ")
    password = getpass.getpass(prompt=f"Enter password for user '{username}': ")
    print("--------------------------\n")
    
    if not authenticate_nas(NAS_PATH, username, password):
        return

    try:
        source_path = Path(NAS_PATH)
        output_path = Path(output_dir)

        output_path.mkdir(parents=True, exist_ok=True)

        if not source_path.is_dir():
            logging.error(f"NAS directory does not exist or cannot be accessed: {source_path}")
            return

        modalities_lower = [m.lower() for m in modalities]

        for subject_dir in source_path.iterdir():
            if subject_dir.is_dir():
                subject_name = subject_dir.name
                
                # Check for all requested modalities in this subject folder
                for child in subject_dir.iterdir():
                    if child.is_dir() and child.name.lower() in modalities_lower:
                        modality_name = child.name
                        modality_dest = output_path / subject_name / modality_name
                        
                        logging.info(f"[{subject_name}] Found '{modality_name}'. Copying to {modality_dest}...")
                        try:
                            shutil.copytree(child, modality_dest, dirs_exist_ok=True)
                            logging.info(f"[{subject_name}] '{modality_name}' successfully copied.")
                        except Exception as e:
                            logging.error(f"[{subject_name}] Failed to copy '{modality_name}': {e}")
    finally:
        if 'NAS_PATH' in locals() and NAS_PATH:
            disconnect_nas(NAS_PATH)
