using System;
using System.Net;
using System.Net.Http;
using System.Net.Http.Json;
using System.Text;
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

public enum SessionState
{
    Pending,
    Claimed,
    NotFound,
    NetworkError
}

public sealed record SessionStatusResult(SessionState State, VisitorData? Visitor);

/// <summary>
/// Looks up a visitor by the id encoded in their QR pass.
/// Base URL is configurable via the DIYA_API_BASE environment variable, e.g.
///   DIYA_API_BASE=https://diya-registration.onrender.com
/// </summary>
public static class VisitorApiClient
{
    public static readonly string BaseUrl =
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

    // ---- Sessions (Model B) ------------------------------------------------

    /// <summary>Kiosk starts a session. Returns the token, or null on failure.</summary>
    public static async Task<string?> CreateSessionAsync(CancellationToken ct = default)
    {
        try
        {
            using var content = new StringContent("{}", Encoding.UTF8, "application/json");
            using var resp = await Http.PostAsync($"{BaseUrl}/api/sessions", content, ct);
            if (!resp.IsSuccessStatusCode)
                return null;

            var doc = await resp.Content.ReadFromJsonAsync<SessionCreateResponse>(ct);
            return string.IsNullOrWhiteSpace(doc?.Token) ? null : doc!.Token;
        }
        catch
        {
            return null;
        }
    }

    /// <summary>Kiosk polls a session until the visitor registers on their phone.</summary>
    public static async Task<SessionStatusResult> GetSessionAsync(string token, CancellationToken ct = default)
    {
        if (string.IsNullOrWhiteSpace(token))
            return new SessionStatusResult(SessionState.NotFound, null);

        try
        {
            using var resp = await Http.GetAsync(
                $"{BaseUrl}/api/sessions/{Uri.EscapeDataString(token)}", ct);

            if (resp.StatusCode == HttpStatusCode.NotFound)
                return new SessionStatusResult(SessionState.NotFound, null);
            if (!resp.IsSuccessStatusCode)
                return new SessionStatusResult(SessionState.NetworkError, null);

            var doc = await resp.Content.ReadFromJsonAsync<SessionStatusResponse>(ct);
            if (doc is null)
                return new SessionStatusResult(SessionState.NetworkError, null);

            if (string.Equals(doc.Status, "claimed", StringComparison.OrdinalIgnoreCase)
                && doc.Visitor is not null
                && !string.IsNullOrWhiteSpace(doc.Visitor.Name))
            {
                return new SessionStatusResult(SessionState.Claimed, doc.Visitor);
            }

            return new SessionStatusResult(SessionState.Pending, null);
        }
        catch
        {
            return new SessionStatusResult(SessionState.NetworkError, null);
        }
    }

    /// <summary>
    /// Downloads an image (the visitor's roster photo) as bytes. Returns null on
    /// any failure — a missing/broken photo must never break the kiosk flow.
    /// Only http/https URLs are fetched.
    /// </summary>
    public static async Task<byte[]?> DownloadBytesAsync(string? url, CancellationToken ct = default)
    {
        if (string.IsNullOrWhiteSpace(url)
            || !Uri.TryCreate(url, UriKind.Absolute, out var uri)
            || (uri.Scheme != Uri.UriSchemeHttp && uri.Scheme != Uri.UriSchemeHttps))
            return null;

        try
        {
            using var resp = await Http.GetAsync(uri, ct);
            if (!resp.IsSuccessStatusCode)
                return null;
            return await resp.Content.ReadAsByteArrayAsync(ct);
        }
        catch
        {
            return null;
        }
    }

    private sealed class SessionCreateResponse
    {
        public string? Token { get; set; }
    }

    private sealed class SessionStatusResponse
    {
        public string? Status { get; set; }
        public VisitorData? Visitor { get; set; }
    }
}
