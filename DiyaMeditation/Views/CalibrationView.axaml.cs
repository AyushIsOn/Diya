using System.Text;
using System.Threading.Tasks;
using Avalonia.Controls;
using Avalonia.Interactivity;
using Avalonia.Media;
using Avalonia.Threading;
using DiyaMeditation.Models;
using DiyaMeditation.Services;

namespace DiyaMeditation.Views;

public partial class CalibrationView : UserControl
{
    private readonly IKioskNavigator _nav;
    private readonly SessionContext _ctx;
    private readonly StringBuilder _log = new();
    private bool _advanced;
    private bool _active = true;
    private bool _running;

    public CalibrationView(IKioskNavigator nav, SessionContext ctx)
    {
        _nav = nav;
        _ctx = ctx;
        InitializeComponent();
        Unloaded += (_, _) => _active = false;
        Loaded += async (_, _) => await RunAsync();
    }

    private async Task RunAsync()
    {
        if (_running) return;
        _running = true;
        try
        {
            ContinueButton.IsVisible = false;
            RetryButton.IsVisible = false;
            BackButton.IsVisible = false;
            CalibProgress.IsVisible = true;
            StatusText.Foreground = Brush.Parse("#6B7280");
            StatusText.Text = "Preparing your session… please make yourself comfortable.";
            AppendLine("[calibration] starting…");

            var result = await CalibrationRunner.RunAsync(
                line => Dispatcher.UIThread.Post(() => AppendLine(line)));

            if (!_active) return;

            _ctx.CalibrationOk = result.Started;
            _ctx.CalibrationLog = result.Output;
            CalibProgress.IsVisible = false;

            if (result.Started)
            {
                StatusText.Foreground = Brush.Parse("#16A34A");
                StatusText.Text = "All set. Let's begin.";
                ContinueButton.IsVisible = true;
                await Task.Delay(1500);
                Advance();
            }
            else
            {
                StatusText.Foreground = Brushes.IndianRed;
                StatusText.Text = string.IsNullOrWhiteSpace(result.Error)
                    ? "We couldn't get set up. Please try again or ask a staff member."
                    : $"We couldn't get set up: {result.Error}";
                if (!string.IsNullOrWhiteSpace(result.Error)) AppendLine(result.Error!);
                DetailsExpander.IsExpanded = true;
                RetryButton.IsVisible = true;
                BackButton.IsVisible = true;
            }
        }
        finally
        {
            _running = false;
        }
    }

    private void AppendLine(string line)
    {
        _log.AppendLine(line);
        LogBox.Text = _log.ToString();
        LogBox.CaretIndex = LogBox.Text.Length;
    }

    private void Advance()
    {
        if (_advanced || !_active) return;
        _advanced = true;
        _nav.GoToMeditation(_ctx);
    }

    private void OnContinue(object? sender, RoutedEventArgs e) => Advance();
    private async void OnRetry(object? sender, RoutedEventArgs e) => await RunAsync();
    private void OnBack(object? sender, RoutedEventArgs e) => _nav.GoToHome();
}
