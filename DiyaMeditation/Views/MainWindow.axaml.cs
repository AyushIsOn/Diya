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
    // Secret exit combination. Chosen to avoid clashing with Ubuntu/GNOME defaults:
    //   Ctrl + Shift + Alt + Q
    private const Key ExitKey = Key.Q;
    private const KeyModifiers ExitModifiers =
        KeyModifiers.Control | KeyModifiers.Shift | KeyModifiers.Alt;

    // Only an explicit secret exit is allowed to actually close the window.
    private bool _allowClose;

    public MainWindow()
    {
        InitializeComponent();

        // Block every "normal" way of closing the window. The OS/user cannot close it;
        // only the secret shortcut flips _allowClose to true.
        Closing += OnClosing;

        // Listen for the secret exit shortcut at the window level (tunnel so it fires
        // even if a child control, e.g. the name field, currently has focus).
        AddHandler(KeyDownEvent, OnGlobalKeyDown, RoutingStrategies.Tunnel);
    }

    protected override void OnOpened(EventArgs e)
    {
        base.OnOpened(e);
        Console.WriteLine("[Diya] v1.0.2 OnOpened — applying fullscreen");
        // Apply fullscreen here (not in XAML): doing it after the window is shown is
        // reliable across Linux and macOS, where XAML-time fullscreen often doesn't stick.
        GoFullScreen();

        // Some Linux compositors (GNOME/Wayland/XWayland) map the window in a normal
        // state first and only honor the fullscreen request a moment later. Re-assert
        // it a few times shortly after opening so it reliably lands fullscreen.
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

        // Keep the kiosk locked in fullscreen: if anything minimizes/restores the
        // window, snap it straight back (unless we're intentionally exiting).
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
            // Veto the close request — users and the OS cannot dismiss the kiosk.
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

        // Shut the whole application down cleanly (we use OnExplicitShutdown mode).
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
