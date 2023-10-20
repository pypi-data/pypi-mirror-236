# Theia Technologies IQSmart(R)
[Theia Technologies](https://www.theiatech.com) offers a [MCR600 motor control board](https://www.theiatech.com/lenses/accessories/mcr/) for interfacing with Theia's motorized lenses.  This board controls focus, zoom, iris, and IRC filter motors.  It can be connected to a host comptuer by USB, UART, or I2C connection.  This IQSmart module allows the user to easily convert from engineering units (meters, degrees) to motor steps applicable to Theia's motorized lenses.  For sending thess motor steps to the contorl board to move the lens, install TheiaMCR ([TheiaMCR on Githum](https://github.com/cliquot22/TheiaMCR))

# Features
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> Engineering units can be converted to motor steps and vice versa.  The calculations use the design data for the lens but it is possible to load a calibration data file as well.  
## Motor steps to engineering units
- zoomStep2FL: calculate the lens focal length from the current focal length motor step.  
- focusStep2OD: calculate the object distance at the current focal length from the current focus motor step. 
- irisStep2NA, irisStep2FNum: calculate the numeric aperture or F/# at the current focal length from the current iris step.  
## Engineering units to motor steps
- FL2ZoomStep: calculate the zoom motor step for a focal length (in mm)
- OD2FocusStep: calculate the focus motor step for a given zoom motor step and object distance (in m)
- ODFL2FocusStep: calculate the focus motor step for a given focal length (in mm) and object distance (in m)
- NA2IrisStep: calculate the iris step from the numeric aperture at the current focal length (in mm)
- fnum2IrisStep: calculate the iris step from the F/# at the current focal length (in mm)
- AOV2MotorSteps: calculate the focus and zoom motor steps to support the requested angle of view (in deg).  This depends on the object distance as well and image sensor size.  
- FOV2MotorSteps: calculate the focus and zoom motor steps to support the field of view (in m).  This depends on the object distance as well and image sensor size.  
## Conversion functions
- calcAOV: calculate the angle of view (in deg) from a focal length (in mm).  
- calcFOV: calcualte the field of view (in m) from the focal length (in mm) and object distance (in m)
- calcDOF: calculate the minimum and maximum object distances for acceptable focus at the given focal length (in mm), aperture (in iris motor step position), and focused object distance (in m).  
## Camera back focal length compensation
- BFLCorrection: apply a correction to any focus motor step position to compensate for tolerances in the camera side lens mount.  BFL correction points are made by adjusting the lens for best focus from the calculated focus step position.  The correction is calcualted from a curve through several of these points.  
- addBFLCorrection, removeBFLCorrectionByIndex: add or remove compensation points to the BFL correction curve.  
## Other support functions
- NA2FNum: convert numeric aperture to F/#
- FNum2NA: convert F/# to numeric aperture
- FOV2AOV: convert field of view at a given object distance to angle of view

This software module is in beta test mode.  There may be bugs and the functions may change if corrections or enhancements are required.  Please send any comments about issues to the contact information below.  

# License
Theia Technologies proprietary and confidential license
Copyright 2023 Theia Technologies

# Contact information
For more information contact: 
Mark Peterson at Theia Technologies
[mpeterson@theiatech.com](mailto://mpeterson@theiatech.com)

# Revision
v.1.1.1