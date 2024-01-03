# Certificate Generator

> [!NOTE]
> The Certificate Generator is a powerful tool designed to simplify the mass generation of certificates for GDSC SJEC Events.

## Getting Started

1. Clone the repository and change directory to the cloned repository.
```bash
git clone git@github.com:gdscsjec/certificate-generator.git
cd certificate-generator
```

2. Create a virtual environment.
```bash
python -m venv venv
```

3. Activate the virtual environment
```bash
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

4. Install required packages
```bash
pip install -r requirements.txt
```
- Modify data.csv with participant details.
- Change the filename within `generate.py`

5. Generate data using `generate.py`.
```bash
python generate.py
```

- Replace `template.jpg` with your own certificate design.
- Replace `signature.png` with your own signature.
  - Go to [Excalidraw](https://excalidraw.com/).
  - Draw your signature.
  - Select your signature, and export it.
  - Set options as Only Selected, background dark mode, embed scence should be disabled. scale factor is not important.
- Ensure placeholders for participant names, event details, etc., are included.

6. Generate certificates.
```bash
python main.py
```

## Demo
![Demo](https://raw.githubusercontent.com/gdscsjec/certificate-generator/main/misc/Abigail_Turner_Certificate.jpg)
## Feedback and Contributions
Feel free to provide feedback or contribute to the project by submitting issues or pull requests.