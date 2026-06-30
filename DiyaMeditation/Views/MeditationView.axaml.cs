using System;
using Avalonia.Controls;
using Avalonia.Media;
using Avalonia.Threading;
using DiyaMeditation.Models;
using DiyaMeditation.Services;
using DiyaMeditation.Services.Hardware;

namespace DiyaMeditation.Views;

public partial class MeditationView : UserControl
{
    private readonly IKioskNavigator _nav;
    private readonly SessionContext _ctx;
    private readonly ISensorSource _sensor = new MockSensorSource();

    private DispatcherTimer? _timer;
    private DateTime _start;
    private int _total;
    private double _sumCalm, _sumFocus, _sumHr;
    private int _samples;
    private int _lastSecond = -1;
    private bool _done;

    public MeditationView(IKioskNavigator nav, SessionContext ctx)
    {
        _nav = nav;
        _ctx = ctx;
        InitializeComponent();
        Loaded += (_, _) => Begin();
        Unloaded += (_, _) => Cleanup();
    }

    private void Begin()
    {
        _total = GetDurationSeconds();
        _sensor.Start();
        _start = DateTime.Now;
        _timer = new DispatcherTimer { Interval = TimeSpan.FromMilliseconds(100) };
        _timer.Tick += (_, _) => Tick();
        _timer.Start();
        Tick();
    }

    private static int GetDurationSeconds()
    {
        var env = Environment.GetEnvironmentVariable("DIYA_MEDITATION_SECONDS");
        if (int.TryParse(env, out var s) && s > 0) return s;
        return 60;
    }

    private void Tick()
    {
        var elapsed = (DateTime.Now - _start).TotalSeconds;
        var remaining = Math.Max(0, _total - elapsed);
        TimeText.Text = $"{Math.Ceiling(remaining):0}s remaining";

        // 8-second breathing cycle, smooth ease in/out.
        var phase = (elapsed % 8.0) / 8.0;
        var scale = 0.7 + 0.45 * (0.5 - 0.5 * Math.Cos(2 * Math.PI * phase));
        BreathCircle.RenderTransform = new ScaleTransform(scale, scale);
        BreathGlow.RenderTransform = new ScaleTransform(scale * 1.15, scale * 1.15);
        BreathText.Text = (elapsed % 8.0) < 4.0 ? "Breathe in…" : "Breathe out…";

        var sec = (int)elapsed;
        if (sec != _lastSecond)
        {
            _lastSecond = sec;
            var s = _sensor.Read();
            _sumCalm += s.Calmness;
            _sumFocus += s.Focus;
            _sumHr += s.HeartRate;
            _samples++;
        }

        if (elapsed >= _total && !_done)
        {
            _done = true;
            Finish();
        }
    }

    private void Finish()
    {
        Cleanup();
        var n = Math.Max(1, _samples);
        var calm = _sumCalm / n;
        var focus = _sumFocus / n;
        _ctx.Metrics = new MeditationMetrics
        {
            DurationSeconds = _total,
            AvgCalmness = Math.Round(calm, 0),
            AvgFocus = Math.Round(focus, 0),
            AvgHeartRate = (int)Math.Round(_sumHr / n),
            Score = (int)Math.Round(calm * 0.5 + focus * 0.5),
        };
        _nav.GoToReport(_ctx);
    }

    private void Cleanup()
    {
        _timer?.Stop();
        _timer = null;
        _sensor.Stop();
    }
}
