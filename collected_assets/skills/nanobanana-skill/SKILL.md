---
name: nanobanana-skill
description: Generate or edit images using Google Gemini API via nanobanana Python script. Use when asked to create, generate, or edit images with AI assistance.
---

# Nanobanana Image Generation Skill

Google Gemini API üzerinden AI destekli görsel oluşturma ve düzenleme rehberi.

## When to use this skill

- AI ile görsel oluşturulacağında
- Mevcut görseller düzenlenecekken
- Logo, banner, illüstrasyon, wallpaper üretilirken

---

## 1. Gereksinimler

```bash
# GEMINI_API_KEY gerekli
export GEMINI_API_KEY="your-api-key"
# veya ~/.nanobanana.env dosyasında

# Bağımlılıklar
pip install google-genai Pillow python-dotenv
```

---

## 2. Temel Kullanım

```bash
# Basit görsel oluşturma
python3 nanobanana.py --prompt "Gün batımında dağ manzarası"

# Özel boyut ve çıktı dosyası
python3 nanobanana.py \
  --prompt "Minimalist tech startup logosu" \
  --size 1024x1024 \
  --output "logo.png"

# Görsel düzenleme
python3 nanobanana.py \
  --prompt "Gökyüzüne gökkuşağı ekle" \
  --input photo.png \
  --output "photo-with-rainbow.png"

# Hızlı model ile
python3 nanobanana.py \
  --prompt "Kedi çizimi" \
  --model gemini-2.5-flash-image \
  --output "cat.png"

# Yüksek çözünürlük
python3 nanobanana.py \
  --prompt "Fütüristik şehir manzarası" \
  --size 1344x768 \
  --resolution 2K \
  --output "cityscape.png"
```

---

## 3. Parametreler

### Boyut (--size)

| Boyut       | Oran | Kullanım                  |
| ----------- | ---- | ------------------------- |
| `1024x1024` | 1:1  | Logo, sosyal medya        |
| `768x1344`  | 9:16 | Story, mobil (varsayılan) |
| `1344x768`  | 16:9 | Wallpaper, banner         |
| `864x1184`  | 3:4  | Dikey içerik              |
| `1184x864`  | 4:3  | Yatay içerik              |
| `1536x672`  | 21:9 | Ultra geniş               |

### Model (--model)

| Model                        | Özellik                    |
| ---------------------------- | -------------------------- |
| `gemini-3-pro-image-preview` | Yüksek kalite (varsayılan) |
| `gemini-2.5-flash-image`     | Hızlı üretim               |

### Çözünürlük (--resolution)

`1K` (varsayılan), `2K`, `4K`

---

## 4. Etkili Prompt Yazma

**Spesifik ol:**

```
❌ "Bir şehir görseli"
✅ "Modern Tokyo sokağı, gece, neon ışıklar, yağmurlu, fotogerçekçi"
```

**Stil belirt:**

```
✅ "Minimalist vektör illüstrasyon, düz renkler, siyah arka plan"
✅ "Fotogerçekçi, 8K, sinematik ışıklandırma"
✅ "Suluboya resim tarzı, yumuşak renkler"
```

**Kategori önerileri:**

- Logo/grafik: `1024x1024`, minimalist vektör stil
- Sosyal medya story: `768x1344`, canlı renkler
- Wallpaper: `1344x768` veya `1536x672`, `2K` çözünürlük
- Thumbnail: `1184x864`, güçlü odak noktası

---

## 5. Çoklu Görsel Düzenleme

```bash
# Birden fazla görsel birleştir
python3 nanobanana.py \
  --prompt "Bu iki görseli tek bir panoramada birleştir" \
  --input sol_gorsel.png sag_gorsel.png \
  --size 1536x672 \
  --output "panorama.png"
```

---

## 6. Hata Yönetimi

```
❌ API key hatası:
   → GEMINI_API_KEY export edildi mi? ~/.nanobanana.env var mı?

❌ Görsel oluşturulmadı:
   → Prompt daha spesifik yap, "görsel oluştur" ibaresini ekle

❌ Düşük kalite:
   → Resolution'ı artır: --resolution 2K
   → Model değiştir: --model gemini-3-pro-image-preview
```
