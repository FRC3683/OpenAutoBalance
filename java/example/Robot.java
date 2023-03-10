
/**********************************************************
 * EXAMPLE IMPLEMENTATION WITH SPARKMAX MOTOR CONTROLLERS *
 **********************************************************/

package frc.robot;

import com.revrobotics.CANSparkMax;
import com.revrobotics.CANSparkMax.IdleMode;
import com.revrobotics.CANSparkMaxLowLevel.MotorType;

import edu.wpi.first.wpilibj.TimedRobot;
import edu.wpi.first.wpilibj2.command.Command;
import edu.wpi.first.wpilibj2.command.CommandScheduler;

public class Robot extends TimedRobot {
  private Command m_autonomousCommand;

  private CANSparkMax mLF;
  private CANSparkMax mLB;
  private CANSparkMax mRF;
  private CANSparkMax mRB;
  private autoBalance mAutoBalance;

  @Override
  public void robotInit() {
    mLF = new CANSparkMax(2, MotorType.kBrushless);
    mLB = new CANSparkMax(3, MotorType.kBrushless);
    mRF = new CANSparkMax(4, MotorType.kBrushless);
    mRB = new CANSparkMax(5, MotorType.kBrushless);
    mAutoBalance = new autoBalance();
  }
  @Override
  public void robotPeriodic() {
    CommandScheduler.getInstance().run();
  }

  @Override
  public void disabledInit() {
    mLB.setIdleMode(IdleMode.kCoast);
    mLF.setIdleMode(IdleMode.kCoast);
    mRB.setIdleMode(IdleMode.kCoast);
    mRF.setIdleMode(IdleMode.kCoast);

  }

  @Override
  public void disabledPeriodic() {}

  @Override
  public void autonomousInit() {
    mLB.setIdleMode(IdleMode.kBrake);
    mLF.setIdleMode(IdleMode.kBrake);
    mRB.setIdleMode(IdleMode.kBrake);
    mRF.setIdleMode(IdleMode.kBrake);
    if (m_autonomousCommand != null) {
      m_autonomousCommand.schedule();
    }
  }

  /***********************************************************************************
   * To implement the auto balance auto, just run the command in autonomous periodic *
   * and set your left and right motor speeds to the output like this                *
   ***********************************************************************************/
  @Override
  public void autonomousPeriodic() {
    double speed = mAutoBalance.scoreAndBalance();
    setSpeed(speed, speed);
  }

  @Override
  public void teleopInit() {
    if (m_autonomousCommand != null) {
      m_autonomousCommand.cancel();
    }
  }

  @Override
  public void teleopPeriodic() {}

  @Override
  public void testInit() {
    CommandScheduler.getInstance().cancelAll();
  }

  @Override
  public void testPeriodic() {}

  @Override
  public void simulationInit() {}

  @Override
  public void simulationPeriodic() {}

  //helper function for setting motor controller speeds
  private void setSpeed(double left, double right){
    mLF.set(left);
    mLB.set(left);
    mRF.set(right);
    mRB.set(right);
  }
}
