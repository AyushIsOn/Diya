using System;
using System.Diagnostics;
using System.IO;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace DiyaMeditation.Services;

public sealed record CalibrationResult(bool Started, string Output, string? Error);

/// <summary>
/// Runs the calibration script (calibration/start_calibration.py) and reports
/// whether it produced any output. The kiosk treats "any output" as
/// "calibration started".
///
/// Configurable via env vars:
///   DIYA_PYTHON             - python executable (default: python3)
///   DIYA_CALIBRATION_SCRIPT - full path to the script (default: &lt;app&gt;/calibration/start_calibration.py)
/// </summary>
public static class CalibrationRunner
{
    private static string PythonExe =>
        Environment.GetEnvironmentVariable("DIYA_PYTHON") is { Length: > 0 } p ? p : "python3";

    private static string ScriptPath()
    {
        var custom = Environment.GetEnvironmentVariable("DIYA_CALIBRATION_SCRIPT");
        if (!string.IsNullOrWhiteSpace(custom))
            return custom;
        return Path.Combine(AppContext.BaseDirectory, "calibration", "start_calibration.py");
    }

    public static async Task<CalibrationResult> RunAsync(CancellationToken ct = default)
    {
        var script = ScriptPath();
        if (!File.Exists(script))
            return new CalibrationResult(false, "", $"Calibration script not found at {script}");

        var psi = new ProcessStartInfo
        {
            FileName = PythonExe,
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            UseShellExecute = false,
            CreateNoWindow = true,
            WorkingDirectory = Path.GetDirectoryName(script) ?? AppContext.BaseDirectory,
        };
        psi.ArgumentList.Add(script);

        var output = new StringBuilder();
        void Capture(string? data)
        {
            if (data is null) return;
            lock (output) output.AppendLine(data);
            Console.WriteLine($"[calib] {data}");
        }

        try
        {
            using var proc = new Process { StartInfo = psi };
            proc.OutputDataReceived += (_, e) => Capture(e.Data);
            proc.ErrorDataReceived += (_, e) => Capture(e.Data);

            if (!proc.Start())
                return new CalibrationResult(false, "", "Failed to start the calibration process.");

            proc.BeginOutputReadLine();
            proc.BeginErrorReadLine();

            // Wait for completion, but cap it so the UI never hangs.
            using var cts = CancellationTokenSource.CreateLinkedTokenSource(ct);
            cts.CancelAfter(TimeSpan.FromSeconds(20));
            try
            {
                await proc.WaitForExitAsync(cts.Token);
            }
            catch (OperationCanceledException)
            {
                // Long-running (e.g. future streaming hardware): we already have output.
            }

            string text;
            lock (output) text = output.ToString().Trim();
            return new CalibrationResult(text.Length > 0, text, null);
        }
        catch (Exception ex)
        {
            // python3 not installed, permission denied, etc.
            return new CalibrationResult(false, "", ex.Message);
        }
    }
}
