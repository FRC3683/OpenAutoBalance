import math
import wpilib


class AutoBalance:
    def __init__(self):
        self.mRioAccel = wpilib.BuiltInAccelerometer()

        self.state = 0
        self.debounceCount = 0

        ##########
        # CONFIG #
        ##########

        # Speed the robot drived while scoring/approaching station, default = 0.4
        self.robotSpeedFast = 0.4

        # Speed the robot drives while balancing itself on the charge station.
        # Should be roughly half the fast speed, to make the robot more accurate, default = 0.2
        self.robotSpeedSlow = 0.2

        # Angle where the robot knows it is on the charge station, default = 13.0
        self.onChargeStationDegree = 13.0

        # Angle where the robot can assume it is level on the charging station
        # Used for exiting the drive forward sequence as well as for auto balancing, default = 6.0
        self.levelDegree = 6.0

        # Amount of time a sensor condition needs to be met before changing states in seconds
        # Reduces the impact of sensor noice, but too high can make the auto run slower, default = 0.2
        self.debounceTime = 0.2

        # Amount of time to drive towards to scoring target when trying to bump the game piece off
        # Time it takes to go from starting position to hit the scoring target
        self.singleTapTime = 0.4

        # Amount of time to drive away from knocked over gamepiece before the second tap
        self.scoringBackUpTime = 0.2

        # Amount of time to drive forward to secure the scoring of the gamepiece
        self.doubleTapTime = 0.3

    def getPitch(self) -> float:
        return (
            math.atan2(
                (-self.mRioAccel.getX()),
                math.sqrt(
                    self.mRioAccel.getY() * self.mRioAccel.getY()
                    + self.mRioAccel.getZ() * self.mRioAccel.getZ()
                ),
            )
            * 57.3
        )

    def getRoll(self) -> float:
        return math.atan2(self.mRioAccel.getY(), self.mRioAccel.getZ()) * 57.3

    def getTilt(self) -> float:
        """returns the magnititude of the robot's tilt calculated by the root of
        pitch^2 + roll^2, used to compensate for diagonally mounted rio

        """
        if (self.getPitch() + self.getRoll()) >= 0:
            return math.sqrt(
                self.getPitch() * self.getPitch() + self.getRoll() * self.getRoll()
            )
        else:
            return -math.sqrt(
                self.getPitch() * self.getPitch() + self.getRoll() * self.getRoll()
            )

    def secondsToTicks(self, time: float) -> int:
        return int(time * 50)

    def autoBalanceRoutine(self) -> float:
        """
        routine for automatically driving onto and engaging the charge station.
        returns a value from -1.0 to 1.0, which left and right motors should be set to.
        """
        if self.state == 0:
            # drive forwards to approach station, exit when tilt is detected
            if self.getTilt() > self.onChargeStationDegree:
                self.debounceCount += 1

            if self.debounceCount > self.secondsToTicks(self.debounceTime):
                self.state = 1
                self.debounceCount = 0
                return self.robotSpeedSlow

            return self.robotSpeedFast

        elif self.state == 1:
            # driving up charge station, drive slower, stopping when level
            if self.getTilt() < self.levelDegree:
                self.debounceCount += 1

            if self.debounceCount > self.secondsToTicks(self.debounceTime):
                self.state = 2
                self.debounceCount = 0
                return 0

            return self.robotSpeedSlow

        elif self.state == 2:
            # on charge station, stop motors and wait for end of auto
            if abs(self.getTilt()) <= self.levelDegree / 2:
                self.debounceCount += 1

            if self.debounceCount > self.secondsToTicks(self.debounceTime):
                self.state = 4
                self.debounceCount = 0
                return 0

            if self.getTilt() >= self.levelDegree:
                return 0.1
            elif self.getTilt() <= -self.levelDegree:
                return -0.1

        else:
            return 0

    def scoreAndBalance(self) -> float:
        """
        Same as auto balance above, but starts auto period by scoring
        a game piece on the back bumper of the robot
        """
        if self.state == 0:
            # drive back, then forwards, then back again to knock off and score game piece
            self.debounceCount += 1
            if self.debounceCount < self.secondsToTicks(self.singleTapTime):
                return -self.robotSpeedFast
            elif self.debounceCount < self.secondsToTicks(
                self.singleTapTime + self.scoringBackUpTime
            ):
                return self.robotSpeedFast
            elif self.debounceCount < self.secondsToTicks(
                self.singleTapTime + self.scoringBackUpTime + self.doubleTapTime
            ):
                return -self.robotSpeedFast
            else:
                self.debounceCount = 0
                self.state = 1
                return 0

        elif self.state == 1:
            # drive forwards until on charge station
            if self.getTilt() > self.onChargeStationDegree:
                self.debounceCount += 1

            if self.debounceCount > self.secondsToTicks(self.debounceTime):
                self.state = 2
                self.debounceCount = 0
                return self.robotSpeedSlow

            return self.robotSpeedFast

        elif self.state == 2:
            # driving up charge station, drive slower, stopping when level
            if self.getTilt() < self.levelDegree:
                self.debounceCount += 1

            if self.debounceCount > self.secondsToTicks(self.debounceTime):
                self.state = 3
                self.debounceCount = 0
                return 0

            return self.robotSpeedSlow

        elif self.state == 3:
            # on charge station, ensure robot is flat, then end auto
            if abs(self.getTilt()) <= self.levelDegree / 2:
                self.debounceCount += 1

            if self.debounceCount > self.secondsToTicks(self.debounceTime):
                self.state = 4
                self.debounceCount = 0
                return 0

            if self.getTilt() >= self.levelDegree:
                return self.robotSpeedSlow / 2
            elif self.getTilt() <= -self.levelDegree:
                return -self.robotSpeedSlow / 2

        return 0
