using System;
using System.Net;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading;
using System.Threading.Tasks;

namespace DiyaMeditation.Models;

public enum FetchStatus
{
    Found,
    NotFound,
    NetworkError
}

public sealed record FetchResult(FetchStatus Status, VisitorData? Visitor);

/// <summary>
/// Looks up a visitor by the id encoded in their QR pass.
/// Base URL is configurable via the DIYA_API_BASE environment variable, e.g.
///   DIYA_API_BASE=https://diya-registration.onrender.com
/// </summary>
public static class VisitorApiClient
{
    private static readonly string BaseUrl =
        (Environment.GetEnvironmentVariable("DIYA_API_BASE")
         ?? "https://diya-registration.onrender.com").TrimEnd('/');

    private static readonly HttpClient Http = new()
    {
        // Render's free tier can cold-start (~30-50s) after being idle.
        Timeout = TimeSpan.FromSeconds(60)
    };

    public static async Task<FetchResult> FetchAsync(string id, CancellationToken ct = default)
    {
        if (string.IsNullOrWhiteSpace(id))
            return new FetchResult(FetchStatus.NotFound, null);

        var url = $"{BaseUrl}/api/visitors/{Uri.EscapeDataString(id)}";
        try
        {
            using var resp = await Http.GetAsync(url, ct);

            if (resp.StatusCode == HttpStatusCode.NotFound)
                return new FetchResult(FetchStatus.NotFound, null);

            if (!resp.IsSuccessStatusCode)
                return new FetchResult(FetchStatus.NetworkError, null);

            var v = await resp.Content.ReadFromJsonAsync<VisitorData>(cancellationToken: ct);
            if (v is null || string.IsNullOrWhiteSpace(v.Name))
                return new FetchResult(FetchStatus.NotFound, null);

            return new FetchResult(FetchStatus.Found, v);
        }
        catch
        {
            // timeout, DNS failure, no network, etc.
            return new FetchResult(FetchStatus.NetworkError, null);
        }
    }
}
