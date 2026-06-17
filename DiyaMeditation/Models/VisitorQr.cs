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
}
