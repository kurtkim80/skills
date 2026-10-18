using System.Net.Http.Json;
using System.Text.Json;
using BlazorHub.Models;
using Microsoft.JSInterop;

namespace BlazorHub.Services;

/// <summary>
/// GitHub의 실시간 인기 AI 에이전트/스킬 트렌드를 감지하고
/// 검색 추천 리스트 및 카탈로그 DB에 자동으로 추가/갱신하는 서비스
/// </summary>
public class TrendingThemeService
{
    private readonly HttpClient _http;
    private readonly IJSRuntime _js;
    private readonly WasmSkillCollectorService _collector;
    private readonly VectorSearchService _searchService;

    public List<TrendingTheme> Themes { get; private set; } = new();
    public event Action? OnThemesChanged;
    public bool IsRefreshing { get; private set; }
    public string LastUpdatedText { get; private set; } = string.Empty;

    public TrendingThemeService(
        HttpClient http,
        IJSRuntime js,
        WasmSkillCollectorService collector,
        VectorSearchService searchService)
    {
        _http = http;
        _js = js;
        _collector = collector;
        _searchService = searchService;
        InitializeDefaultThemes();
    }

    private void InitializeDefaultThemes()
    {
        Themes = new List<TrendingTheme>
        {
            new() { Id = "morluto-rea", Title = "🔍 REA 역공학", Query = "reverse-engineer-anything", RepoFullName = "morluto/rea", Stars = 316030, Badge = "🔥" },
            new() { Id = "obra-superpowers", Title = "⚡ Superpowers", Query = "superpowers", RepoFullName = "obra/superpowers", Stars = 301457, Badge = "🔥" },
            new() { Id = "browser-use", Title = "🌐 Browser-Use", Query = "browser-use web automation", RepoFullName = "browser-use/browser-use", Stars = 61200, Badge = "🚀" },
            new() { Id = "claude-code", Title = "🤖 Claude Code", Query = "claude-code terminal agent", RepoFullName = "anthropics/claude-code", Stars = 48500, Badge = "🌟" },
            new() { Id = "mcp-servers", Title = "🔌 MCP 서버", Query = "modelcontextprotocol servers", RepoFullName = "modelcontextprotocol/servers", Stars = 64200, Badge = "🛠️" },
            new() { Id = "deepseek-r1", Title = "🧠 DeepSeek R1", Query = "deepseek r1 reasoning", RepoFullName = "deepseek-ai/DeepSeek-R1", Stars = 89200, Badge = "💡" },
            new() { Id = "openhands", Title = "💻 OpenHands", Query = "openhands autonomous coder", RepoFullName = "OpenHands/OpenHands", Stars = 45100, Badge = "🦾" },
            new() { Id = "claude-context", Title = "🎯 RAG & 시맨틱 검색", Query = "claude-context vector search", RepoFullName = "zilliztech/claude-context", Stars = 28500, Badge = "🔍" }
        };
    }

    /// <summary>
    /// 초기 트렌드 데이터 로딩 (정적 data/trending.json + 브라우저 캐시 병합)
    /// </summary>
    public async Task LoadInitialThemesAsync()
    {
        try
        {
            // 1. data/trending.json 정적 파일 로드 (캐시 버스팅)
            long cacheBuster = DateTime.UtcNow.Ticks;
            var jsonThemes = await _http.GetFromJsonAsync<List<TrendingTheme>>($"data/trending.json?t={cacheBuster}");
            if (jsonThemes != null && jsonThemes.Count > 0)
            {
                Themes = jsonThemes;
            }

            // 2. 브라우저 localStorage에 캐시된 최신 동적 갱신본이 있는지 확인
            try
            {
                var cachedJson = await _js.InvokeAsync<string?>("localStorage.getItem", "skills_trending_cache");
                if (!string.IsNullOrWhiteSpace(cachedJson))
                {
                    var cached = JsonSerializer.Deserialize<List<TrendingTheme>>(cachedJson);
                    if (cached != null && cached.Count > 0)
                    {
                        MergeThemes(cached);
                    }
                }
            }
            catch { }

            OnThemesChanged?.Invoke();
        }
        catch (Exception ex)
        {
            Console.WriteLine($"[WASM] 트렌드 초기 로드 경고: {ex.Message}");
        }
    }

    /// <summary>
    /// GitHub API를 비동기 탐색하여 신규 인기 저장소 및 스타 수 변경사항을 자동으로 감지하고 추가
    /// </summary>
    public async Task AutoRefreshTrendingAsync(bool force = false)
    {
        if (IsRefreshing) return;

        try
        {
            // 6시간 주기 체크 (force가 아닌 경우)
            if (!force)
            {
                try
                {
                    var lastUpdatedStr = await _js.InvokeAsync<string?>("localStorage.getItem", "skills_trending_last_ts");
                    if (long.TryParse(lastUpdatedStr, out var lastTs))
                    {
                        var lastDate = new DateTime(lastTs, DateTimeKind.Utc);
                        if (DateTime.UtcNow - lastDate < TimeSpan.FromHours(6))
                        {
                            return; // 아직 6시간 미경과
                        }
                    }
                }
                catch { }
            }

            IsRefreshing = true;
            OnThemesChanged?.Invoke();

            var queries = new (string Query, string Emoji)[]
            {
                ("topic:mcp sort:stars", "🔌"),
                ("topic:ai-agents sort:stars", "🤖"),
                ("skills in:name,description sort:stars", "⚡")
            };

            var discovered = new List<TrendingTheme>();

            foreach (var (q, emoji) in queries)
            {
                try
                {
                    var repos = await _collector.SearchGitHubAsync(q, 6);
                    foreach (var repo in repos)
                    {
                        var shortTitle = repo.Name.Replace('-', ' ');
                        if (shortTitle.Length > 20) shortTitle = shortTitle[..18] + "…";

                        discovered.Add(new TrendingTheme
                        {
                            Id = repo.FullName.Replace('/', '-').ToLowerInvariant(),
                            Title = $"{emoji} {shortTitle}",
                            Query = repo.Name,
                            RepoFullName = repo.FullName,
                            Stars = repo.StargazersCount,
                            Description = repo.Description ?? string.Empty,
                            Badge = "🔥",
                            LastUpdated = DateTime.UtcNow
                        });

                        // 카탈로그에 없는 고스타(10k+ 스타) 저장소는 백그라운드 자동 스킬 등록 시도
                        if (repo.StargazersCount >= 10000 && !_searchService.IsItemInCatalog(repo.FullName))
                        {
                            _ = AutoRegisterRepoToCatalogAsync(repo);
                        }
                    }
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"[WASM] GitHub 트렌드 검색 ({q}) 건너뜀: {ex.Message}");
                }
            }

            if (discovered.Count > 0)
            {
                MergeThemes(discovered);

                // 로컬 스토리지에 캐시
                try
                {
                    var serialized = JsonSerializer.Serialize(Themes);
                    await _js.InvokeVoidAsync("localStorage.setItem", "skills_trending_cache", serialized);
                    await _js.InvokeVoidAsync("localStorage.setItem", "skills_trending_last_ts", DateTime.UtcNow.Ticks.ToString());
                }
                catch { }
            }

            LastUpdatedText = DateTime.Now.ToString("HH:mm");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"[WASM] 트렌드 자동 갱신 중 오류: {ex.Message}");
        }
        finally
        {
            IsRefreshing = false;
            OnThemesChanged?.Invoke();
        }
    }

    /// <summary>
    /// 새로 발굴된 신규 트렌드 저장소를 카탈로그 DB에 자동 등록하여 검색 가능하게 만듦
    /// </summary>
    private async Task AutoRegisterRepoToCatalogAsync(GitHubRepoItem repo)
    {
        try
        {
            var skills = await _collector.ExtractSkillsFromRepoAsync(repo.FullName, repo.Description);
            foreach (var s in skills)
            {
                if (!_searchService.IsItemInCatalog(s.Source) && !_searchService.IsItemInCatalog(s.Id))
                {
                    _searchService.AddItem(s);
                    Console.WriteLine($"[WASM Auto-Add] 신규 인기 스킬 자동 등록 완료: {s.Name} ({repo.FullName})");
                }
            }
        }
        catch { }
    }

    private void MergeThemes(List<TrendingTheme> incoming)
    {
        var existingDict = Themes.ToDictionary(t => t.RepoFullName.ToLowerInvariant(), t => t);

        foreach (var inc in incoming)
        {
            if (string.IsNullOrEmpty(inc.RepoFullName)) continue;
            var key = inc.RepoFullName.ToLowerInvariant();

            if (existingDict.TryGetValue(key, out var existing))
            {
                if (inc.Stars > 0) existing.Stars = inc.Stars;
                if (!string.IsNullOrEmpty(inc.Description)) existing.Description = inc.Description;
                existing.LastUpdated = DateTime.UtcNow;
            }
            else
            {
                Themes.Add(inc);
            }
        }

        // 스타 수 기준 내림차순 정렬 및 상위 16개 유지
        Themes = Themes.OrderByDescending(t => t.Stars).Take(16).ToList();
    }
}
