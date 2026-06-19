using System;
using System.Text;
using System.Text.Json;

namespace DiyaMeditation.Models;

public static class VisitorQr
{
    private const string Prefix = "DIYA1:";

    public static bool TryParse(string? raw, out VisitorData? visitor)
    {
        visitor = null;
        if (string.IsNullOrWhiteSpace(raw))
            return false;

        raw = raw.Trim();

        string json;
        if (raw.StartsWith(Prefix, StringComparison.OrdinalIgnoreCase))
        {
            try { json = Encoding.UTF8.GetString(DecodeBase64(raw.Substring(Prefix.Length))); }
            catch { return false; }
        }
        else if (raw.StartsWith("{", StringComparison.Ordinal))
        {
            json = raw;
        }
        else
        {
            return false;
        }

        try
        {
            var v = JsonSerializer.Deserialize<VisitorData>(
                json, new JsonSerializerOptions { PropertyNameCaseInsensitive = true });

            if (v is null || string.IsNullOrWhiteSpace(v.Name))
                return false;

            visitor = v;
            return true;
        }
        catch
        {
            return false;
        }
    }

    private static byte[] DecodeBase64(string s)
    {
        s = s.Trim().Replace('-', '+').Replace('_', '/');
        switch (s.Length % 4)
        {
            case 2: s += "=="; break;
            case 3: s += "="; break;
        }
        return Convert.FromBase64String(s);
    }

    /// <summary>
    /// Extracts the short visitor id from a scanned QR payload. Accepts:
    ///   - a bare id            ("7F3KM9AC")
    ///   - a prefixed id        ("DIYA1:7F3KM9AC")
    ///   - a full URL           ("https://.../v/7F3KM9AC")
    /// Returns the normalised (upper-case) id, or null if it doesn't look like an id.
    /// </summary>
    public static string? ExtractId(string? raw)
    {
        if (string.IsNullOrWhiteSpace(raw))
            return null;

        var s = raw.Trim();

        if (s.StartsWith(Prefix, StringComparison.OrdinalIgnoreCase))
            s = s.Substring(Prefix.Length).Trim();

        // If it's a URL, take the last non-empty path segment.
        var slash = s.LastIndexOf('/');
        if (slash >= 0 && slash < s.Length - 1)
            s = s.Substring(slash + 1);

        s = s.Trim().ToUpperInvariant();

        if (s.Length == 0 || s.Length > 64)
            return null;

        foreach (var c in s)
            if (!char.IsLetterOrDigit(c))
                return null;

        return s;
    }
}
