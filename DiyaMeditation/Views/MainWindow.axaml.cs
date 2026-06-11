using Avalonia.Controls;
using Avalonia.Controls.ApplicationLifetimes;
using Avalonia.Input;
using Avalonia.Interactivity;

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
