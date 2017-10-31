import wpilib

from networktables import NetworkTable
from networktables.util import ntproperty
import math

# Define constants. This way if we need to change something we don't have to change it 50 times.
ENCODER_ROTATION = 1023
WHEEL_DIAMETER = 7.639
class Drive:
    """
        The sole interaction between the robot and its driving system
        occurs here. Anything that wants to drive the robot must go
        through this class.
    """
    #robot_drive = wpilib.RobotDrive


    sd = NetworkTable


    def __init__(self):
        self.sd = NetworkTable.getTable('/SmartDashboard')
        self.angle_P = self.sd.getAutoUpdateValue('Drive/Angle_P', .055)
        self.angle_I = self.sd.getAutoUpdateValue('Drive/Angle_I', 0)
        self.drive_constant = self.sd.getAutoUpdateValue('Drive/Drive_Constant', .0001)
        self.rotate_max = self.sd.getAutoUpdateValue('Drive/Max Gyro Rotate Speed', .37)

        self.enabled = False
        self.align_angle = None
        self.align_print_timer = wpilib.Timer()
        self.align_print_timer.start()

    def on_enable(self):
        """
            Constructor.
            :param robotDrive: a `wpilib.RobotDrive` object
            :type rf_encoder: DriveEncoders()
            :type lf_encoder: DriveEncoders()
        """

        # Hack for one-time initialization because magicbot doesn't support it
        if not self.enabled:
            nt = NetworkTable.getTable('components/autoaim')
            nt.addTableListener(self._align_angle_updated, True, 'target_angle')

        self.isTheRobotBackwards = False
        self.iErr = 0
        # set defaults here
        self.y = 0
        self.rotation = 0
        self.squaredInputs = False

        self.halfRotation = 1





    # Verb functions -- these functions do NOT talk to motors directly. This
    # allows multiple callers in the loop to call our functions without
    # conflicts.

    def _align_angle_updated(self, source, key, value, isNew):
        # store the absolute value that we need to go to
        self.align_angle = value + self.return_gyro_angle()
        self.align_angle_nt = self.align_angle

    def move(self, y, rotation, squaredInputs=False):
        """
            Causes the robot to move
            :param x: The speed that the robot should drive in the X direction. 1 is right [-1.0..1.0]
            :param y: The speed that the robot should drive in the Y direction. -1 is forward. [-1.0..1.0]
            :param rotation:  The rate of rotation for the robot that is completely independent of the translation. 1 is rotate to the right [-1.0..1.0]
            :param squaredInputs: If True, the x and y values will be squared, allowing for more gradual speed.
        """
        self.y = max(min(y, 1), -1)
        self.rotation = max(min(1.0, rotation), -1)
        self.squaredInputs = squaredInputs

    def set_angle_constant(self, constant):
        """Sets the constant that is used to determine the robot turning speed"""
        self.angle_constant = constant

    def _get_inches_to_ticks(self, inches):
        """Converts inches to encoder ticks"""

        gear_ratio = 50 / 12
        target_position = (gear_ratio * ENCODER_ROTATION * inches) / (math.pi*WHEEL_DIAMETER)
        return target_position

    def drive_distance(self, inches, max_speed=.9):

        return self.encoder_drive(self._get_inches_to_ticks(inches), max_speed)


    def set_direction(self, direction):
        """Used to reverse direction"""
        self.isTheRobotBackwards = bool(direction)

    def switch_direction(self):
        """when called the robot will reverse front/back"""
        self.isTheRobotBackwards = not self.isTheRobotBackwards

    def halveRotation(self):
        self.halfRotation = .5

    def normalRotation(self):
        self.halfRotation = 1

    def execute(self):
        """Actually makes the robot drive"""
        backwards = -1 if self.isTheRobotBackwards else 1

        if(self.isTheRobotBackwards):
            self.robot_drive.arcadeDrive(-self.y, -self.rotation / 2, self.squaredInputs)
        else:
            self.robot_drive.arcadeDrive(self.y, -self.rotation * self.halfRotation, self.squaredInputs)


        # by default, the robot shouldn't move
        self.y = 0
        self.rotation = 0
