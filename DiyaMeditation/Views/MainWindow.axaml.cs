using System;
using Avalonia.Controls;
using Avalonia.Threading;

namespace DiyaMeditation.Views;

public partial class MainWindow : Window
{
    public MainWindow()
    {
        InitializeComponent();
    }

    protected override void OnOpened(EventArgs e)
    {
        base.OnOpened(e);
        Console.WriteLine("[Diya] v1.6.0 OnOpened — applying fullscreen");
        GoFullScreen();

        // Wayland/GNOME maps the window in a normal state first, so re-assert
        // fullscreen a few times right after opening. This only runs at startup —
        // it no longer fights the user afterwards, so the window can be minimised
        // or closed normally.
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
        if (WindowState != WindowState.FullScreen)
            WindowState = WindowState.FullScreen;
        Console.WriteLine($"[Diya] fullscreen check -> WindowState={WindowState}, ClientSize={ClientSize}");
    }
}
