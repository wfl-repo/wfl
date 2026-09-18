# WFL Datasets Extractor

A Python package designed to securely authenticate and extract large multimodal datasets (Audio, 3D, Thermal, RGB, Retina) from a Network Attached Storage (NAS) into your local environment. 

## ⚙️ Setup & Configuration

This package requires **zero external dependencies** and uses only standard Python libraries (`pathlib`, `shutil`, `subprocess`, etc.).

Before using the package, you must configure your NAS path:

1. Open `wfl_data/config.json`.
2. Update the `NAS_PATH` with your actual NAS IP and shared directory using double backslashes (like below):
   ```json
   {
       "NAS_PATH": "\\\\YOUR_NAS_IP_HERE\\data\\Master_data"
   }
   ```

## 🚀 Usage

Here is a simple example of how to use the package to extract data. 
*(Note: Create your python script in the root directory of this repository, directly next to the `wfl_data` package folder, to ensure imports work correctly and to prevent accidentally creating nested `wfl_data/wfl_data` folders).*

*(Note: The `output_dir` parameter specifies the local destination folder where the downloaded data will be saved).*

```python
from wfl_data import audio, thermal, rgb, retina, three_d
from wfl_data.extractor import extract_modalities

"""Individual modality download"""
audio.extract_datasets(output_dir=r"./audio")
thermal.extract_datasets(output_dir=r"./thermal")
rgb.extract_datasets(output_dir=r"./rgb")
retina.extract_datasets(output_dir=r"./retinal")
three_d.extract_datasets(output_dir=r"./3d")

"""Multiple modalities download"""
extract_modalities(output_dir=r".\all_data", modalities=["audio", "thermal"])
```