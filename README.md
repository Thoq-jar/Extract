# Extract

A GPU extracting utility (much zoom)

## Setup
**Unix:**
Prerequisites:
- Cuda Toolkit (Or metal for macOS, coming soon)
- Python 3.12
- Bash/ZSH etc

```cmd
python3 -m venv venv
```
```cmd
source venv/bin/acitvate
```
```cmd
pip install numpy
pip install pytorch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```
```cmd
python Extract/extract.py
```

**Windows**:

Prerequisites:
- Cuda Toolkit
- Python 3.12
- Powershell

```cmd
python -m venv venv
```
```cmd
.\venv\Scripts\Activate.ps1
```
```cmd
pip install numpy
pip install pytorch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```
```cmd
python Extract/extract.py
```
