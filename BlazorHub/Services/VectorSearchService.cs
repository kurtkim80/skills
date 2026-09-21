using System.Net.Http.Json;
using System.Numerics.Tensors;
using BlazorHub.Models;

namespace BlazorHub.Services;

public class VectorSearchService
{
    private readonly HttpClient _http;
    private List<SkillItem> _items = new();
    private readonly List<SkillItem> _customItems = new();
    private float[]? _embeddings;
    private const int Dimension = 384;
    private bool _isCatalogLoaded;
    private bool _isVectorsLoaded;
    private Task? _catalogLoadingTask;
    private Task? _vectorsLoadingTask;
    private readonly Dictionary<string, string> _contentCache = new();

    public bool IsCatalogLoaded => _isCatalogLoaded;
    public bool IsVectorsLoaded => _isVectorsLoaded;
    public IReadOnlyList<SkillItem> AllItems => _items;
    public IReadOnlyList<SkillItem> CustomItems => _customItems;

    public VectorSearchService(HttpClient http)
    {
        _http = http;
    }

    /// <summary>
    /// 1단계: 초경량 카탈로그 데이터(4.8MB) 로드
    /// </summary>
    public Task LoadCatalogAsync(Action<string>? onProgress = null)
    {
        if (_isCatalogLoaded) return Task.CompletedTask;
        if (_catalogLoadingTask != null) return _catalogLoadingTask;

        _catalogLoadingTask = LoadCatalogInternalAsync(onProgress);
        return _catalogLoadingTask;
    }

    private async Task LoadCatalogInternalAsync(Action<string>? onProgress)
    {
        onProgress?.Invoke("스킬 데이터베이스 로드 중 (4.8MB)...");
        var items = await _http.GetFromJsonAsync<List<SkillItem>>("data/skills.json");
        _items = items ?? new List<SkillItem>();
        _isCatalogLoaded = true;
    }

    /// <summary>
    /// 로컬 스토리지 등에 저장된 사용자 커스텀 추가 스킬 병합
    /// </summary>
    public void MergeCustomItems(List<SkillItem>? customList)
    {
        if (customList == null || customList.Count == 0) return;

        foreach (var c in customList)
        {
            if (!IsItemInCatalog(c.Source) && !IsItemInCatalog(c.Id))
            {
                c.Idx = _items.Count;
                _items.Insert(0, c);
                _customItems.Add(c);
            }
        }
    }

    /// <summary>
    /// 특정 저장소나 ID가 이미 카탈로그에 등록되어 있는지 확인
    /// </summary>
    public bool IsItemInCatalog(string? identifier)
    {
        if (string.IsNullOrWhiteSpace(identifier)) return false;
        var clean = identifier.Trim().ToLowerInvariant();
        return _items.Any(x =>
            x.Source.Equals(clean, StringComparison.OrdinalIgnoreCase) ||
            x.Id.Equals(clean, StringComparison.OrdinalIgnoreCase) ||
            x.Name.Equals(clean, StringComparison.OrdinalIgnoreCase) ||
            x.RepoUrl.TrimEnd('/').EndsWith(clean, StringComparison.OrdinalIgnoreCase));
    }

    /// <summary>
    /// 새로운 스킬/저장소를 메모리 카탈로그 맨 앞에 즉시 추가
    /// </summary>
    public void AddItem(SkillItem item)
    {
        if (IsItemInCatalog(item.Source) || IsItemInCatalog(item.Id))
            return;

        item.Idx = _items.Count;
        _items.Insert(0, item);
        _customItems.Insert(0, item);
    }

    /// <summary>
    /// 2단계: 9.5MB AI 벡터 데이터베이스(embeddings.bin) 백그라운드 비동기 로딩
    /// </summary>
    public Task EnsureVectorsLoadedAsync(Action<string>? onProgress = null)
    {
        if (_isVectorsLoaded) return Task.CompletedTask;
        if (_vectorsLoadingTask != null) return _vectorsLoadingTask;

        _vectorsLoadingTask = LoadVectorsInternalAsync(onProgress);
        return _vectorsLoadingTask;
    }

    private async Task LoadVectorsInternalAsync(Action<string>? onProgress)
    {
        onProgress?.Invoke("AI 시맨틱 벡터 엔진 백그라운드 준비 중 (9.5MB)...");
        var bytes = await _http.GetByteArrayAsync("embeddings.bin");
        _embeddings = new float[bytes.Length / sizeof(float)];
        Buffer.BlockCopy(bytes, 0, _embeddings, 0, bytes.Length);

        _isVectorsLoaded = true;
        onProgress?.Invoke($"⚡ C# .NET SIMD 벡터 검색 준비 완료! ({_items.Count:N0}개 에셋)");
    }

    /// <summary>
    /// 스킬의 SKILL.md 마크다운 본문을 온디맨드로 로드 (로컬 또는 GitHub Raw URL)
    /// </summary>
    public async Task<string> GetContentAsync(SkillItem item)
    {
        var cacheKey = !string.IsNullOrEmpty(item.Doc) ? item.Doc : item.Source;
        if (_contentCache.TryGetValue(cacheKey, out var cached))
        {
            return cached;
        }

        // 1. Doc 상대경로가 지정되어 있을 때 시도
        if (!string.IsNullOrEmpty(item.Doc))
        {
            try
            {
                var content = await _http.GetStringAsync(item.Doc);
                _contentCache[cacheKey] = content;
                return content;
            }
            catch { }
        }

        // 2. GitHub 원격 저장소에서 raw SKILL.md / README.md 가져오기 시도
        if (!string.IsNullOrEmpty(item.Source) && item.Source.Contains("/"))
        {
            var rawUrls = new[]
            {
                $"https://raw.githubusercontent.com/{item.Source}/main/SKILL.md",
                $"https://raw.githubusercontent.com/{item.Source}/master/SKILL.md",
                $"https://raw.githubusercontent.com/{item.Source}/main/README.md",
                $"https://raw.githubusercontent.com/{item.Source}/master/README.md"
            };

            foreach (var url in rawUrls)
            {
                try
                {
                    var res = await _http.GetStringAsync(url);
                    if (!string.IsNullOrWhiteSpace(res))
                    {
                        _contentCache[cacheKey] = res;
                        return res;
                    }
                }
                catch { }
            }
        }

        return $"# {item.Name}\n\n**출처 저장소**: [{item.Source}]({item.RepoUrl})\n\n{item.Desc}\n\n```bash\n{item.Install}\n```";
    }

    /// <summary>
    /// C# SIMD 가속 코사인 유사도 검색
    /// </summary>
    public async Task<List<SkillItem>> SearchAsync(float[] queryVector, string catId = "all", int limit = 80)
    {
        if (!_isVectorsLoaded)
        {
            await EnsureVectorsLoadedAsync();
        }

        if (_embeddings == null || queryVector == null || queryVector.Length != Dimension)
        {
            return GetCategoryItems(catId);
        }

        ReadOnlySpan<float> querySpan = queryVector;

        for (int i = 0; i < _items.Count; i++)
        {
            int offset = i * Dimension;
            if (offset + Dimension <= _embeddings.Length)
            {
                ReadOnlySpan<float> candidateSpan = _embeddings.AsSpan(offset, Dimension);
                _items[i].AiScore = TensorPrimitives.CosineSimilarity(querySpan, candidateSpan);
            }
            else
            {
                // 새로 추가된 커스텀 스킬의 경우 (임베딩이 아직 바이너리에 없는 경우 기본 점수 부여)
                if (_items[i].AiScore <= 0f)
                {
                    _items[i].AiScore = 0.5f;
                }
            }
        }

        return _items
            .Where(x => (catId == "all" || x.CatId == catId) && x.AiScore > 0.02f)
            .OrderByDescending(x => x.AiScore)
            .Take(limit)
            .ToList();
    }

    public List<SkillItem> GetCategoryItems(string catId)
    {
        if (catId == "all") return _items;
        return _items.Where(x => x.CatId == catId).ToList();
    }

    public List<SkillItem> GetFilteredSearchResults(string catId, int limit = 80)
    {
        return _items
            .Where(x => (catId == "all" || x.CatId == catId) && x.AiScore > 0.02f)
            .OrderByDescending(x => x.AiScore)
            .Take(limit)
            .ToList();
    }

    public void ResetScores()
    {
        foreach (var item in _items)
        {
            item.AiScore = 0f;
        }
    }

    /// <summary>
    /// 저장소 이름과 설명을 바탕으로 13개 카테고리 중 하나로 자동 분류
    /// </summary>
    public static (string CatId, string CatLabel) ClassifyCategory(string name, string? desc)
    {
        var text = (name + " " + (desc ?? "")).ToLowerInvariant();

        if (text.Contains("rag") || text.Contains("embedding") || text.Contains("vector") || text.Contains("retrieval") || text.Contains("semantic search") || text.Contains("chunking") || text.Contains("rerank"))
            return ("rag_search", "🔍 RAG & 시맨틱 검색");

        if (text.Contains("llm") || text.Contains("prompt") || text.Contains("fine-tuning") || text.Contains("mcp") || text.Contains("agent") || text.Contains("claude") || text.Contains("gpt") || text.Contains("openai") || text.Contains("anthropic"))
            return ("llm_ai", "🧠 LLM & AI 개발");

        if (text.Contains("security") || text.Contains("auth") || text.Contains("vulnerability") || text.Contains("crypto") || text.Contains("xss") || text.Contains("injection") || text.Contains("secret") || text.Contains("guardian"))
            return ("security", "🛡️ 보안 & 취약점");

        if (text.Contains("test") || text.Contains("qa") || text.Contains("jest") || text.Contains("pytest") || text.Contains("mock") || text.Contains("e2e") || text.Contains("cypress") || text.Contains("playwright"))
            return ("testing", "🧪 테스트 & QA");

        if (text.Contains("react") || text.Contains("next") || text.Contains("vue") || text.Contains("frontend") || text.Contains("tailwind") || text.Contains("css") || text.Contains("html") || text.Contains("ui") || text.Contains("ux") || text.Contains("web-design") || text.Contains("svelte"))
            return ("frontend", "🎨 프론트엔드 & UI/UX");

        if (text.Contains("fastapi") || text.Contains("django") || text.Contains("flask") || text.Contains("express") || text.Contains("nestjs") || text.Contains("api") || text.Contains("backend") || text.Contains("graphql") || text.Contains("rest") || text.Contains("grpc"))
            return ("backend", "⚙️ 백엔드 & API");

        if (text.Contains("sql") || text.Contains("database") || text.Contains("postgres") || text.Contains("mysql") || text.Contains("mongo") || text.Contains("redis") || text.Contains("data") || text.Contains("orm") || text.Contains("prisma"))
            return ("database", "🗄️ DB & 데이터");

        if (text.Contains("docker") || text.Contains("kubernetes") || text.Contains("k8s") || text.Contains("devops") || text.Contains("cloud") || text.Contains("aws") || text.Contains("azure") || text.Contains("gcp") || text.Contains("terraform") || text.Contains("helm") || text.Contains("ci-cd"))
            return ("devops", "☁️ DevOps & 클라우드");

        if (text.Contains("ios") || text.Contains("swift") || text.Contains("android") || text.Contains("kotlin") || text.Contains("flutter") || text.Contains("rust") || text.Contains("wasm") || text.Contains("c++") || text.Contains("system") || text.Contains("embedded"))
            return ("mobile_sys", "📱 모바일 & 시스템");

        if (text.Contains("review") || text.Contains("architect") || text.Contains("design") || text.Contains("refactor"))
            return ("architecture", "🏗️ 아키텍처 & 리뷰");

        return ("general_dev", "💻 일반 언어 & 도구");
    }
}
