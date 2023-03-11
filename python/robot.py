#!/usr/bin/env python3

import rev
import wpilib

import auto_balance


class MyRobot(wpilib.TimedRobot):
    def robotInit(self) -> None:
        self.mLF = rev.CANSparkMax(2, rev.CANSparkMax.MotorType.kBrushless)
        self.mLB = rev.CANSparkMax(3, rev.CANSparkMax.MotorType.kBrushless)
        self.mRF = rev.CANSparkMax(4, rev.CANSparkMax.MotorType.kBrushless)
        self.mRB = rev.CANSparkMax(5, rev.CANSparkMax.MotorType.kBrushless)

        self.mAutoBalance = auto_balance.AutoBalance()

    def disabledInit(self) -> None:
        self.mLF.setIdleMode(rev.CANSparkMax.IdleMode.kCoast)
        self.mLB.setIdleMode(rev.CANSparkMax.IdleMode.kCoast)
        self.mRF.setIdleMode(rev.CANSparkMax.IdleMode.kCoast)
        self.mRB.setIdleMode(rev.CANSparkMax.IdleMode.kCoast)

    def disabledPeriodic(self) -> None:
        pass

    def autonomousInit(self) -> None:
        self.mLF.setIdleMode(rev.CANSparkMax.IdleMode.kBrake)
        self.mLB.setIdleMode(rev.CANSparkMax.IdleMode.kBrake)
        self.mRF.setIdleMode(rev.CANSparkMax.IdleMode.kBrake)
        self.mRB.setIdleMode(rev.CANSparkMax.IdleMode.kBrake)

    def autonomousPeriodic(self) -> None:
        speed = self.mAutoBalance.scoreAndBalance()
        self.setDrive(speed, speed)

    def teleopInit(self) -> None:
        pass

    def teleopPeriodic(self) -> None:
        pass

    def setDrive(self, left: float, right: float):
        self.mLF.set(left)
        self.mLB.set(left)
        self.mRF.set(right)
        self.mRB.set(right)


if __name__ == "__main__":
    wpilib.run(MyRobot)
