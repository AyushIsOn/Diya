using System;

namespace DiyaMeditation.Models;

/// <summary>Results computed from the meditation session (from the sensor stream).</summary>
public sealed class MeditationMetrics
{
    public int DurationSeconds { get; set; }
    public double AvgCalmness { get; set; }   // 0..100
    public double AvgFocus { get; set; }      // 0..100
    public int AvgHeartRate { get; set; }     // bpm
    public int Score { get; set; }            // 0..100

    /// <summary>
    /// Build metrics from accumulated sensor totals. Safe against zero samples and
    /// clamps everything to sane ranges.
    /// </summary>
    public static MeditationMetrics From(double sumCalmness, double sumFocus, double sumHeartRate,
                                         int samples, int durationSeconds)
    {
        var n = Math.Max(1, samples);
        var calm = Math.Clamp(sumCalmness / n, 0, 100);
        var focus = Math.Clamp(sumFocus / n, 0, 100);
        var hr = (int)Math.Round(sumHeartRate / n);

        return new MeditationMetrics
        {
            DurationSeconds = Math.Max(0, durationSeconds),
            AvgCalmness = Math.Round(calm, 0),
            AvgFocus = Math.Round(focus, 0),
            AvgHeartRate = hr,
            Score = (int)Math.Round(Math.Clamp(calm * 0.5 + focus * 0.5, 0, 100)),
        };
    }

    /// <summary>Friendly takeaway message for a given score.</summary>
    public static string Message(int score) => score switch
    {
        >= 80 => "Beautifully calm and focused — a deeply settled session.",
        >= 60 => "A calm, steady session — nicely done.",
        >= 40 => "A good start. With practice it gets easier to settle.",
        _ => "Thanks for taking a moment for yourself today.",
    };
}
