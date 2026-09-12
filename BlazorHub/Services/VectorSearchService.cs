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
    private bool _isLoaded;
    private Task? _loadingTask;

    public bool IsLoaded => _isLoaded;
    public IReadOnlyList<SkillItem> AllItems => _items;

    public VectorSearchService(HttpClient http)
    {
        _http = http;
    }

    public Task EnsureLoadedAsync(Action<string>? onProgress = null)
    {
        if (_isLoaded) return Task.CompletedTask;
        if (_loadingTask != null) return _loadingTask;

        _loadingTask = LoadInternalAsync(onProgress);
        return _loadingTask;
    }

    private async Task LoadInternalAsync(Action<string>? onProgress)
    {
        onProgress?.Invoke("1/2: 스킬 데이터베이스 로드 중 (skills.json)...");
        var items = await _http.GetFromJsonAsync<List<SkillItem>>("data/skills.json");
        _items = items ?? new List<SkillItem>();

        onProgress?.Invoke("2/2: 6,186개 384차원 벡터 DB 로드 중 (embeddings.bin)...");
        var bytes = await _http.GetByteArrayAsync("embeddings.bin");
        _embeddings = new float[bytes.Length / sizeof(float)];
        Buffer.BlockCopy(bytes, 0, _embeddings, 0, bytes.Length);

        _isLoaded = true;
        onProgress?.Invoke($"✅ C# .NET SIMD 벡터 검색 준비 완료! ({_items.Count:N0}개 에셋)");
    }

    public List<SkillItem> Search(float[] queryVector, string catId = "all", int limit = 80)
    {
        if (!_isLoaded || _embeddings == null || queryVector == null || queryVector.Length != Dimension)
        {
            return GetCategoryItems(catId);
        }

        ReadOnlySpan<float> querySpan = queryVector;

        // C# .NET SIMD 가속: TensorPrimitives.CosineSimilarity
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
