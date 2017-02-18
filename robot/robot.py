#!/usr/bin/env python3

import magicbot
import wpilib

from robotpy_ext.control.button_debouncer import ButtonDebouncer
from networktables.util import ntproperty
from components import drive

from robotpy_ext.common_drivers import navx

from networktables.networktable import NetworkTable

class MyRobot(magicbot.MagicRobot):
    mode = 'tankdrive'
    counter = 0
    #drive = drive.Drive
    """Create basic components (motor controllers, joysticks, etc.)"""
    def createObjects(self):
        # NavX (purple board on top of the RoboRIO)
        # self.navX = navx.AHRS.create_spi()

        # Initialize SmartDashboard
        self.sd = NetworkTable.getTable('SmartDashboard')

        # Joysticks
        #self.left_joystick = wpilib.Joystick(0)
        #self.right_joystick = wpilib.Joystick(1)
        self.joystick = wpilib.Joystick(0)
        self.switch = ButtonDebouncer(self.joystick, 1)
        # TODO: Motors
        self.lf_motor = wpilib.Victor(0)
        self.lr_motor = wpilib.Victor(1)
        self.rf_motor = wpilib.Victor(2)
        self.rr_motor = wpilib.Victor(3)

        # TODO: Drivetrain object

        #self.robot_drive = wpilib.RobotDrive(self.lf_motor, self.lr_motor, self.rf_motor, self.rr_motor)


    def autonomous(self):
        """Prepare for autonomous mode"""
        pass

    def disabledPeriodic(self):
        """Repeat periodically while robot is disabled. Usually emptied. Sometimes used to easily test sensors and other things."""
        pass

    def disabledInit(self):
        """Do once right away when robot is disabled."""

    def teleopInit(self):
        """Do when teleoperated mode is started."""
        pass

    def teleopPeriodic(self):
        """Do periodically while robot is in teleoperated mode."""
        #self.drive.move(-self.left_joystick.getY(), self.right_joystick.getX())
        #leftStick, leftAxis, rightStick, rightAxis
        #self.robot_drive.tankDrive(self.joystick, 1, self.joystick, 3)

        #if self.counter%1000 == 0:
            #print(self.joystick.getRawAxis(1))
            #print(self.mode)
        if self.mode == 'tankdrive':
            self.lf_motor.set(-1*self.joystick.getRawAxis(1))
            self.lr_motor.set(-1*self.joystick.getRawAxis(1))
            self.rf_motor.set(self.joystick.getRawAxis(3))
            self.rr_motor.set(self.joystick.getRawAxis(3))
        elif self.mode == 'arcade':
            self.steering = self.joystick.getRawAxis(2) + 1
            self.power = self.joystick.getRawAxis(1)
            self.lf_motor.set(-self.power*self.steering)
            self.lr_motor.set(-self.power*self.steering)
            self.rf_motor.set(self.power*(2-self.steering))
            self.rr_motor.set(self.power*(2-self.steering))
        if self.switch.get():
            self.mode = 'arcade' if self.mode == 'tankdrive' else 'tankdrive'
            print('switched to ' + self.mode)



if __name__ == '__main__':
    wpilib.run(MyRobot)
