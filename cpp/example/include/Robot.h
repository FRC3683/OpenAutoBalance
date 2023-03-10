// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

#pragma once

#include <optional>

#include <frc/TimedRobot.h>
#include <frc2/command/CommandPtr.h>
#include <rev/CANSparkMax.h>

#include "autoBalance.h"

class Robot : public frc::TimedRobot {
 public:
  void RobotInit() override;
  void RobotPeriodic() override;
  void DisabledInit() override;
  void DisabledPeriodic() override;
  void AutonomousInit() override;
  void AutonomousPeriodic() override;
  void TeleopInit() override;
  void TeleopPeriodic() override;
  void TestPeriodic() override;
  void SimulationInit() override;
  void SimulationPeriodic() override;
  rev::CANSparkMax mLF{2, rev::CANSparkMax::MotorType::kBrushless};
  rev::CANSparkMax mLB{3, rev::CANSparkMax::MotorType::kBrushless};
  rev::CANSparkMax mRF{4, rev::CANSparkMax::MotorType::kBrushless};
  rev::CANSparkMax mRB{5, rev::CANSparkMax::MotorType::kBrushless};


 private:
  void setDrive(double left, double right);
  autoBalance mAutoBalance;
};
