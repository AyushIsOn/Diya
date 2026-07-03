using System;

namespace DiyaMeditation.Models;

/// <summary>
/// Carried through the whole visit (Home -> Calibration -> Meditation -> Report)
/// and discarded when the kiosk returns to Idle.
/// </summary>
public sealed class SessionContext
{
    public VisitorData Visitor { get; }
    public DateTime StartedAt { get; } = DateTime.Now;

    public bool CalibrationOk { get; set; }
    public string CalibrationLog { get; set; } = "";

    public MeditationMetrics? Metrics { get; set; }

    public SessionContext(VisitorData visitor) => Visitor = visitor;
}
