---
name: gemini-skill
description: Execute Google Gemini models via CLI or API for complex reasoning, code analysis, and AI-powered tasks. Use when needing Gemini's capabilities alongside or as alternative to Anthropic Claude, especially for multimodal or large context tasks.
---

# Gemini Skill

Google Gemini modellerine CLI veya API üzerinden erişim rehberi.

## When to use this skill

- Anthropic Claude'a alternatif AI perspektifi gerektiğinde
- Çok büyük context window gerektiren görevlerde (Gemini 1M token)
- Multimodal görevlerde (görsel + metin)
- Gemini CLI yüklüyse ve API key konfigüre edilmişse

---

## 1. Gemini CLI (Yüklüyse)

```bash
# Temel kullanım
gemini "prompt buraya"

# Dosya analizi
gemini "Bu kodu incele: $(cat app.py)"

# Belirli model
GEMINI_MODEL=gemini-2.5-flash gemini "hızlı soru"
```

**Varsayılan model**: `gemini-2.5-pro` (en güçlü)
**Hızlı model**: `gemini-2.5-flash` (daha ucuz/hızlı)

---

## 2. Gemini API (OpenAI-Uyumlu SDK)

### Python

```python
import google.generativeai as genai

genai.configure(api_key="GEMINI_API_KEY")

model = genai.GenerativeModel('gemini-2.5-pro')
response = model.generate_content("Prompt buraya")
print(response.text)
```

### JavaScript/TypeScript

```typescript
import { GoogleGenerativeAI } from '@google/generative-ai'

const genai = new GoogleGenerativeAI(process.env.GEMINI_API_KEY!)
const model = genai.getGenerativeModel({ model: 'gemini-2.5-pro' })

const result = await model.generateContent('Prompt buraya')
console.log(result.response.text())
```

### OpenRouter Üzerinden (Talent Architect'te Tercih Edilen)

Talent Architect'te Gemini'ye OpenRouter üzerinden erişilebilir:

```typescript
import OpenAI from 'openai'

const client = new OpenAI({
  baseURL: 'https://openrouter.ai/api/v1 ',
  apiKey: process.env.OPENROUTER_API_KEY,
})

const completion = await client.chat.completions.create({
  model: 'google/gemini-2.5-flash',
  messages: [{ role: 'user', content: prompt }],
})
```

---

## 3. Model Karşılaştırması

| Model                       | Kullanım          | Context  | Hız   |
| --------------------------- | ----------------- | -------- | ----- |
| `gemini-2.5-pro`            | Karmaşık görevler | 1M token | Yavaş |
| `gemini-2.5-flash`          | Hızlı görevler    | 1M token | Hızlı |
| `gemini-2.0-flash-exp:free` | Test/prototip     | Sınırlı  | Hızlı |

---

## 4. Multimodal Kullanım

```python
import google.generativeai as genai
from PIL import Image

genai.configure(api_key="GEMINI_API_KEY")
model = genai.GenerativeModel('gemini-2.5-pro')

img = Image.open('screenshot.png')
response = model.generate_content(["Bu UI screenshot'ını analiz et:", img])
print(response.text)
```

---

## 5. Talent Architect Entegrasyon Notu

Proje halihazırda `OPENROUTER_API_KEY` ile Gemini'ye erişebilir. Yeni AI feature için:

1. `lib/server/ai/` altındaki mevcut provider wrapper'larına bak
2. OpenRouter üzerinden Gemini eklemek için mevcut pattern'ı kullan
3. Direkt Gemini SDK kullanma — transport değişirse tüm kod güncellenmeli

---

## 6. Kaynaklar

- Gemini API: https://ai.google.dev/
- Gemini Models: https://ai.google.dev/gemini-api/docs/models/gemini
- OpenRouter (Gemini): https://openrouter.ai/models?q=google
