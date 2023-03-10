
/**********************************************************
 * EXAMPLE IMPLEMENTATION WITH SPARKMAX MOTOR CONTROLLERS *
 **********************************************************/

#include "Robot.h"

#include <frc2/command/CommandScheduler.h>

void Robot::RobotInit() {}

void Robot::RobotPeriodic() {
  frc2::CommandScheduler::GetInstance().Run();
}

void Robot::DisabledInit() {
  mLB.SetIdleMode(rev::CANSparkMax::IdleMode::kCoast);
  mLF.SetIdleMode(rev::CANSparkMax::IdleMode::kCoast);
  mRB.SetIdleMode(rev::CANSparkMax::IdleMode::kCoast);
  mRF.SetIdleMode(rev::CANSparkMax::IdleMode::kCoast);
}

void Robot::DisabledPeriodic() {}

void Robot::AutonomousInit() {
  mLB.SetIdleMode(rev::CANSparkMax::IdleMode::kBrake);
  mLF.SetIdleMode(rev::CANSparkMax::IdleMode::kBrake);
  mRB.SetIdleMode(rev::CANSparkMax::IdleMode::kBrake);
  mRF.SetIdleMode(rev::CANSparkMax::IdleMode::kBrake);
}

  /***********************************************************************************
   * To implement the auto balance auto, just run the command in autonomous periodic *
   * and set your left and right motor speeds to the output like this                *
   ***********************************************************************************/
void Robot::AutonomousPeriodic() {
  double speed = mAutoBalance.scoreAndBalance();
  
  setDrive(speed, speed);
}

void Robot::TeleopInit() {}

void Robot::TeleopPeriodic() {}

void Robot::TestPeriodic() {}

void Robot::SimulationInit() {}

void Robot::SimulationPeriodic() {}

void Robot::setDrive(double left, double right){
  mLF.Set(left);
  mLB.Set(left);
  mRF.Set(right);
  mRB.Set(right);
}

#ifndef RUNNING_FRC_TESTS
int main() {
  return frc::StartRobot<Robot>();
}
#endif
