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
            StatusText.Foreground = Brush.Parse("#6B7280");
            StatusText.Text = "Calibrating… please hold still.";
            AppendLine("[calibration] starting…");

            var result = await CalibrationRunner.RunAsync(
                line => Dispatcher.UIThread.Post(() => AppendLine(line)));

            if (!_active) return;

            _ctx.CalibrationOk = result.Started;
            _ctx.CalibrationLog = result.Output;

            if (result.Started)
            {
                StatusText.Foreground = Brush.Parse("#16A34A");
                StatusText.Text = "Calibration complete.";
                ContinueButton.IsVisible = true;
                await Task.Delay(1800);
                Advance();
            }
            else
            {
                StatusText.Foreground = Brushes.IndianRed;
                StatusText.Text = string.IsNullOrWhiteSpace(result.Error)
                    ? "Calibration produced no output."
                    : $"Calibration could not start: {result.Error}";
                if (!string.IsNullOrWhiteSpace(result.Error)) AppendLine(result.Error!);
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
