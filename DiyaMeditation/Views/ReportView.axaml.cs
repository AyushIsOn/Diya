using System;
using Avalonia.Controls;
using Avalonia.Interactivity;
using Avalonia.Threading;
using DiyaMeditation.Models;
using DiyaMeditation.Services;

namespace DiyaMeditation.Views;

public partial class ReportView : UserControl
{
    private readonly IKioskNavigator _nav;
    private readonly SessionContext _ctx;
    private DispatcherTimer? _autoReturn;
    private int _secondsLeft = 30;
    private bool _left;

    public ReportView(IKioskNavigator nav, SessionContext ctx)
    {
        _nav = nav;
        _ctx = ctx;
        InitializeComponent();
        Populate();
        Loaded += (_, _) => StartAutoReturn();
        Unloaded += (_, _) => _autoReturn?.Stop();
    }

    private void Populate()
    {
        var name = _ctx.Visitor.Name;
        TitleText.Text = string.IsNullOrWhiteSpace(name) ? "Your session" : $"Well done, {name}";

        var m = _ctx.Metrics;
        if (m is null)
        {
            ScoreText.Text = "—";
            MessageText.Text = "Session complete.";
            return;
        }

        ScoreText.Text = m.Score.ToString();
        CalmText.Text = $"{m.AvgCalmness:0}%";
        FocusText.Text = $"{m.AvgFocus:0}%";
        HrText.Text = m.AvgHeartRate.ToString();
        DurationText.Text = $"Session length: {m.DurationSeconds}s";
        MessageText.Text = MeditationMetrics.Message(m.Score);
    }

    private void StartAutoReturn()
    {
        UpdateAutoText();
        _autoReturn = new DispatcherTimer { Interval = TimeSpan.FromSeconds(1) };
        _autoReturn.Tick += (_, _) =>
        {
            _secondsLeft--;
            if (_secondsLeft <= 0) Leave();
            else UpdateAutoText();
        };
        _autoReturn.Start();
    }

    private void UpdateAutoText() => AutoText.Text = $"Returning to the start in {_secondsLeft}s…";

    private void OnDone(object? sender, RoutedEventArgs e) => Leave();

    private void Leave()
    {
        if (_left) return;
        _left = true;
        _autoReturn?.Stop();
        _nav.GoToHome();
    }
}
