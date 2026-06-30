using Avalonia.Controls;
using Avalonia.Input;
using Avalonia.Interactivity;
using Avalonia.Media;
using DiyaMeditation.Models;

namespace DiyaMeditation.Views;

public partial class HomeView : UserControl
{
    private readonly PeopleDirectory _directory;
    private VisitorData? _visitor;

    public HomeView()
    {
        InitializeComponent();

        _directory = PeopleDirectory.Load();

        Loaded += (_, _) =>
        {
            ScanBox.Focus();
            ShowDirectoryStatus();
        };
    }

    private void ShowDirectoryStatus()
    {
        if (_directory.Error is not null)
        {
            DirectoryStatus.Foreground = Brushes.IndianRed;
            DirectoryStatus.Text = $"People list problem: {_directory.Error}";
        }
        else
        {
            DirectoryStatus.Foreground = Brush.Parse("#9CA3AF");
            var file = _directory.SourcePath ?? "(unknown)";
            DirectoryStatus.Text = $"Loaded {_directory.People.Count} people from {file}";
        }
    }

    private void OnScanKeyDown(object? sender, KeyEventArgs e)
    {
        if (e.Key != Key.Enter && e.Key != Key.Return)
            return;
        e.Handled = true;

        var code = ScanBox.Text?.Trim();
        ScanBox.Text = "";

        if (string.IsNullOrWhiteSpace(code))
            return;

        var match = _directory.FindById(code);
        if (match is not null)
        {
            ApplyVisitor(match);
        }
        else
        {
            ShowError($"Pass \"{code}\" not found in the list. Try again or search your name.");
        }
        ScanBox.Focus();
    }

    private void OnNameSearchKeyDown(object? sender, KeyEventArgs e)
    {
        if (e.Key != Key.Enter && e.Key != Key.Return)
            return;
        e.Handled = true;

        var query = NameBox.Text?.Trim();
        if (string.IsNullOrWhiteSpace(query))
            return;

        var matches = _directory.SearchByName(query);
        if (matches.Count == 1)
        {
            ApplyVisitor(matches[0]);
        }
        else if (matches.Count == 0)
        {
            ShowError($"No one named \"{query}\" in the list. Check the spelling or scan your pass.");
        }
        else
        {
            ShowError($"{matches.Count} people match \"{query}\". Type your full name, or scan your pass.");
        }
    }

    private void ApplyVisitor(VisitorData v)
    {
        _visitor = v;
        NameText.Text = v.Name;
        EmailText.Text = string.IsNullOrWhiteSpace(v.Email) ? "" : $"Email: {v.Email}";
        AgeText.Text = v.Age > 0 ? $"Age: {v.Age}" : "";
        IdText.Text = string.IsNullOrWhiteSpace(v.Id) ? "" : $"Pass: {v.Id}";
        DetailsPanel.IsVisible = true;
        NameBox.Text = v.Name;

        StatusText.Foreground = Brush.Parse("#16A34A");
        StatusText.Text = $"Found {v.Name}.";
    }

    private void ShowError(string message)
    {
        _visitor = null;
        DetailsPanel.IsVisible = false;
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
            StatusText.Text = "Scan your pass or find your name first.";
            ScanBox.Focus();
            return;
        }

        StatusText.Foreground = Brush.Parse("#16A34A");
        StatusText.Text = $"Starting calibration for {name}…";
    }
}
