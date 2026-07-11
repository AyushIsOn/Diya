using System;
using Avalonia;
using Avalonia.Controls;
using Avalonia.Controls.ApplicationLifetimes;
using Avalonia.Input;
using Avalonia.Interactivity;
using Avalonia.Threading;

namespace DiyaMeditation.Views;

public partial class MainWindow : Window
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
    }

    protected override void OnOpened(EventArgs e)
    {
        base.OnOpened(e);
        Console.WriteLine("[Diya] v1.5.0 OnOpened — applying fullscreen");
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
