from .extractor import extract_modalities
from pathlib import Path

def extract_datasets(output_dir: str | Path) -> None:
    """Extracts only the RGB dataset."""
    extract_modalities(output_dir, ["rgb"])
