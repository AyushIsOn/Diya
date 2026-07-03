namespace DiyaMeditation.Services.Hardware;

/// <summary>A single reading from the meditation sensors / CV pipeline.</summary>
public readonly record struct SensorSample(double Calmness, double Focus, int HeartRate);

/// <summary>
/// Source of live meditation metrics. The IITH CV/sensor integration implements
/// this; the app only depends on the interface. Pull model: the screen reads on a
/// timer.
/// </summary>
public interface ISensorSource
{
    void Start();
    SensorSample Read();
    void Stop();
}

/// <summary>Camera plug-in point (calibration + meditation). Implemented by IITH later.</summary>
public interface ICameraSource
{
    void Start();
    void Stop();
}

/// <summary>Servo/motor plug-in point (calibration). Implemented by IITH later.</summary>
public interface IMotorController
{
    void MoveTo(int position);
}
