using System;
using System.Diagnostics;
using System.IO;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace DiyaMeditation.Services;

public sealed record PipelineResult(bool Completed, int ExitCode, string Output, string? Error);

/// <summary>
/// Runs the bundled pipeline script (scripts/run1.sh) with bash and WAITS for it
/// to finish. run1.sh drives the camera/CV scripts and then launches the external
/// (headless) meditation-app, which writes the report PDF. Only once the script
/// exits do we look for the resulting PDF.
///
/// There is intentionally NO timeout: run1.sh owns its own retry logic and blocks
/// until the pipeline is done.
///
/// Configurable via env vars:
///   DIYA_PIPELINE_SCRIPT - full path to the script (default: &lt;app&gt;/scripts/run1.sh)
///   DIYA_BASH            - bash executable (default: bash)
/// </summary>
public static class PipelineRunner
{
    private static string BashExe =>
        Environment.GetEnvironmentVariable("DIYA_BASH") is { Length: > 0 } b ? b : "bash";

    public static string ScriptPath()
    {
        var custom = Environment.GetEnvironmentVariable("DIYA_PIPELINE_SCRIPT");
        if (!string.IsNullOrWhiteSpace(custom))
            return custom;
        return Path.Combine(AppContext.BaseDirectory, "scripts", "run1.sh");
    }

    public static async Task<PipelineResult> RunAsync(Action<string>? onOutput = null, CancellationToken ct = default)
    {
        var script = ScriptPath();
        if (!File.Exists(script))
            return new PipelineResult(false, -1, "", $"Pipeline script not found at {script}");

        var psi = new ProcessStartInfo
        {
            FileName = BashExe,
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
            Console.WriteLine($"[pipeline] {data}");
            // Surface each line so the UI can show a live status while running.
            onOutput?.Invoke(data);
        }

        try
        {
            using var proc = new Process { StartInfo = psi };
            proc.OutputDataReceived += (_, e) => Capture(e.Data);
            proc.ErrorDataReceived += (_, e) => Capture(e.Data);

            if (!proc.Start())
                return new PipelineResult(false, -1, "", "Failed to start the pipeline process.");

            proc.BeginOutputReadLine();
            proc.BeginErrorReadLine();

            // Wait for the whole pipeline (incl. meditation-app) to finish.
            await proc.WaitForExitAsync(ct);

            string text;
            lock (output) text = output.ToString().Trim();
            return new PipelineResult(true, proc.ExitCode, text, null);
        }
        catch (Exception ex)
        {
            // bash missing, permission denied, cancelled, etc.
            return new PipelineResult(false, -1, "", ex.Message);
        }
    }
}
