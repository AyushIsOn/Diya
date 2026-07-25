using System;
using System.Collections.Generic;
using System.IO;
using System.Threading.Tasks;
using Avalonia;
using Avalonia.Controls;
using Avalonia.Interactivity;
using Avalonia.Layout;
using Avalonia.Media;
using Avalonia.Media.Imaging;
using Avalonia.Threading;
using DiyaMeditation.Models;
using DiyaMeditation.Services;
using QRCoder;

namespace DiyaMeditation.Views;

public partial class HomeView : UserControl
{
    private VisitorData? _visitor;
    private string? _sessionToken;
    private DispatcherTimer? _pollTimer;
    private bool _claimed;
    private bool _busy;
    private bool _pipelineRunning;

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

        // Optional roster photo. Downloaded in the background; a missing or broken
        // image simply leaves the avatar hidden and never blocks the flow.
        PhotoBorder.IsVisible = false;
        PhotoImage.Source = null;
        if (!string.IsNullOrWhiteSpace(v.ImageUrl))
            _ = LoadPhotoAsync(v.ImageUrl);

        LiveStatus.Foreground = Brush.Parse("#16A34A");
        LiveStatus.Text = $"Authenticated! Welcome, {v.Name}.";
        ScanHint.Text = "";

        // Successful authentication auto-starts the pipeline (no button press).
        _ = StartPipelineAsync();
    }

    private async void OnNewCode(object? sender, RoutedEventArgs e)
        => await StartNewSessionAsync();

    /// <summary>
    /// Manual fallback: if nobody scanned, build a visitor from the typed name and
    /// start the same pipeline.
    /// </summary>
    private async void OnStart(object? sender, RoutedEventArgs e)
    {
        if (_visitor is null)
        {
            var typedName = NameBox.Text?.Trim();
            if (string.IsNullOrWhiteSpace(typedName))
            {
                StatusText.Foreground = Brushes.IndianRed;
                StatusText.Text = "Scan the QR with your phone, or enter your name.";
                return;
            }

            _visitor = new VisitorData
            {
                Name = typedName,
                Email = EmailBox.Text?.Trim() ?? "",
                Age = int.TryParse(AgeBox.Text?.Trim(), out var a) && a > 0 ? a : 0,
            };
        }

        await StartPipelineAsync();
    }

    /// <summary>
    /// Runs run1.sh (which drives the cameras/CV and the headless meditation-app),
    /// waits for it to finish, then displays the newest report PDF in-app.
    /// </summary>
    private async Task StartPipelineAsync()
    {
        if (_pipelineRunning) return;
        _pipelineRunning = true;
        _pollTimer?.Stop();

        StatusText.Foreground = Brush.Parse("#6B7280");
        StatusText.Text = "Please wait — running your session…";
        LiveStatus.Foreground = Brush.Parse("#6B7280");
        LiveStatus.Text = "Session in progress…";

        // Note: we do NOT minimise the window here. On Wayland an app can minimise
        // itself but cannot un-minimise/raise itself, so it would appear to "close"
        // and never come back. Instead we stay put showing this "please wait" state;
        // the external meditation-app's own fullscreen windows cover us during the
        // session, and we are already here to show the report afterwards.
        try
        {
            var result = await PipelineRunner.RunAsync();

            var pdf = ReportRenderer.FindNewestPdf();
            if (pdf is not null)
            {
                try
                {
                    var pages = await ReportRenderer.RenderPagesAsync(pdf);
                    ShowReport(pages);
                }
                catch (Exception ex)
                {
                    ShowReportMessage($"A report was found but could not be displayed.\n{ex.Message}");
                }
            }
            else
            {
                ShowReportMessage(result.Completed
                    ? $"No report was found in {ReportRenderer.ReportDir}."
                    : $"The session could not start:\n{result.Error}");
            }
        }
        finally
        {
            _pipelineRunning = false;
        }
    }

    private void ShowReport(List<Bitmap> pages)
    {
        ReportPages.Children.Clear();

        if (pages.Count == 0)
        {
            ShowReportMessage("The report has no pages.");
            return;
        }

        foreach (var bmp in pages)
        {
            var img = new Image { Source = bmp, Stretch = Stretch.Uniform, MaxWidth = 900 };
            ReportPages.Children.Add(new Border
            {
                Background = Brushes.White,
                CornerRadius = new CornerRadius(4),
                HorizontalAlignment = HorizontalAlignment.Center,
                Child = img,
            });
        }

        ReportMessage.IsVisible = false;
        ReportScroll.IsVisible = true;
        ReportOverlay.IsVisible = true;
    }

    private void ShowReportMessage(string message)
    {
        ReportPages.Children.Clear();
        ReportScroll.IsVisible = false;
        ReportMessage.Text = message;
        ReportMessage.IsVisible = true;
        ReportOverlay.IsVisible = true;
    }

    /// <summary>Return button: reset everything for the next visitor.</summary>
    private async void OnReturn(object? sender, RoutedEventArgs e)
    {
        ReportOverlay.IsVisible = false;
        ReportPages.Children.Clear();
        await StartNewSessionAsync();
    }

    private async Task LoadPhotoAsync(string url)
    {
        var bytes = await VisitorApiClient.DownloadBytesAsync(url).ConfigureAwait(false);
        if (bytes is null || bytes.Length == 0)
            return;

        try
        {
            using var ms = new MemoryStream(bytes);
            var bmp = new Bitmap(ms);
            await Dispatcher.UIThread.InvokeAsync(() =>
            {
                // Ignore a late-arriving image if a new session started meanwhile.
                if (_claimed)
                {
                    PhotoImage.Source = bmp;
                    PhotoBorder.IsVisible = true;
                }
            });
        }
        catch
        {
            // Unsupported/corrupt image data — leave the avatar hidden.
        }
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
