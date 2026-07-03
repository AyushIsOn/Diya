using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using DiyaMeditation.Models;
using QuestPDF.Fluent;

namespace DiyaMeditation.Services;

/// <summary>
/// Saves session report PDFs to disk.
///
/// Target folder (first writable one wins):
///   1. DIYA_DATA_DIR env var
///   2. /opt/meditation-app/data       (created writable by the .deb postinst)
///   3. ~/.local/share/diya-meditation/data
///   4. a temp folder
/// </summary>
public static class ReportStore
{
    public static string ResolveDataDir()
    {
        var candidates = new List<string>();

        var env = Environment.GetEnvironmentVariable("DIYA_DATA_DIR");
        if (!string.IsNullOrWhiteSpace(env)) candidates.Add(env);

        candidates.Add("/opt/meditation-app/data");

        var home = Environment.GetFolderPath(Environment.SpecialFolder.UserProfile);
        if (!string.IsNullOrWhiteSpace(home))
            candidates.Add(Path.Combine(home, ".local", "share", "diya-meditation", "data"));

        candidates.Add(Path.Combine(Path.GetTempPath(), "diya-meditation-data"));

        foreach (var dir in candidates)
            if (TryEnsureWritable(dir))
                return dir;

        return candidates[^1];
    }

    private static bool TryEnsureWritable(string dir)
    {
        try
        {
            Directory.CreateDirectory(dir);
            var probe = Path.Combine(dir, ".write-test");
            File.WriteAllText(probe, "ok");
            File.Delete(probe);
            return true;
        }
        catch
        {
            return false;
        }
    }

    /// <summary>Generates the report PDF and returns the full path it was written to.</summary>
    public static string Save(SessionContext ctx)
    {
        var dir = ResolveDataDir();
        var fileName = $"{DateTime.Now:yyyyMMdd_HHmmss}_{Sanitize(ctx.Visitor.Name)}.pdf";
        var path = Path.Combine(dir, fileName);
        ReportPdf.Build(ctx).GeneratePdf(path);
        return path;
    }

    private static string Sanitize(string? name)
    {
        if (string.IsNullOrWhiteSpace(name)) return "visitor";
        var cleaned = new string(name.Trim().Select(c => char.IsLetterOrDigit(c) ? c : '_').ToArray());
        return cleaned.Length > 40 ? cleaned[..40] : cleaned;
    }
}
