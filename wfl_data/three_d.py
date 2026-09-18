from .extractor import extract_modalities
from pathlib import Path

def extract_datasets(output_dir: str | Path) -> None:
    """Extracts only the 3D dataset."""
    extract_modalities(output_dir, ["3d"])
