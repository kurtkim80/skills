namespace BlazorHub.Models;

/// <summary>
/// 실시간 GitHub 트렌드 및 추천 인기 검색 테마 모델
/// </summary>
public class TrendingTheme
{
    public string Id { get; set; } = string.Empty;
    public string Title { get; set; } = string.Empty;
    public string Query { get; set; } = string.Empty;
    public string RepoFullName { get; set; } = string.Empty;
    public int Stars { get; set; }
    public string Description { get; set; } = string.Empty;
    public string Badge { get; set; } = "🔥";
    public DateTime LastUpdated { get; set; } = DateTime.UtcNow;

    public string DisplayLabel
    {
        get
        {
            if (Stars > 0)
            {
                var starStr = Stars >= 1000 ? $"{(Stars / 1000.0):0.#}k" : Stars.ToString();
                return $"{Title} ({starStr}★)";
            }
            return Title;
        }
    }
}
