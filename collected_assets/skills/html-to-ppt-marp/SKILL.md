---
name: html-to-ppt-marp
description: Convert Markdown to PowerPoint, PDF, or HTML presentations using Marp. Use when creating slide decks from Markdown, building tech talks or product presentations, generating PPTX from structured content, or automating presentation creation. Supports themes, animations, speaker notes, two-column layouts, and Python/Node.js integration.
---

# Markdown → Sunum (Marp)

Marp ile Markdown'dan profesyonel PPTX, PDF ve HTML sunumları oluşturma rehberi.

---

## 1. Kurulum

```bash
npm install -g @marp-team/marp-cli   # Global CLI
# veya
brew install marp-cli                 # macOS
```

---

## 2. Temel Yapı

```markdown
---
marp: true
theme: default
paginate: true
---

# İlk Slayt

İçerik buraya

---

# İkinci Slayt

- Madde 1
- Madde 2
```

`---` slaytları ayırır. Frontmatter seçenekleri:

```yaml
---
marp: true
theme: default # default | gaia | uncover
size: 16:9 # 4:3 | 16:9
paginate: true
header: 'Şirket Adı'
footer: 'Gizli'
backgroundColor: '#fff'
---
```

---

## 3. CLI Kullanımı

```bash
# PPTX
marp slides.md -o presentation.pptx

# PDF
marp slides.md -o presentation.pdf

# HTML
marp slides.md -o presentation.html

# Tema belirterek
marp slides.md --theme gaia -o presentation.pptx

# İzleme modu (geliştirme)
marp --watch slides.md
```

---

## 4. Tema Seçenekleri

**Built-in temalar:** `default` (temiz, minimal), `gaia` (renkli, modern), `uncover` (cesur, sunum odaklı).

```markdown
<!-- class ile özel slayt stili -->
<!-- _class: lead -->        ← Ortalanmış başlık slaydı
<!-- _class: invert -->      ← Ters renkler
```

---

## 5. Animasyonlar (Fragments)

```html
<section>
  <p class="fragment">İlk görünen</p>
  <p class="fragment fade-up">Sonra bu yukarı kayarak</p>
  <p class="fragment highlight-red">Vurgulanan</p>
</section>
```

Diğer stiller: `fade-in`, `fade-out`, `fade-left`, `fade-right`, `strike`.

---

## 6. İki Sütunlu Layout

```markdown
---
marp: true
style: |
  .cols {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
  }
---

# İki Sütun

<div class="cols">
<div>

## Sol

- Madde A
- Madde B

</div>
<div>

## Sağ

- Madde C
- Madde D

</div>
</div>
```

---

## 7. Konuşmacı Notları

```markdown
# Başlık

İçerik

<!-- Burada konuşmacı notu. 'S' tuşuyla görüntülenir. -->
```

---

## 8. Auto-Animate

Aynı `data-id` değerine sahip elementler slaytlar arasında otomatik animasyon alır:

```html
<!-- Slayt 1 -->
<div data-id="box" style="background: blue; padding: 20px;">Küçük</div>

<!-- Slayt 2 -->
<div data-id="box" style="background: green; padding: 60px; width: 400px;">Büyük</div>
```

---

## 9. Python Entegrasyonu

```python
import subprocess
import tempfile
import os
from pathlib import Path

def markdown_to_pptx(
    md_content: str,
    output_path: str,
    theme: str = 'gaia'
) -> str:
    if '---\nmarp: true' not in md_content:
        md_content = f"---\nmarp: true\ntheme: {theme}\npaginate: true\n---\n\n" + md_content

    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
        f.write(md_content)
        temp_path = f.name

    try:
        subprocess.run(['marp', temp_path, '-o', output_path], check=True)
        return output_path
    finally:
        os.unlink(temp_path)


def create_presentation(title: str, slides: list[dict], output_path: str) -> str:
    md = f"""---
marp: true
theme: gaia
paginate: true
---

<!-- _class: lead -->

# {title}

---

"""
    for slide in slides:
        md += f"# {slide['title']}\n\n"
        for point in slide.get('points', []):
            md += f"- {point}\n"
        md += "\n---\n\n"

    md += "<!-- _class: lead -->\n\n# Teşekkürler\n"
    return markdown_to_pptx(md, output_path)


# Kullanım
slides_data = [
    {'title': 'Problem', 'points': ['Manuel süreç', 'Yüksek hata oranı', 'Zaman kaybı']},
    {'title': 'Çözüm', 'points': ['Otomatik analiz', '%99 doğruluk', 'Anlık sonuç']},
]

create_presentation('Ürün Lansmanı', slides_data, 'sunum.pptx')
```

---

## 10. Teknik Sunum Şablonu

```markdown
---
marp: true
theme: night
paginate: true
---

<!-- _class: lead -->

# API Tasarım İlkeleri

Mühendislik Ekibi — 2024

---

# Gündem

1. RESTful Tasarım
2. Versiyonlama
3. Hata Yönetimi
4. Örnekler

---

# Endpoint Tasarımı

| Metot  | URL     | Açıklama |
| ------ | ------- | -------- |
| GET    | /cv     | Liste    |
| POST   | /cv     | Oluştur  |
| GET    | /cv/:id | Detay    |
| DELETE | /cv/:id | Sil      |

---

# Hata Yanıtı

\`\`\`json
{
"error": "CV_NOT_FOUND",
"message": "İstenen CV bulunamadı",
"statusCode": 404
}
\`\`\`

---

<!-- _class: lead -->

# Sorular?

api-destek@example.com
```

---

## 11. Kısıtlamalar

Marp bazı PowerPoint özelliklerini desteklemiyor: karmaşık geçiş animasyonları, video yerleştirme, izleyici etkileşimi (anket vb.), tracked changes. Bu özellikler gerekiyorsa Google Slides veya PowerPoint native önerilir.
