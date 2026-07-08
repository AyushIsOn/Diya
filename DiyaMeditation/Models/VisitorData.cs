using System.Text.Json.Serialization;

namespace DiyaMeditation.Models;

public sealed class VisitorData
{
    public string Name { get; set; } = "";
    public string Email { get; set; } = "";
    public int Age { get; set; }

    // Direct image URL from the admin roster's "Image" column. The API returns
    // it as snake_case "image_url", so map it explicitly.
    [JsonPropertyName("image_url")]
    public string ImageUrl { get; set; } = "";
}
