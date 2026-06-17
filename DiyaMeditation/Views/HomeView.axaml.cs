using Avalonia.Controls;
using Avalonia.Input;
using Avalonia.Interactivity;
using Avalonia.Media;
using DiyaMeditation.Models;

namespace DiyaMeditation.Views;

public partial class HomeView : UserControl
{
    private VisitorData? _visitor;

    public HomeView()
    {
        InitializeComponent();
        Loaded += (_, _) => QrBox.Focus();
    }

    private void OnQrKeyDown(object? sender, KeyEventArgs e)
    {
        if (e.Key != Key.Enter && e.Key != Key.Return)
            return;

        e.Handled = true;

        if (VisitorQr.TryParse(QrBox.Text, out var v) && v is not null)
        {
            _visitor = v;
            NameText.Text = v.Name;
            EmailText.Text = string.IsNullOrWhiteSpace(v.Email) ? "" : $"Email: {v.Email}";
            AgeText.Text = v.Age > 0 ? $"Age: {v.Age}" : "";
            DetailsPanel.IsVisible = true;
            NameBox.Text = v.Name;

            StatusText.Foreground = Brush.Parse("#16A34A");
            StatusText.Text = "Pass scanned successfully.";
        }
        else
        {
            StatusText.Foreground = Brushes.IndianRed;
            StatusText.Text = "Unrecognized code. Try again or enter your name.";
        }

        QrBox.Text = "";
    }

    private void OnStartCalibration(object? sender, RoutedEventArgs e)
    {
        var name = _visitor?.Name;
        if (string.IsNullOrWhiteSpace(name))
            name = NameBox.Text?.Trim();

        if (string.IsNullOrWhiteSpace(name))
        {
            StatusText.Foreground = Brushes.IndianRed;
            StatusText.Text = "Please scan your pass or enter your name.";
            QrBox.Focus();
            return;
        }

        StatusText.Foreground = Brush.Parse("#16A34A");
        StatusText.Text = $"Starting calibration for {name}...";
    }
}
