# AzCam Testers

*azcam-testers* is a suite for the acquition and analysis of image sensor data for sensor characterization.

## Documentation

See https://azcam.readthedocs.io/.

## Installation

`pip install azcam-testers`

Or download the latest version from from github: https://github.com/mplesser/azcam-testers.git.

# Testers

The **tester** tools are for image sensor characterization and are available when this package is installed.

Usage Example:
 
```
from azcam_testers.tools.bias import bias
bias.acquire()
bias.analyze()
```

### Tester Base

[Testers base class](/code/azcam/tools/testers/testers.html)

### Detector Characterization Base

[DetChar base class](/code/azcam/tools/testers/detchar.html)

### Bias Images

[Bias class](/code/azcam/tools/testers/bias.html)

### Dark Signal

[Dark class](/code/azcam/tools/testers/dark.html)

### Defects

[Defects class](/code/azcam/tools/testers/defects.html)

### Detector Calibration

[DetCal class](/code/azcam/tools/testers/detcal.html)

### Extended Pixel Edge Response Charge Transfer Efficiency

[Eper class](/code/azcam/tools/testers/eper.html)

### Fe55 X-Ray Gain, Noise, and Charge Transfer Efficiency

[Fe55 class](/code/azcam/tools/testers/fe55.html)

### Gain

[Gain class](/code/azcam/tools/testers/gain.html)

### Linearity

[Linearity class](/code/azcam/tools/testers/linearity.html)

### Metrology

[Metrology class](/code/azcam/tools/testers/metrology.html)

### Pocket Pumping

[PocketPump class](/code/azcam/tools/testers/pocketpump.html)

### Photo-Response Non-Uniformity

[PRNU class](/code/azcam/tools/testers/prnu.html)

### Photon Transfer Curve

[PTC class](/code/azcam/tools/testers/ptc.html)

### Quantum Efficiency

[QE class](/code/azcam/tools/testers/qe.html)

### Ramp Images

[Ramp class](/code/azcam/tools/testers/ramp.html)

### Superflat Images

[Superflat class](/code/azcam/tools/testers/superflat.html)

## Report Commands

The report tool is helpful when generating reports. 

Usage Example:

```
from azcam.tools.report import Report
report=Report()
report.make_rstfile("rstfile.rst")
```
