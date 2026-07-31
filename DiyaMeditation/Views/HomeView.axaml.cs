using System;
using System.Collections.Generic;
using System.IO;
using System.Text.RegularExpressions;
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

    // Strips ANSI escape sequences (colour codes) that the pipeline scripts emit,
    // so the on-screen status line stays clean.
    private static readonly Regex AnsiRegex = new(@"\x1B\[[0-9;]*[A-Za-z]");

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
    /// Runs run1.sh (which drives the cameras/CV and the external meditation-app)
    /// and waits for it to finish — the meditation-app exits once its report PDF is
    /// written. The pipeline's own output is shown as a live status line. We then
    /// display the report produced by THIS session (a PDF newer than when we
    /// started), so a stale report from a previous visitor is never shown.
    /// Nothing about the external meditation-app is modified.
    /// </summary>
    private async Task StartPipelineAsync()
    {
        if (_pipelineRunning) return;
        _pipelineRunning = true;
        _pollTimer?.Stop();

        StatusText.Foreground = Brush.Parse("#6B7280");
        StatusText.Text = "Please wait — running your session…";
        LiveStatus.Foreground = Brush.Parse("#6B7280");
        LiveStatus.Text = "Starting your session…";

        var startUtc = DateTime.UtcNow;

        try
        {
            // The meditation-app prints its progress (e.g. "Running t3 (PDF report)…");
            // surface the latest line as a live status. This is visible during the
            // calibration phase, before the external app covers the screen.
            var result = await PipelineRunner.RunAsync(onOutput: line =>
                Dispatcher.UIThread.Post(() =>
                {
                    var t = AnsiRegex.Replace(line ?? "", "").Trim();
                    if (t.Length > 0)
                        LiveStatus.Text = t.Length > 140 ? t.Substring(0, 140) : t;
                }));

            // Only show a report produced by THIS session (newer than when we started),
            // so a previous visitor's PDF is never displayed by mistake.
            var pdf = ReportRenderer.FindNewestPdfSince(startUtc);

            if (pdf is not null)
            {
                LiveStatus.Text = "Preparing your report…";
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
                BorderBrush = Brush.Parse("#E5E7EB"),
                BorderThickness = new Thickness(1),
                CornerRadius = new CornerRadius(8),
                HorizontalAlignment = HorizontalAlignment.Center,
                Child = img,
            });
        }

        // Personalised thank-you, shown alongside the report.
        ReportTitle.Text = "Your Report";
        ReportThanks.Text = string.IsNullOrWhiteSpace(_visitor?.Name)
            ? "Thank you for meditating with us."
            : $"Thank you, {_visitor!.Name} — we hope you enjoyed your session.";
        ReportThanks.IsVisible = true;

        ReportMessage.IsVisible = false;
        ReportScroll.IsVisible = true;
        ReportOverlay.IsVisible = true;
    }

    private void ShowReportMessage(string message)
    {
        ReportPages.Children.Clear();
        ReportScroll.IsVisible = false;
        ReportTitle.Text = "Your Report";
        ReportThanks.IsVisible = false;
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
