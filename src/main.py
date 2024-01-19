# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       wandows man                                                  #
# 	Created:      10/13/2023, 9:01:10 a.m.                                       #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

# Brain should be defined by default
brain=Brain()

# Define the controller
controller1 = Controller(ControllerType.PRIMARY)
# controller2 = Controller(ControllerType.PARTNER)

# Define Motors
# variable = Motor(port number, gear ratio (green=18-1, red=36-1, blue=6-1), reverse)

leftMotor = Motor(Ports.PORT20, GearSetting.RATIO_18_1, False)
rightMotor = Motor(Ports.PORT10, GearSetting.RATIO_18_1, True)
drivetrain = DriveTrain(leftMotor, rightMotor)

clawMotor = Motor(Ports.PORT8, GearSetting.RATIO_18_1, True)
armMotor = Motor(Ports.PORT16, GearSetting.RATIO_18_1, True)

inertialSensor = Inertial(Ports.PORT9)


def preauton():
    armMotor.set_stopping(HOLD)
    inertialSensor.calibrate()

def autonomous():
    drivetrain.drive_for(FORWARD, 48, INCHES)
    drivetrain.turn(LEFT)
    while (inertialSensor.rotation() > -90):
        wait(20, MSEC)
    drivetrain.stop()
    armMotor.spin_for(FORWARD, 180 * 7)
    clawMotor.spin_for(FORWARD, 360)


def drivercontrol():
    while True:
    
        leftMotor.spin(FORWARD, controller1.axis3.position() + (controller1.axis1.position() / 2), PERCENT)
        rightMotor.spin(FORWARD, controller1.axis3.position() - (controller1.axis1.position() / 2), PERCENT)


        #clawMotor.spin_for(FORWARD, controller1.axis4.position(), PERCENT)

        if (controller1.buttonL1.pressing()):
            clawMotor.spin(FORWARD, 100, PERCENT)
        elif (controller1.buttonL2.pressing()):
            clawMotor.spin(REVERSE, 100, PERCENT)
        else:
            clawMotor.stop()


        if (controller1.buttonR1.pressing()):
            armMotor.spin(FORWARD, 50, PERCENT)
        elif (controller1.buttonR2.pressing()):
            armMotor.spin(REVERSE, 50, PERCENT)
        else:
            armMotor.stop()

        wait(20, MSEC)


competition = Competition(drivercontrol, autonomous)
preauton()