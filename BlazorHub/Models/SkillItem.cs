using System.Text.Json.Serialization;

namespace BlazorHub.Models;

public class SkillItem
{
    [JsonPropertyName("idx")]
    public int Idx { get; set; }

    [JsonPropertyName("id")]
    public string Id { get; set; } = string.Empty;

    [JsonPropertyName("name")]
    public string Name { get; set; } = string.Empty;

    [JsonPropertyName("type")]
    public string Type { get; set; } = "skill";

    [JsonPropertyName("catId")]
    public string CatId { get; set; } = "all";

    [JsonPropertyName("catLabel")]
    public string CatLabel { get; set; } = string.Empty;

    [JsonPropertyName("desc")]
    public string Desc { get; set; } = string.Empty;

    [JsonPropertyName("source")]
    public string Source { get; set; } = string.Empty;

    [JsonPropertyName("repoUrl")]
    public string RepoUrl { get; set; } = string.Empty;

    [JsonPropertyName("content")]
    public string Content { get; set; } = string.Empty;

    [JsonPropertyName("install")]
    public string Install { get; set; } = string.Empty;

    [JsonIgnore]
    public float AiScore { get; set; } = 0f;
}
