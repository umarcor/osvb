from pathlib import Path
from pyOSVR import LoadOSVRFile

OSVR = LoadOSVRFile(Path(__file__).parent / 'vunit.osvr.yml')
