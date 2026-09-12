// aiSearch.js - In-browser Hugging Face Transformers.js Query Vectorizer for Blazor WebAssembly

let aiPipelineInstance = null;
let aiLoadingPromise = null;

window.initAiPipeline = async function (statusCallbackObj) {
  if (aiPipelineInstance) return true;
  if (aiLoadingPromise) return aiLoadingPromise;

  aiLoadingPromise = (async () => {
    try {
      const { pipeline, env } = await import('https://cdn.jsdelivr.net/npm/@xenova/transformers@2.17.2');
      env.allowLocalModels = false;

      aiPipelineInstance = await pipeline('feature-extraction', 'Xenova/all-MiniLM-L6-v2', {
        quantized: true,
        progress_callback: (d) => {
          if (d.status === 'progress' && d.progress && statusCallbackObj) {
            statusCallbackObj.invokeMethodAsync('OnModelDownloadProgress', Math.round(d.progress));
          }
        }
      });
      return true;
    } catch (err) {
      console.error('Transformers.js init error:', err);
      aiLoadingPromise = null;
      return false;
    }
  })();

  return aiLoadingPromise;
};

window.vectorizeQuery = async function (text, statusCallbackObj) {
  if (!text || !text.trim()) return null;
  if (!aiPipelineInstance) {
    const ok = await window.initAiPipeline(statusCallbackObj);
    if (!ok || !aiPipelineInstance) throw new Error('AI Model load failed');
  }

  const out = await aiPipelineInstance(text.trim(), { pooling: 'mean', normalize: true });
  // Return regular array of numbers so Blazor can deserialize into float[]
  return Array.from(out.data);
};

window.copyToClipboard = async function (text) {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch (e) {
    const ta = document.createElement('textarea');
    ta.value = text;
    document.body.appendChild(ta);
    ta.select();
    document.execCommand('copy');
    document.body.removeChild(ta);
    return true;
  }
};

window.setAppTheme = function (theme) {
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem('theme', theme);
};

window.getSavedTheme = function () {
  return localStorage.getItem('theme') ||
    (window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark');
};
