using Avalonia.Controls;
using Avalonia.Interactivity;

namespace DiyaMeditation.Views;

public partial class HomeView : UserControl
{
    public HomeView() => InitializeComponent();

    private void OnStartCalibration(object? sender, RoutedEventArgs e)
    {
        var name = NameBox.Text?.Trim();
        if (string.IsNullOrWhiteSpace(name))
        {
            NameBox.Focus();
            return;
        }

        // TODO: advance to the calibration screen using `name`.
    }
}
