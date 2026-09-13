using System.Net.Http.Json;
using System.Numerics.Tensors;
using BlazorHub.Models;

namespace BlazorHub.Services;

public class VectorSearchService
{
    private readonly HttpClient _http;
    private List<SkillItem> _items = new();
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

    public VectorSearchService(HttpClient http)
    {
        _http = http;
    }

    /// <summary>
    /// 1단계: 초경량 카탈로그 데이터(4.8MB)만 신속하게 로드하여 첫 화면 즉시 렌더링
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
    /// 2단계: 9.5MB AI 벡터 데이터베이스(embeddings.bin)를 백그라운드에서 비동기 로딩 (화면 블로킹 없음)
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
    /// 사용자가 카드를 클릭했을 때 해당 스킬의 SKILL.md 마크다운 본문을 온디맨드로 즉시 로드 (1~3KB)
    /// </summary>
    public async Task<string> GetContentAsync(SkillItem item)
    {
        if (string.IsNullOrEmpty(item.Doc))
        {
            return "// 상세 지침 및 사양이 등록되지 않은 에셋입니다.";
        }

        if (_contentCache.TryGetValue(item.Doc, out var cached))
        {
            return cached;
        }

        try
        {
            var content = await _http.GetStringAsync(item.Doc);
            _contentCache[item.Doc] = content;
            return content;
        }
        catch (Exception ex)
        {
            return $"// 상세 사양을 불러오지 못했습니다: {ex.Message}";
        }
    }

    /// <summary>
    /// C# SIMD 가속 코사인 유사도 검색 (TensorPrimitives.CosineSimilarity)
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
}
