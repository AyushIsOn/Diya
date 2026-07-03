using System;
using Avalonia;
using Avalonia.Controls;
using Avalonia.Controls.ApplicationLifetimes;
using Avalonia.Input;
using Avalonia.Interactivity;
using Avalonia.Threading;
using DiyaMeditation.Models;
using DiyaMeditation.Services;

namespace DiyaMeditation.Views;

public partial class MainWindow : Window, IKioskNavigator
{
    private const Key ExitKey = Key.Q;
    private const KeyModifiers ExitModifiers =
        KeyModifiers.Control | KeyModifiers.Shift | KeyModifiers.Alt;

    private bool _allowClose;

    public MainWindow()
    {
        InitializeComponent();
        Closing += OnClosing;
        AddHandler(KeyDownEvent, OnGlobalKeyDown, RoutingStrategies.Tunnel);
        GoToHome();
    }

    // ---- IKioskNavigator: swap the hosted screen --------------------------

    public void GoToHome() => ContentHost.Content = new HomeView(this);
    public void GoToCalibration(SessionContext context) => ContentHost.Content = new CalibrationView(this, context);
    public void GoToMeditation(SessionContext context) => ContentHost.Content = new MeditationView(this, context);
    public void GoToReport(SessionContext context) => ContentHost.Content = new ReportView(this, context);

    protected override void OnOpened(EventArgs e)
    {
        base.OnOpened(e);
        Console.WriteLine("[Diya] v1.7.1 OnOpened — applying fullscreen");
        GoFullScreen();

        var attempts = 0;
        var timer = new DispatcherTimer { Interval = TimeSpan.FromMilliseconds(250) };
        timer.Tick += (_, _) =>
        {
            GoFullScreen();
            if (++attempts >= 6)
                timer.Stop();
        };
        timer.Start();
    }

    private void GoFullScreen()
    {
        if (_allowClose) return;
        if (WindowState != WindowState.FullScreen)
            WindowState = WindowState.FullScreen;
        Console.WriteLine($"[Diya] fullscreen check -> WindowState={WindowState}, ClientSize={ClientSize}");
    }

    protected override void OnPropertyChanged(AvaloniaPropertyChangedEventArgs change)
    {
        base.OnPropertyChanged(change);

        if (change.Property == WindowStateProperty
            && !_allowClose
            && WindowState != WindowState.FullScreen)
        {
            WindowState = WindowState.FullScreen;
        }
    }

    private void OnClosing(object? sender, WindowClosingEventArgs e)
    {
        if (!_allowClose)
        {
            e.Cancel = true;
        }
    }

    private void OnGlobalKeyDown(object? sender, KeyEventArgs e)
    {
        if (e.Key == ExitKey && e.KeyModifiers == ExitModifiers)
        {
            e.Handled = true;
            ExitKiosk();
        }
    }

    private void ExitKiosk()
    {
        _allowClose = true;

        if (Avalonia.Application.Current?.ApplicationLifetime
            is IClassicDesktopStyleApplicationLifetime desktop)
        {
            desktop.Shutdown();
        }
        else
        {
            Close();
        }
    }
}
