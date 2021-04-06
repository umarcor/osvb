from pathlib import Path
from pyOSVR import LoadOSVRFile, LoadXUnitFile

OSVR = LoadOSVRFile(Path(__file__).parent / 'vunit.osvr.yml')

OSVR = LoadXUnitFile(Path(__file__).parent / 'vunit.xml')
