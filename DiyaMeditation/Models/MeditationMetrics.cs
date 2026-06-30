namespace DiyaMeditation.Models;

/// <summary>Results computed from the meditation session (from the sensor stream).</summary>
public sealed class MeditationMetrics
{
    public int DurationSeconds { get; set; }
    public double AvgCalmness { get; set; }   // 0..100
    public double AvgFocus { get; set; }      // 0..100
    public int AvgHeartRate { get; set; }     // bpm
    public int Score { get; set; }            // 0..100
}
