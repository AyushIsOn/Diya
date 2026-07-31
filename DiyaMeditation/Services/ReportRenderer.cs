using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using Avalonia.Media.Imaging;
using PDFtoImage;
using SkiaSharp;

namespace DiyaMeditation.Services;

/// <summary>
/// Locates and renders the meditation report PDF written by the external
/// meditation-app. The report directory defaults to /opt/meditation-app/data and
/// is overridable via DIYA_REPORT_DIR. Pages are rendered to Avalonia bitmaps so
/// the report can be shown inside the kiosk (no external viewer).
/// </summary>
public static class ReportRenderer
{
    public static string ReportDir =>
        Environment.GetEnvironmentVariable("DIYA_REPORT_DIR") is { Length: > 0 } d
            ? d
            : "/opt/meditation-app/data";

    /// <summary>Newest *.pdf in the report directory, or null if none/unreadable.</summary>
    public static string? FindNewestPdf()
    {
        try
        {
            var dir = ReportDir;
            if (!Directory.Exists(dir)) return null;
            return new DirectoryInfo(dir)
                .EnumerateFiles("*.pdf", SearchOption.TopDirectoryOnly)
                .OrderByDescending(f => f.LastWriteTimeUtc)
                .FirstOrDefault()?.FullName;
        }
        catch
        {
            return null;
        }
    }

    /// <summary>
    /// Newest *.pdf whose last-write time is at/after <paramref name="sinceUtc"/> —
    /// i.e. a report produced by the current session (avoids showing a stale PDF
    /// from a previous visitor). Returns null if none/unreadable.
    /// </summary>
    public static string? FindNewestPdfSince(DateTime sinceUtc)
    {
        try
        {
            var dir = ReportDir;
            if (!Directory.Exists(dir)) return null;
            return new DirectoryInfo(dir)
                .EnumerateFiles("*.pdf", SearchOption.TopDirectoryOnly)
                .Where(f => f.LastWriteTimeUtc >= sinceUtc)
                .OrderByDescending(f => f.LastWriteTimeUtc)
                .FirstOrDefault()?.FullName;
        }
        catch
        {
            return null;
        }
    }

    /// <summary>File size in bytes, or -1 if it can't be read.</summary>
    public static long SafeLength(string path)
    {
        try { return new FileInfo(path).Length; }
        catch { return -1; }
    }

    /// <summary>
    /// Render every page of the PDF to Avalonia bitmaps. Runs off the UI thread.
    /// </summary>
    public static Task<List<Bitmap>> RenderPagesAsync(string pdfPath) => Task.Run(() =>
    {
        var pages = new List<Bitmap>();
        var bytes = File.ReadAllBytes(pdfPath);
        using var input = new MemoryStream(bytes);

        foreach (var sk in Conversion.ToImages(input))
        {
            using (sk)
            using (var img = SKImage.FromBitmap(sk))
            using (var data = img.Encode(SKEncodedImageFormat.Png, 90))
            {
                var ms = new MemoryStream();
                data.SaveTo(ms);
                ms.Position = 0;
                pages.Add(new Bitmap(ms));
            }
        }

        return pages;
    });
}
