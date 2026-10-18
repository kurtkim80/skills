using System.Net.Http.Json;
using System.Text.Json;
using System.Text.RegularExpressions;
using BlazorHub.Models;

namespace BlazorHub.Services;

/// <summary>
/// 브라우저 WASM 클라이언트에서 직접 GitHub API 및 원격 에셋을 탐색, 수집, 파싱하는 서비스
/// (HobbyCollector의 WasmCollectorService 패턴 벤치마킹)
/// </summary>
public class WasmSkillCollectorService
{
    private readonly HttpClient _http;

    public WasmSkillCollectorService(HttpClient http)
    {
        _http = http;
    }

    /// <summary>
    /// GitHub Search API를 통해 스킬/에이전트 저장소 실시간 탐색 (CORS 지원)
    /// </summary>
    public async Task<List<GitHubRepoItem>> SearchGitHubAsync(string query, int limit = 20)
    {
        if (string.IsNullOrWhiteSpace(query)) return new List<GitHubRepoItem>();

        // 1. owner/repo 또는 github.com URL 직접 입력인 경우 Direct Lookup 우선 수행
        var (owner, repo) = ParseOwnerAndRepo(query);
        if (!string.IsNullOrEmpty(owner) && !string.IsNullOrEmpty(repo))
        {
            var direct = await GetSingleRepoAsync(owner, repo);
            if (direct != null)
            {
                return new List<GitHubRepoItem> { direct };
            }
        }

        // 2. 검색어 문법 정제 (콜론 및 GitHub Search API 예약 특수문자 안전화)
        var sanitized = SanitizeGitHubQuery(query);
        var clean = Uri.EscapeDataString(sanitized);

        // 3. 1차 시도: 사용자가 입력한 검색어 그대로 정밀 검색
        string url = $"https://api.github.com/search/repositories?q={clean}&sort=stars&order=desc&per_page={limit}";

        try
        {
            var items = await FetchSearchResultsAsync(url);
            if (items.Count > 0)
            {
                return items;
            }

            // 4. 검색 결과가 없고 키워드에 skills/agent/mcp가 없으면 폴백 확장 검색 시도
            if (!sanitized.Contains("skill", StringComparison.OrdinalIgnoreCase) &&
                !sanitized.Contains("agent", StringComparison.OrdinalIgnoreCase) &&
                !sanitized.Contains("mcp", StringComparison.OrdinalIgnoreCase))
            {
                string fallbackUrl = $"https://api.github.com/search/repositories?q={clean}+skills&sort=stars&order=desc&per_page={limit}";
                items = await FetchSearchResultsAsync(fallbackUrl);
                return items;
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"[WASM] GitHub Search 오류: {ex.Message}");
        }

        return new List<GitHubRepoItem>();
    }

    private async Task<List<GitHubRepoItem>> FetchSearchResultsAsync(string url)
    {
        using var req = new HttpRequestMessage(HttpMethod.Get, url);
        req.Headers.Add("User-Agent", "Blazor-WASM-SkillHub");
        req.Headers.Add("Accept", "application/vnd.github.v3+json");

        var res = await _http.SendAsync(req);
        if (res.IsSuccessStatusCode)
        {
            var result = await res.Content.ReadFromJsonAsync<GitHubSearchResult>();
            return result?.Items ?? new List<GitHubRepoItem>();
        }
        return new List<GitHubRepoItem>();
    }

    private async Task<GitHubRepoItem?> GetSingleRepoAsync(string owner, string repo)
    {
        string url = $"https://api.github.com/repos/{owner}/{repo}";
        try
        {
            using var req = new HttpRequestMessage(HttpMethod.Get, url);
            req.Headers.Add("User-Agent", "Blazor-WASM-SkillHub");
            req.Headers.Add("Accept", "application/vnd.github.v3+json");

            var res = await _http.SendAsync(req);
            if (res.IsSuccessStatusCode)
            {
                return await res.Content.ReadFromJsonAsync<GitHubRepoItem>();
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"[WASM] Direct repo 조회 오류 ({owner}/{repo}): {ex.Message}");
        }
        return null;
    }

    private static string SanitizeGitHubQuery(string query)
    {
        var tokens = query.Trim().Split(' ', StringSplitOptions.RemoveEmptyEntries);
        var validQualifiers = new HashSet<string>(StringComparer.OrdinalIgnoreCase)
        {
            "user", "org", "repo", "language", "topic", "stars", "forks", "in"
        };

        var cleanedTokens = new List<string>();
        foreach (var token in tokens)
        {
            var colonIdx = token.IndexOf(':');
            if (colonIdx > 0)
            {
                var prefix = token[..colonIdx];
                if (!validQualifiers.Contains(prefix))
                {
                    // 예: "REA: Reverse" -> "REA Reverse"
                    cleanedTokens.Add(token.Replace(':', ' '));
                    continue;
                }
            }
            else if (token == ":")
            {
                continue;
            }

            cleanedTokens.Add(token);
        }

        return string.Join(" ", string.Join(" ", cleanedTokens).Split(' ', StringSplitOptions.RemoveEmptyEntries));
    }

    /// <summary>
    /// GitHub 저장소 URL 또는 owner/repo로부터 SKILL.md 및 에셋 정보를 직접 수집
    /// </summary>
    public async Task<List<SkillItem>> ExtractSkillsFromRepoAsync(string repoFullNameOrUrl, string? customDesc = null)
    {
        var (owner, repo) = ParseOwnerAndRepo(repoFullNameOrUrl);
        if (string.IsNullOrEmpty(owner) || string.IsNullOrEmpty(repo))
        {
            throw new ArgumentException("유효한 GitHub 저장소 주소(owner/repo)를 입력해주세요.");
        }

        var results = new List<SkillItem>();
        var branches = new[] { "main", "master" };

        // 1. 루트의 SKILL.md 탐색
        string? rootSkillMd = null;
        string matchedBranch = "main";

        foreach (var b in branches)
        {
            var rawUrl = $"https://raw.githubusercontent.com/{owner}/{repo}/{b}/SKILL.md";
            try
            {
                var text = await _http.GetStringAsync(rawUrl);
                if (!string.IsNullOrWhiteSpace(text) && (text.Contains("name:") || text.Contains("# ")))
                {
                    rootSkillMd = text;
                    matchedBranch = b;
                    break;
                }
            }
            catch { }
        }

        if (!string.IsNullOrEmpty(rootSkillMd))
        {
            var parsed = ParseSkillMarkdown(rootSkillMd, owner, repo, matchedBranch, "SKILL.md", customDesc);
            results.Add(parsed);
            return results;
        }

        // 2. 루트 SKILL.md가 없는 경우 다양한 스킬 디렉토리 탐색 (.agents/skills, skills, .claude/skills 등)
        var possibleDirs = new[] { ".agents/skills", "skills", ".claude/skills", ".github/skills", "skill-src" };
        foreach (var dir in possibleDirs)
        {
            try
            {
                using var req = new HttpRequestMessage(HttpMethod.Get, $"https://api.github.com/repos/{owner}/{repo}/contents/{dir}");
                req.Headers.Add("User-Agent", "Blazor-WASM-SkillHub");
                req.Headers.Add("Accept", "application/vnd.github.v3+json");

                var res = await _http.SendAsync(req);
                if (res.IsSuccessStatusCode)
                {
                    var json = await res.Content.ReadAsStringAsync();
                    using var doc = JsonDocument.Parse(json);
                    if (doc.RootElement.ValueKind == JsonValueKind.Array)
                    {
                        foreach (var item in doc.RootElement.EnumerateArray())
                        {
                            var name = item.TryGetProperty("name", out var n) ? n.GetString() : null;
                            var type = item.TryGetProperty("type", out var t) ? t.GetString() : null;

                            if (type == "dir" && !string.IsNullOrEmpty(name))
                            {
                                var skillDocUrl = $"https://raw.githubusercontent.com/{owner}/{repo}/main/{dir}/{name}/SKILL.md";
                                string? rawContent = null;
                                try
                                {
                                    rawContent = await _http.GetStringAsync(skillDocUrl);
                                }
                                catch { }

                                if (!string.IsNullOrEmpty(rawContent))
                                {
                                    var parsed = ParseSkillMarkdown(rawContent, owner, repo, "main", $"{dir}/{name}/SKILL.md", customDesc);
                                    results.Add(parsed);
                                }
                                else
                                {
                                    var (catId, catLabel) = VectorSearchService.ClassifyCategory(name, customDesc);
                                    results.Add(new SkillItem
                                    {
                                        Id = $"{repo}:{name}",
                                        Name = name,
                                        Type = "skill",
                                        CatId = catId,
                                        CatLabel = catLabel,
                                        Desc = $"{repo}에서 수집된 서브 스킬: {name}",
                                        Source = $"{owner}/{repo}",
                                        RepoUrl = $"https://github.com/{owner}/{repo}",
                                        Install = $"mkdir -p ~/.config/opencode/skills/{name} && curl -fsSL {skillDocUrl} -o ~/.config/opencode/skills/{name}/SKILL.md",
                                        Doc = skillDocUrl
                                    });
                                }
                            }
                        }
                        if (results.Count > 0) break;
                    }
                }
            }
            catch { }
        }

        // 3. 디렉토리에서도 못 찾으면 저장소 메타데이터 기반 기본 스킬 생성
        if (results.Count == 0)
        {
            var (catId, catLabel) = VectorSearchService.ClassifyCategory(repo, customDesc);
            var docUrl = $"https://raw.githubusercontent.com/{owner}/{repo}/main/SKILL.md";
            results.Add(new SkillItem
            {
                Id = repo,
                Name = repo,
                Type = "skill",
                CatId = catId,
                CatLabel = catLabel,
                Desc = !string.IsNullOrEmpty(customDesc) ? customDesc : $"GitHub 저장소: {owner}/{repo}",
                Source = $"{owner}/{repo}",
                RepoUrl = $"https://github.com/{owner}/{repo}",
                Install = $"mkdir -p ~/.config/opencode/skills/{repo} && curl -fsSL {docUrl} -o ~/.config/opencode/skills/{repo}/SKILL.md",
                Doc = docUrl
            });
        }

        return results;
    }

    /// <summary>
    /// SKILL.md 마크다운 본문 파싱 (YAML Frontmatter 및 설명 추출)
    /// </summary>
    private SkillItem ParseSkillMarkdown(string content, string owner, string repo, string branch, string relativePath, string? fallbackDesc)
    {
        string name = repo;
        string desc = fallbackDesc ?? string.Empty;

        // Frontmatter 파싱 (--- ... ---)
        var match = Regex.Match(content, @"^---\s*\n(.*?)\n---\s*\n", RegexOptions.Singleline);
        if (match.Success)
        {
            var yaml = match.Groups[1].Value;
            var nameMatch = Regex.Match(yaml, @"(?m)^name:\s*(.+)$");
            if (nameMatch.Success) name = nameMatch.Groups[1].Value.Trim('\'', '"', ' ');

            var descMatch = Regex.Match(yaml, @"(?m)^description:\s*(.+)$");
            if (descMatch.Success) desc = descMatch.Groups[1].Value.Trim('\'', '"', ' ');
        }

        if (string.IsNullOrEmpty(desc))
        {
            // 첫 번째 헤딩(#) 다음의 일반 텍스트 라인 탐색
            var headingMatch = Regex.Match(content, @"(?m)^#\s+(.+)$");
            if (headingMatch.Success && name == repo)
            {
                name = headingMatch.Groups[1].Value.Trim();
            }
            desc = fallbackDesc ?? $"{repo} 오픈코드 스킬 에셋";
        }

        var (catId, catLabel) = VectorSearchService.ClassifyCategory(name, desc);
        var rawUrl = $"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{relativePath}";

        return new SkillItem
        {
            Id = name.ToLowerInvariant().Replace(' ', '-'),
            Name = name,
            Type = "skill",
            CatId = catId,
            CatLabel = catLabel,
            Desc = desc,
            Source = $"{owner}/{repo}",
            RepoUrl = $"https://github.com/{owner}/{repo}",
            Install = $"mkdir -p ~/.config/opencode/skills/{name} && curl -fsSL {rawUrl} -o ~/.config/opencode/skills/{name}/SKILL.md",
            Doc = rawUrl,
            Content = content
        };
    }

    private static (string Owner, string Repo) ParseOwnerAndRepo(string input)
    {
        if (string.IsNullOrWhiteSpace(input)) return (string.Empty, string.Empty);

        var cleaned = input.Trim().TrimEnd('/');
        if (cleaned.EndsWith(".git", StringComparison.OrdinalIgnoreCase))
        {
            cleaned = cleaned[..^4];
        }

        if (cleaned.StartsWith("https://github.com/", StringComparison.OrdinalIgnoreCase))
        {
            cleaned = cleaned["https://github.com/".Length..];
        }
        else if (cleaned.StartsWith("github.com/", StringComparison.OrdinalIgnoreCase))
        {
            cleaned = cleaned["github.com/".Length..];
        }

        var parts = cleaned.Split('/');
        if (parts.Length >= 2)
        {
            return (parts[0], parts[1]);
        }

        return (string.Empty, string.Empty);
    }
}
