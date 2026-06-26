using System;
using System.IO;
using System.Threading.Tasks;
using Avalonia.Controls;
using Avalonia.Interactivity;
using Avalonia.Media;
using Avalonia.Media.Imaging;
using Avalonia.Threading;
using DiyaMeditation.Models;
using QRCoder;

namespace DiyaMeditation.Views;

public partial class HomeView : UserControl
{
    private VisitorData? _visitor;
    private string? _sessionToken;
    private DispatcherTimer? _pollTimer;
    private bool _claimed;
    private bool _busy;

    public HomeView()
    {
        InitializeComponent();
        Loaded += async (_, _) => await StartNewSessionAsync();
        Unloaded += (_, _) => _pollTimer?.Stop();
    }

    /// <summary>Create a fresh session, show its QR, and start polling for a claim.</summary>
    private async Task StartNewSessionAsync()
    {
        if (_busy) return;
        _busy = true;
        try
        {
            _pollTimer?.Stop();
            _claimed = false;
            _visitor = null;

            DetailsPanel.IsVisible = false;
            QrImage.Source = null;
            QrPlaceholder.IsVisible = true;
            QrPlaceholder.Text = "Connecting…";
            ScanHint.Text = "Scan this code with your phone camera to register.";
            LiveStatus.Foreground = Brush.Parse("#9CA3AF");
            LiveStatus.Text = "Waking up the server…";
            StatusText.Text = "";

            string? token = null;
            for (var attempt = 0; attempt < 3 && token is null; attempt++)
                token = await VisitorApiClient.CreateSessionAsync();

            if (token is null)
            {
                QrPlaceholder.Text = "Offline";
                LiveStatus.Foreground = Brushes.IndianRed;
                LiveStatus.Text = "Couldn't reach the server. Tap \"New code\" to retry.";
                return;
            }

            _sessionToken = token;
            var url = $"{VisitorApiClient.BaseUrl}/?session={token}";

            try
            {
                QrImage.Source = RenderQr(url);
                QrPlaceholder.IsVisible = false;
            }
            catch
            {
                QrPlaceholder.IsVisible = true;
                QrPlaceholder.Text = "QR error";
            }

            LiveStatus.Foreground = Brush.Parse("#9CA3AF");
            LiveStatus.Text = "Waiting for you to register…";

            _pollTimer = new DispatcherTimer { Interval = TimeSpan.FromSeconds(2) };
            _pollTimer.Tick += async (_, _) => await PollAsync();
            _pollTimer.Start();
        }
        finally
        {
            _busy = false;
        }
    }

    private async Task PollAsync()
    {
        if (_sessionToken is null || _claimed)
            return;

        var result = await VisitorApiClient.GetSessionAsync(_sessionToken);

        if (result.State == SessionState.Claimed && result.Visitor is not null)
        {
            _claimed = true;
            _pollTimer?.Stop();
            ApplyVisitor(result.Visitor);
        }
        // pending / transient network errors: keep polling silently
    }

    private void ApplyVisitor(VisitorData v)
    {
        _visitor = v;
        NameText.Text = v.Name;
        EmailText.Text = string.IsNullOrWhiteSpace(v.Email) ? "" : $"Email: {v.Email}";
        AgeText.Text = v.Age > 0 ? $"Age: {v.Age}" : "";
        DetailsPanel.IsVisible = true;
        NameBox.Text = v.Name;

        LiveStatus.Foreground = Brush.Parse("#16A34A");
        LiveStatus.Text = $"Registered! Welcome, {v.Name}.";
        ScanHint.Text = "You're all set — press Start Calibration.";

        StatusText.Foreground = Brush.Parse("#16A34A");
        StatusText.Text = "Pass scanned successfully.";
    }

    private async void OnNewCode(object? sender, RoutedEventArgs e)
        => await StartNewSessionAsync();

    private void OnStartCalibration(object? sender, RoutedEventArgs e)
    {
        var name = _visitor?.Name;
        if (string.IsNullOrWhiteSpace(name))
            name = NameBox.Text?.Trim();

        if (string.IsNullOrWhiteSpace(name))
        {
            StatusText.Foreground = Brushes.IndianRed;
            StatusText.Text = "Scan the QR with your phone, or enter your name.";
            return;
        }

        StatusText.Foreground = Brush.Parse("#16A34A");
        StatusText.Text = $"Starting calibration for {name}…";
    }

    private static Bitmap RenderQr(string text)
    {
        using var generator = new QRCodeGenerator();
        using var data = generator.CreateQrCode(text, QRCodeGenerator.ECCLevel.M);
        var png = new PngByteQRCode(data).GetGraphic(10);
        using var ms = new MemoryStream(png);
        return new Bitmap(ms);
    }
}
