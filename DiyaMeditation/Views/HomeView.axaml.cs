using Avalonia.Controls;
using Avalonia.Interactivity;

namespace DiyaMeditation.Views;

public partial class HomeView : UserControl
{
    public HomeView()
    {
        InitializeComponent();
    }

    private void OnStartCalibration(object? sender, RoutedEventArgs e)
    {
        var name = NameBox.Text?.Trim();

        if (string.IsNullOrWhiteSpace(name))
        {
            StatusText.Foreground = Avalonia.Media.Brushes.Salmon;
            StatusText.Text = "Please enter your name before starting.";
            NameBox.Focus();
            return;
        }

        // Calibration flow is not built yet — this is the hook point for the next step.
        StatusText.Foreground = Avalonia.Media.Brush.Parse("#9C8FC7");
        StatusText.Text = $"Thanks, {name}! Calibration will begin here in the next step.";
    }
}
