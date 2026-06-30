using System;

namespace DiyaMeditation.Services.Hardware;

/// <summary>
/// Stand-in sensor source used until the real IITH hardware/CV is wired in.
/// Produces a smooth, plausible "settling down" curve: calmness and focus drift
/// up over the session while heart rate eases down, with light noise.
/// </summary>
public sealed class MockSensorSource : ISensorSource
{
    private readonly Random _rng = new();
    private double _calm = 45;
    private double _focus = 40;
    private double _hr = 80;
    private bool _running;

    public void Start()
    {
        _running = true;
        _calm = 45;
        _focus = 40;
        _hr = 80;
    }

    public void Stop() => _running = false;

    public SensorSample Read()
    {
        if (_running)
        {
            _calm = Clamp(_calm + (_rng.NextDouble() * 4.0 - 1.2), 0, 100);  // avg +0.8
            _focus = Clamp(_focus + (_rng.NextDouble() * 4.0 - 1.0), 0, 100); // avg +1.0
            _hr = Clamp(_hr + (_rng.NextDouble() * 3.0 - 1.8), 52, 95);       // avg -0.3
        }
        return new SensorSample(_calm, _focus, (int)Math.Round(_hr));
    }

    private static double Clamp(double v, double lo, double hi)
        => v < lo ? lo : (v > hi ? hi : v);
}
