# Theia IQ Smart lens calculations and motor control functions
# (c)2023 Theia Technologies

import numpy.polynomial.polynomial as nppp
import numpy as np
from scipy import optimize
from typing import Tuple


# These functions are ease of use functions for setting and getting motor step positions
# and relating them to engineering units.
# Initialize the class to access the variables.  Then call the loadData function to add the calibration data
# for use in all the calculations
class IQSmart():
    DEFAULT_SPEED = 1000                # default motor (focus/zoom) speed
    DEFAULT_REL_STEP = 1000             # default number of relative steps
    DEFAULT_SPEED_IRIS = 100            # default iris motor speed
    DEFAULT_IRIS_STEP = 10              # default number of iris relative steps
    INFINITY = 1e6                      # infinite object distance
    OD_MIN_DEFAULT = 2                  # default minimum object distance is not specified in the calibration data file
    COC = 0.020                         # circle of confusion for DoF calcualtion

    # error list
    OK = 'OK'
    ERR_NO_CAL = 'no cal data'          # no calibration data loaded
    ERR_FL_MIN = 'FL min'               # minimum focal length exceeded
    ERR_FL_MAX = 'FL max'               # maximum focal length exceeded
    ERR_OD_MIN = 'OD min'               # minimum object distance exceeded
    ERR_OD_MAX = 'OD max'               # maximum object distance (1000000 (infinity)) exceeded
    ERR_OD_VALUE = 'OD value'           # OD not specified
    ERR_NA_MIN = 'NA min'               # minimum numerical aperture exceeded
    ERR_NA_MAX = 'NA max'               # maximum numerical aperture exceeded
    ERR_RANGE_MIN = 'out of range-min'  # out of allowable range
    ERR_RANGE_MAX = 'out of range-max'  # out of allowable range
    ERR_CALC = 'calculation error'      # calculation error (infinity or divide by zero or other)
    WARN_VALUE = 'value warning'        # warning if value seems extreme, possible unit conversion issue

    ### setup functions ###
    def __init__(self):
        self.calData = {}
        self.COC = IQSmart.COC

        # back focal length correction values
        self.BFLCorrectionValues = []
        self.BFLCorrectionCoeffs = []

    # load the calibration data
    # Validate there is data in the variable
    # return: ['OK' | 'no cal data']
    def loadData(self, calData) -> str:
        self.calData = calData
        if calData == {}:
            return IQSmart.ERR_NO_CAL
        return IQSmart.OK

    # load a custom circle of confusion value over the default 0.020mm.
    # A value outside the reasonable range can be set.  The function will return a warning but not prevent it.
    # input: value in mm
    # return: ['OK' | 'value warning']
    def loadCOC(self, COC) -> str:
        self.COC = COC
        # check for validity, expecting a value between extremes 0.005mm and 0.100mm
        if COC < 0.005 or COC > 0.100:
            return IQSmart.WARN_VALUE
        return IQSmart.OK


    ### ----------------------------------------------- ###
    ### convert motor step numbers to engineering units ###
    ### ----------------------------------------------- ###

    # calculate the focal length from zoom step
    # If the calculated focal length is outside the min/max range the value may not be accurate due to curve
    # fitting extrapolation.  But the note will indicate min/max limits are exceeded.
    # FLMin and FLMax are read from the calibration data file.  They are not calculated.
    # input: zoomStep: zoom motor step number
    # return: (calculated focal length, note, FL Min, FL Max)
    # note: ['OK', 'no cal data', 'FL min', 'FL max']
    def zoomStep2FL(self, zoomStep:int) -> Tuple[float, str, float, float]:
        if 'FL' not in self.calData.keys(): return 0, IQSmart.ERR_NO_CAL, 0, 0

        # extract the inverse polynomial coefficients
        coef = self.calData['FL']['coefInv'][0]

        # calculate the result
        FL = nppp.polyval(zoomStep, coef)

        # validate the response
        err = IQSmart.OK
        flMin = self.calData['flMin']
        flMax = self.calData['flMax']
        if (FL < flMin):
            err = IQSmart.ERR_FL_MIN
        elif (FL > flMax):
            err = IQSmart.ERR_FL_MAX
        return FL, err, flMin, flMax

    # calculate the object distance from the focus step
    # If the calculated OD is not close to the nomial range, return out of bounds errors or else
    # calculate the value and validate for out of bounds errors (this method should avoid curve fitting anomnolies)
    # if the min/max limits are exceeded the OD reported may not be accurate.  But the note will
    # indicate a min/max OD exceeded error.
    # ODmin is read from the calibration data file, not calculated.
    # input: focusStep: focus motor step number
    #       zoomStep: zoom motor step number
    #       BFL (optional: 0): back focus correction in focus steps
    # return: (calculated object distance, note, OD min, OD max)
    # note: ['OK', 'no cal data', 'OD min', 'OD max']
    def focusStep2OD(self, focusStep:int, zoomStep:int, BFL:int=0) -> Tuple[float, str, float, float]:
        if 'tracking' not in self.calData.keys(): return 0, IQSmart.ERR_NO_CAL, 0, 0
        # calculation range limit constants, don't calculate outside these limits to avoid curve fitting wrap-around
        DONT_CALC_MAX_OVER = 100
        DONT_CALC_MIN_UNDER = 400

        # extract the polynomial coefficients
        cp1List = self.calData['tracking']['cp1']
        coefList = self.calData['tracking']['coef']

        # calculate the focus step at different object distances for the zoom step
        # add the BFL correction factor
        focusStepList = []
        for cp1, _val in enumerate(cp1List):
            focusStepList.append(nppp.polyval(zoomStep, coefList[cp1]) + BFL)

        # validate the focus step to make sure it is within the valid focus range
        err = IQSmart.OK
        OD = 0
        ODMin = self.calData['odMin'] if 'odMin' in self.calData.keys() else IQSmart.OD_MIN_DEFAULT
        ODMax = self.calData['odMax'] if 'odMax' in self.calData.keys() else IQSmart.INFINITY

        #   range goes from infinity focus [0] to minimum focus [len(cp1)]
        if focusStep > focusStepList[0] + DONT_CALC_MAX_OVER:
            # likely outside valid focus range
            err = IQSmart.ERR_OD_MAX
        elif focusStep < focusStepList[-1] - DONT_CALC_MIN_UNDER:
            # likely outside valid focus range
            err = IQSmart.ERR_OD_MIN
        else:
            # fit the focusStepList/cp1List to find the object distance
            coef = nppp.polyfit(focusStepList, cp1List, 3)
            OD = 1000 / nppp.polyval(focusStep, coef)
            # validate OD
            if OD < 0:
                # points >infinity are calculaed as negative
                err = IQSmart.ERR_OD_MAX
            elif OD < ODMin:
                err = IQSmart.ERR_OD_MIN
        return OD, err, ODMin, ODMax

    # calculate the numeric aperture from iris motor step
    # if the calculated NA is outside the range, return the calculated value but set the note error
    # to indicate min/max exceeded
    # input: irisStep: iris motor step number
    #       FL: focal length
    #       rangeLimit (optional: True): limit the calcuated value to the range
    # return: (NA, note, NAMin, NAMax)
    # note: ['OK', 'no cal data', 'NA max', 'NA min']
    def irisStep2NA(self, irisStep:int, FL:float, rangeLimit:bool=True) -> Tuple[float, str, float, float]:
        if 'AP' not in self.calData.keys(): return 0, IQSmart.ERR_NO_CAL, 0, 0

        # extract data from calibration data file
        NA = self.interpolate(self.calData['AP']['coef'], self.calData['AP']['cp1'], FL, irisStep)

        # calculate min/max values
        NAMin = self.interpolate(self.calData['AP']['coef'], self.calData['AP']['cp1'], FL, self.calData['irisSteps'])
        NAMax = self.interpolate(self.calData['AP']['coef'], self.calData['AP']['cp1'], FL, 0)

        # validate the results
        NAMaxCal = (1/(2 * self.calData['fnum']))

        # set the maximum NA to lesser of calculated value from the curve or calibration data value from the file
        NAMax = min(NAMax, NAMaxCal)
        NAMin = max(NAMin, 0.01)
        err = IQSmart.OK
        if NA > NAMax:
            err = IQSmart.ERR_NA_MAX
            if rangeLimit: NA = NAMax
        elif NA < NAMin:
            err = IQSmart.ERR_NA_MIN
            if rangeLimit: NA = NAMin
        return NA, err, NAMin, NAMax

    # calculate the F/# from the iris motor step
    # calculations are propogated using numeric aperture to avoid division by zero so this
    # function calculates NA first and inverts the results
    # input: irisStep: iris motor step number
    #       FL: focal length
    # return: (FNum, note, FNumMin, FNumMax)
    # note: ['OK', 'no cal data', 'NA max', 'NA min']
    def irisStep2FNum(self, irisStep:int, FL:float) -> Tuple[float, str, float, float]:
        if 'AP' not in self.calData.keys(): return 0, IQSmart.ERR_NO_CAL, 0, 0
        NA, err, NAMin, NAMax = self.irisStep2NA(irisStep, FL)
        fNum = self.NA2FNum(NA)
        fNumMin = self.NA2FNum(NAMin)
        fNumMax = self.NA2FNum(NAMax)
        return fNum, err, fNumMin, fNumMax


    ### ----------------------------------------------- ###
    ### convert engineering units to motor step numbers ###
    ### ----------------------------------------------- ###

    # calculate the zoom step from the focal length
    # Keep the zoom step in the available range.
    # input: FL: focal length
    # return: (zoomStep, note)
    # note: ['OK' | 'no cal data' | 'out of range-min' | 'out of range-max']
    def FL2ZoomStep(self, FL:float) -> Tuple[int, str]:
        if 'FL' not in self.calData.keys(): return 0, IQSmart.ERR_NO_CAL

        # extract the polynomial coefficients
        coef = self.calData['FL']['coef'][0]

        # calculate the result
        zoomStep = int(nppp.polyval(FL, coef))

        # validate the response
        err = IQSmart.OK
        zoomStepMax = self.calData['zoomSteps']
        if (zoomStep < 0):
            err = IQSmart.ERR_RANGE_MIN
            zoomStep = 0
        elif (zoomStep > zoomStepMax):
            err = IQSmart.ERR_RANGE_MAX
            zoomStep = zoomStepMax
        return zoomStep, err

    # calculate object distance from focus motor step
    # Limit the focus motor step to the available range.
    # maximum object distance input can be 1000000m (infinity).  Minimum object distance
    # can be 0 but focus motor step may not support this minimum.  Also, the focus/zoom
    # calculation can cause fitting errors outside the acceptable range.
    # input: OD: object distance
    #       zoomStep: current zoom motor step position
    #       BFL (optional: 0): back focus step adjustment
    # return: (focusStep, note)
    # note: ('OK' | 'no cal data' | 'out of range-min' | 'out of range-max')
    def OD2FocusStep(self, OD:float, zoomStep:int, BFL:int=0) -> Tuple[int, str]:
        if 'tracking' not in self.calData.keys(): return 0, IQSmart.ERR_NO_CAL

        # extract the focus/zoom tracking polynomial data and interpolate to OD
        if OD == 0:
            # divide by zero error
            OD = 0.001
        invOD = 1000 / OD
        focusStep = int(self.interpolate(self.calData['tracking']['coef'], self.calData['tracking']['cp1'], invOD, zoomStep))
        focusStep += BFL

        # validate the result
        err = IQSmart.OK
        focusStepMax = self.calData['focusSteps']
        if focusStep < 0:
            err = IQSmart.ERR_RANGE_MIN
            focusStep = 0
        elif focusStep > focusStepMax:
            err = IQSmart.ERR_RANGE_MAX
            focusStep = focusStepMax
        return focusStep, err

    # calculate object distance from focus motor step
    # See the description at OD2FocusStep()
    # input: OD: object distance
    #       FL: focal length
    #       BFL (optional: 0): back focus step adjustment
    # return: (focusStep, note)
    # note: ('OK' | 'no cal data' | 'out of range-min' | 'out of range-max')
    def ODFL2FocusStep(self, OD:float, FL:float, BFL:int=0) -> Tuple[int, str]:
        if self.calData == {}: return 0, IQSmart.ERR_NO_CAL
        # get the zoom step
        zoomStep, _err = self.FL2ZoomStep(FL)
        focusStep, err = self.OD2FocusStep(OD, zoomStep, BFL)
        return focusStep, err

    # calculate iris step from numeric aperture
    # if the numeric aperture is not supported for the current focal length, return the
    # min/max iris step position and the out of range error.
    # input: NA: numeric aperture
    #       FL: current focal length
    # return: (iris motor step, note)
    # note: ['OK' | 'no cal data' | 'NA min' | 'NA max']
    def NA2IrisStep(self, NA:float, FL:float) -> Tuple[int, str]:
        if 'AP' not in self.calData.keys(): return 0, IQSmart.ERR_NO_CAL

        # find 2 closest focal lengths in the calibrated data file to the target
        FLList = np.subtract(self.calData['AP']['cp1'], FL)

        # sort the FL differences from 0 (root) and save the list indexes
        FLIdx = np.argsort(np.abs(FLList))
        closestFL = np.add(np.array(FLList)[np.sort(FLIdx[:2])], FL)

        # define the merit function (NA v. irisStep) for the root finding
        def merit(x, coef, target):
            return nppp.polyval(x, coef) - target

        # find the coefficients for each focal length and calcualte the iris step for the target NA
        err = IQSmart.OK
        coef = []
        stepValueList = []
        for f in closestFL:
            idx = self.calData['AP']['cp1'].index(f)
            coef = self.calData['AP']['coef'][idx]
            NAMax = nppp.polyval(0, coef)
            if NA < NAMax:
                try:
                    stepValue = optimize.newton(merit, 20, args=(coef, NA,))
                except RuntimeError as e:
                    # no convergence due to excessively negative NA value
                    stepValue = self.calData['irisSteps']
                    err = IQSmart.ERR_NA_MIN
            else:
                stepValue = 0
                err = IQSmart.ERR_NA_MAX
            stepValueList.append(stepValue)

        # interpolate between step values
        interpolationFactor = (FL - closestFL[0]) / (closestFL[1] - closestFL[0])
        irisStep = int(stepValueList[0] + interpolationFactor * (stepValueList[1] - stepValueList[0]))
        return irisStep, err

    # calcualted the iris motor step from F/#
    # input: fNum: F/#
    #       FL: current focal length
    # return (iris motor step, note)
    # note: ['OK' | 'no cal data' | 'NA min' | 'NA max']
    def fNum2IrisStep(self, fNum:float, FL:float) -> Tuple[int, str]:
        if 'AP' not in self.calData.keys(): return 0, IQSmart.ERR_NO_CAL

        # calcualte the NA
        NA = self.FNum2NA(fNum)

        irisStep, err = self.NA2IrisStep(NA, FL)
        return irisStep, err

    # Angle of view to motor steps
    # calculate the zoom motor step that allows the input angle of view.  If the focal length range
    # doesn't support the FOV, return an out of range error.
    # Also calculate the focus motor step to keep the lens in focus.
    # If the object distance is not specified, use infinity.
    # input: AOV: field of view in meters
    #       IH: image height (sensor width)
    #       OD (optional: infinity): object distance
    #           OD < 0 or OD type string: do not calculate focus motor step position
    #       BFL (optional: 0): back focal length adjustment for focus motor
    # return: (focusStep, zoomStep, calculated focal length, note)
    # note: ['OK' | 'no cal data' | 'out of range-min' | 'out of range-max' | 'OD value']
    def AOV2MotorSteps(self, AOV:float, IH:float, OD:float=1000000, BFL:int=0) -> Tuple[int, int, float, str]:
        if 'dist' not in self.calData.keys(): return 0, 0, 0, IQSmart.ERR_NO_CAL

        # get the maximum angle of view for each focal length in the calibration data file
        FLLower = None
        FLUpper = None
        FLList = np.sort(self.calData['dist']['cp1'])
        for FL in FLList:
            AOVMax, _err = self.calcAOV(IH, FL)
            if AOVMax > AOV:
                FLLower = [FL, AOVMax]
            elif FLUpper == None:
                FLUpper = [FL, AOVMax]

        # check if AOV is greater than maximum AOV for the lens (not wide angle enough)
        if FLLower == None:
            # re-calculate to extrapolate focal length
            FLLower = FLUpper
            FL = FLList[1]
            AOVMax, _err = self.calcAOV(IH, FL)
            FLUpper = [FL, AOVMax]

        # check if AOV is less than the minimum AOV for the lens (not telephoto enough)
        if FLUpper == None:
            # recalcualte to extrapolate focal length
            FLUpper = FLLower
            FL = FLList[-2]
            AOVMax, _err = self.calcAOV(IH, FL)
            FLLower = [FL, AOVMax]

        # interpolate to get the focal length value
        interpolationFactor = (AOV - FLLower[1]) / (FLUpper[1] - FLLower[1])
        FLValue = FLLower[0] + interpolationFactor * (FLUpper[0] - FLLower[0])

        # validate FL range
        err = IQSmart.OK
        if FLValue < self.calData['flMin']:
            err = IQSmart.ERR_RANGE_MIN
        elif FLValue > self.calData['flMax']:
            err = IQSmart.ERR_RANGE_MAX

        # calculate zoom step from focal length
        zoomStep, _err = self.FL2ZoomStep(FLValue)

        # check if object distance is valid
        if isinstance(OD, str):
            return 0, zoomStep, FLValue, IQSmart.ERR_OD_VALUE
        elif OD < 0:
            return 0, zoomStep, FLValue, IQSmart.ERR_OD_VALUE

        # calculate focus step using focus/zoom curve
        focusStep, _err = self.OD2FocusStep(OD, zoomStep, BFL)

        return focusStep, zoomStep, FLValue, err

    # field of view to motor steps
    # Calculate the zoom motor step that allows the field of view.  If the focal length
    # is out of range, return a range error but also the calculated focal length.
    # The zoom and focus motor steps won't exceed the limits.
    # input: FOV: field of view in meters
    #       IH: image height (sensor width)
    #       OD (optional: infinity): object distance in meters
    #           OD < 0 or OD type string: do not calculate focus motor step position
    #       BFL (optional: 0): back focus step adjustment
    # return: (focusStep, zoomStep, calcualted FL, note)
    # note: ['OK' | 'no cal data' | 'out of range-min' | 'out of range-max' | 'calculation error' | 'OD value']
    def FOV2MotorSteps(self, FOV:float, IH:float, OD:float=1000000, BFL:int=0) -> Tuple[int, int, float, str]:
        if 'dist' not in self.calData.keys(): return 0, 0, 0, IQSmart.ERR_NO_CAL
        AOV = self.FOV2AOV(FOV, OD)
        if AOV == 0:
            return 0, 0, 0, IQSmart.ERR_CALC
        focusStep, zoomStep, FLValue, err = self.AOV2MotorSteps(AOV, IH, OD, BFL)
        return focusStep, zoomStep, FLValue, err


    ### --------------------------------------- ###
    ### complex calculations, engineering units ###
    ### --------------------------------------- ###

    # calculate angle of view
    # calculate the full angle
    # input: sensorWd: width of sensor for horizontal AOV
    #       FL: focal length
    # return: (full angle of view (deg), note)
    # note: ['OK', 'no cal data']
    def calcAOV(self, sensorWd:float, FL:float) -> Tuple[float, str]:
        if 'dist' not in self.calData.keys(): return 0, IQSmart.ERR_NO_CAL
        semiWd = sensorWd / 2

        # extract the object angle value
        semiAOV = abs(self.interpolate(self.calData['dist']['coef'], self.calData['dist']['cp1'], FL, semiWd))
        AOV = 2 * semiAOV
        return AOV, IQSmart.OK

    # calculate field of view
    # calculate the full field of view width in meters
    # input: sensorWd: width of sensor for horizontal FOV
    #       FL: focal length
    #       OD (optional, infinity): object distance
    # return: (full field of view (m), note)
    # note: ['OK', 'no cal data']
    def calcFOV(self, sensorWd:float, FL:float, OD:float=1000000) -> Tuple[float, str]:
        if 'dist' not in self.calData.keys(): return 0, IQSmart.ERR_NO_CAL
        AOV, _err  = self.calcAOV(sensorWd, FL)

        # calcualte the FOV at the object distance
        FOV = 2 * OD * np.tan(np.radians(AOV / 2))
        return FOV, IQSmart.OK

    # calcualte depth of field (object distance min/max)
    # calcualte the minimum and maximum object distances.  The difference is the depth of field
    # input: irisStep: iris motor step position
    #       FL: focal length
    #       OD (optional: infinity): object distance
    # return: (depth of field, note, minimum object distance, maximum object distance)
    # note: ['OK' | 'no cal data']
    def calcDOF(self, irisStep:int, FL:float, OD:float=1000000) -> Tuple[float, float, str]:
        if 'iris' not in self.calData.keys(): return 0, IQSmart.ERR_NO_CAL, 0, 0
        if OD >= IQSmart.INFINITY: return IQSmart.INFINITY, IQSmart.OK, IQSmart.INFINITY, IQSmart.INFINITY

        # extract the aperture size
        shortDiameter = self.interpolate(self.calData['iris']['coef'], self.calData['iris']['cp1'], FL, irisStep)

        # calculate the magnification
        OD = max(0.001, OD)
        magnification = (FL / 1000) / OD

        # calculate min and max object distances
        # denominator ratios are unitless so calculations are in the units of object distance
        ODMin = min(OD / (1 + self.COC / (shortDiameter * magnification)), IQSmart.INFINITY)
        ODMax = min(OD / (1 - self.COC / (shortDiameter * magnification)), IQSmart.INFINITY)
        if ODMax < 0: ODMax = IQSmart.INFINITY

        # calculate depth of field
        if ODMax == IQSmart.INFINITY:
            DOF = IQSmart.INFINITY
        else:
            DOF = ODMax - ODMin

        return DOF, IQSmart.OK, ODMin, ODMax

    # calculate full depth of field
    # calculate the full depth of field from nearest object to farthest based on set circle of confusion
    # **Not too useful.  More useful is calculating the min/max object distances (see calcDOF())
    # input: irisStep: iris motor step position
    #       FL: focal length
    #       OD (optional, Infinity): Object distance
    # return: (depth of field in meters, note)
    # note: ['OK', 'no cal data']
    def calcFullDOF(self, irisStep:int, FL:float, OD:float=1000000) -> Tuple[float, str]:
        if 'iris' not in self.calData.keys(): return 0, IQSmart.ERR_NO_CAL

        # extract the aperture size
        shortDiameter = self.interpolate(self.calData['iris']['coef'], self.calData['iris']['cp1'], FL, irisStep)

        # calcualte full depth of field
        DOF = (2 * (OD * 1000)**2 * self.COC) / (FL * shortDiameter)

        # convert to standard meters
        DOF = DOF / 1000
        return DOF, IQSmart.OK


    ### -------------------------------------- ###
    ### back focal length correction functions ###
    ### -------------------------------------- ###

    # back focal length correction factor
    # Tolerances in the lens to sensor position will cause an offset in the
    # focus motor step position.  This function calculates the focus
    # step correction for the current focal length.
    # input: FL: focal length
    #       OD: (optional: infinity): object distance in meters
    # globals: read BFL correction coefficients to do the fit
    # return: focus step difference
    ##### TBD add object distance OD; currently all OD will be included in the fitting together
    def BFLCorrection(self, FL:float, OD:float=1000000) -> int:
        if len(self.BFLCorrectionCoeffs) == 0:
            # no correction values set up yet
            return 0
        # calculate the correction step for the focal length
        correctionValue = nppp.polyval(FL, self.BFLCorrectionCoeffs)
        return int(correctionValue)

    # store data points for BFL correction
    # Add a focus shift amount to the list and fit for focal length [[FL, focus shift], [...]]
    # input: focusStep: focus step position for best focus
    #       FL: current focal length
    #       OD: (optional: infinity): current object distance in meters
    # global data: update BFL correction fit parameters
    # return: Current set point BFL correction list [[FL, step, OD],[...]]
    def addBFLCorrection(self, focusStep:int, FL:float, OD:float=1000000) -> list:
        # find the default focus step for infinity object distance
        designFocusStep, _err = self.ODFL2FocusStep(OD, FL, BFL=0)

        # save the focus shift amount
        self.BFLCorrectionValues.append([FL, focusStep - designFocusStep, OD])

        # re-fit the data
        self.fitBFLCorrection()
        return self.BFLCorrectionValues

    # remove BFL correction point
    # remove a point in the list by index number.
    # If the index is not in the list then nothing is removed
    # input: idx: index number (starting at 0) to remove
    # return: updated set point BFL correction list [[FL, step, OD],[...]]
    def removeBFLCorrectionByIndex(self, idx:int) -> list:
        if idx < 0 or idx >= len(self.BFLCorrectionValues):
            return self.BFLCorrectionValues

        # delete the item
        del self.BFLCorrectionValues[idx]

        # re-fit the data
        self.fitBFLCorrection()
        return self.BFLCorrectionValues

    # curve fit the BFL correction list
    # Updates the class variables, no input or return value
    def fitBFLCorrection(self):
        xy = np.transpose(self.BFLCorrectionValues)
        # fit the data
        if len(self.BFLCorrectionValues) == 1:
            # single data point, constant offset
            self.BFLCorrectionCoeffs = xy[1]
        elif len(self.BFLCorrectionValues) <= 3:
            # linear fit for up to 3 data points
            self.BFLCorrectionCoeffs = nppp.polyfit(xy[0], xy[1], 1)
        else:
            # quadratic fit for > 3 data points
            self.BFLCorrectionCoeffs = nppp.polyfit(xy[0], xy[1], 2)


    ### ----------------- ###
    ### support functions ###
    ### ----------------- ###

    # calculate F/# from NA
    # use the simple inversion formula
    # input: NA: numeric aperture
    # return: F/#
    def NA2FNum(self, NA:float) -> float:
        if NA == 0:
            return 10000
        return 1 / (2 * NA)

    # calculate NA from F/#
    # use the simple inversion formula
    # input: F/#
    # return: NA
    def FNum2NA(self, fNum:float) -> float:
        if fNum == 0:
            return 1    # max possible NA in air
        return 1 / (2 * fNum)

    # calcualte angle of view from field of view
    # input: FOV: field of view in meters
    #       OD (optional: infinity): object distance
    # return: angle of view
    def FOV2AOV(self, FOV:float, OD:float=1000000) -> float:
        # check for 'infinity' input to FOV or OD
        if isinstance(FOV, str) or isinstance(OD, str) or (OD == 0) or (FOV == 0):
            return 0
        AOV = np.degrees(2 * np.arctan((FOV / 2) / OD))
        return AOV

    # interpolate/ extrapolate between two values of control points
    # this function has coefficients for a polynomial curve at each of the control points cp1.
    # The curves for the two closest control points around the target are selected and the
    # xValue is calculated for each.  Then the results are interpolated to get to the cp1 target.
    # input: coefficient list of lists for all cp1 values
    #       cp1 control point 1 list corresponding to the coefficients
    #       target control point target
    #       x evaluation value
    # return: interpolated value
    def interpolate(self, coefList:list, cp1List:list, cp1Target:float, xValue:float) -> float:
        # check for only one data set
        if len(cp1List) <= 1:
            return nppp.polyval(cp1Target, coefList[0])

        # Find the indices of the closest lower and upper cp1 values
        valList = np.subtract(cp1List, cp1Target)
        valIdx = np.argsort(np.abs(valList))

        # Extract the corresponding lower and upper coefficients
        lowerCoeffs = coefList[valIdx[0]]
        upperCoeffs = coefList[valIdx[1]]

        # calculate the values
        lowerValue = nppp.polyval(xValue, lowerCoeffs)
        upperValue = nppp.polyval(xValue, upperCoeffs)

        # Calculate the interpolation factor
        interpolation_factor = (cp1Target - cp1List[valIdx[0]]) / (cp1List[valIdx[1]] - cp1List[valIdx[0]])

        # Interpolate between the lower and upper coefficients
        interpolatedValue = lowerValue + interpolation_factor * (upperValue - lowerValue)

        return interpolatedValue