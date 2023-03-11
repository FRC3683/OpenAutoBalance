
#pragma once
#include <frc/BuiltInAccelerometer.h>
#include <cmath>

class autoBalance{
    public:
        autoBalance();
        double getPitch();
        double getRoll();
        double getTilt();
        double autoBalanceRoutine();
        double scoreAndBalance();
        int secondsToTicks(double time);
        
    private:
        frc::BuiltInAccelerometer mAccel{};
        int state;
        int debounceCount;
        double robotSpeedSlow;
        double robotSpeedFast;
        double onChargeStationDegree;
        double levelDegree;
        double debounceTime;
        double singleTapTime;
        double scoringBackUpTime;
        double doubleTapTime;
};