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

    private async void OnQrKeyDown(object? sender, KeyEventArgs e)
    {
        if (e.Key != Key.Enter && e.Key != Key.Return)
            return;

        e.Handled = true;

        var raw = QrBox.Text;
        QrBox.Text = "";

        // Backward-compat / offline testing: a QR (or pasted text) that contains
        // the full visitor JSON embedded as DIYA1:<base64> or raw {json}.
        if (VisitorQr.TryParse(raw, out var embedded) && embedded is not null)
        {
            ApplyVisitor(embedded);
            return;
        }

        // Normal path: the QR holds only the id -> look the visitor up via the API.
        var id = VisitorQr.ExtractId(raw);
        if (id is null)
        {
            ShowError("Unrecognized code. Try again or enter your name.");
            return;
        }

        StatusText.Foreground = Brush.Parse("#6B7280");
        StatusText.Text = "Looking up your pass...";

        var result = await VisitorApiClient.FetchAsync(id);
        switch (result.Status)
        {
            case FetchStatus.Found:
                ApplyVisitor(result.Visitor!);
                break;
            case FetchStatus.NotFound:
                ShowError("Pass not recognized. Try again or enter your name.");
                break;
            default:
                ShowError("Couldn't reach the server. Check the connection and try again.");
                break;
        }
    }

    private void ApplyVisitor(VisitorData v)
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

    private void ShowError(string message)
    {
        StatusText.Foreground = Brushes.IndianRed;
        StatusText.Text = message;
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
