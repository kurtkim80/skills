---
name: office-to-markdown
description: Convert Office documents (Word, Excel, PowerPoint, PDF) to Markdown using Microsoft's markitdown library. Use when extracting content from Office files for version control, AI processing, documentation archiving, or RAG corpus creation. Supports batch conversion, metadata preservation, and AI-enhanced image description via Claude.
---

# Office → Markdown (markitdown)

Microsoft'un açık kaynaklı `markitdown` kütüphanesi ile Office dosyalarını Markdown'a dönüştürme rehberi.

---

## 1. Kurulum

```bash
pip install markitdown          # Temel
pip install markitdown[all]     # Görsel OCR + ses transkripsiyon dahil
```

---

## 2. Desteklenen Formatlar

| Format     | Uzantı     | Notlar                            |
| ---------- | ---------- | --------------------------------- |
| Word       | .docx      | Metin, tablo, temel biçimlendirme |
| Excel      | .xlsx      | Sayfalar → Markdown tabloları     |
| PowerPoint | .pptx      | Slaytlar → Bölümler               |
| PDF        | .pdf       | Metin çıkarma                     |
| HTML       | .html      | Temiz Markdown                    |
| Görsel     | .jpg, .png | LLM ile OCR (opsiyonel)           |
| ZIP        | .zip       | İçerdiği dosyaları işler          |

---

## 3. Temel Kullanım

```python
from markitdown import MarkItDown
from pathlib import Path

md = MarkItDown()

# Tek dosya dönüştürme
result = md.convert("rapor.docx")
print(result.text_content)

# Dosyaya kaydet
Path("rapor.md").write_text(result.text_content, encoding='utf-8')
```

### CLI ile

```bash
markitdown rapor.docx > rapor.md
markitdown rapor.docx -o rapor.md
```

---

## 4. Format Örnekleri

### Word Çıktısı

```markdown
# Yıllık Rapor 2024

## Yönetici Özeti

Bu rapor temel başarıları özetlemektedir...

### Temel Metrikler

| Metrik | 2023 | 2024 | Değişim |
| ------ | ---- | ---- | ------- |
| Gelir  | 10M₺ | 12M₺ | +%20    |
```

### PowerPoint Çıktısı

Her slayt bir bölüm olur, konuşmacı notları da dahil edilir.

```markdown
# Slayt 1: Şirket Genel Bakışı

Misyonumuz şudur...

## Temel Noktalar

- İnovasyon önce gelir
- Müşteri odaklılık

---

# Slayt 2: Pazar Analizi
```

---

## 5. Görsel İçin AI Entegrasyonu

```python
import anthropic
from markitdown import MarkItDown

client = anthropic.Anthropic()

md = MarkItDown(
    llm_client=client,
    llm_model="claude-sonnet-4-20250514"
)

# Görsel içerikleri açıklamaya dönüştürür
result = md.convert("diyagram.png")
print(result.text_content)
```

---

## 6. Toplu Dönüşüm

```python
from markitdown import MarkItDown
from pathlib import Path

def batch_convert(input_dir: str, output_dir: str) -> None:
    md = MarkItDown()
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    extensions = ['.docx', '.xlsx', '.pptx', '.pdf']
    errors = []

    for ext in extensions:
        for file in input_path.glob(f'*{ext}'):
            try:
                result = md.convert(str(file))
                out_file = output_path / f"{file.stem}.md"
                out_file.write_text(result.text_content, encoding='utf-8')
                print(f"✓ {file.name}")
            except Exception as e:
                errors.append((file.name, str(e)))
                print(f"✗ {file.name}: {e}")

    if errors:
        print(f"\n{len(errors)} hata oluştu:")
        for name, err in errors:
            print(f"  - {name}: {err}")


batch_convert('./belgeler', './markdown')
```

---

## 7. Metadata ile Arşivleme

```python
from datetime import datetime
from markitdown import MarkItDown
from pathlib import Path

def archive_with_metadata(doc_path: str, archive_dir: str) -> str:
    md = MarkItDown()
    result = md.convert(doc_path)

    filename = Path(doc_path).name
    output = f"""---
source: {filename}
converted: {datetime.now().strftime('%Y-%m-%d')}
---

{result.text_content}
"""

    out_path = Path(archive_dir) / Path(doc_path).stem
    out_path = out_path.with_suffix('.md')
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(output, encoding='utf-8')

    return str(out_path)
```

---

## 8. RAG / AI Corpus Oluşturma

```python
import json
from markitdown import MarkItDown
from pathlib import Path

def create_ai_corpus(doc_folder: str, output_file: str) -> list[dict]:
    md = MarkItDown()
    corpus = []

    for doc in Path(doc_folder).rglob('*'):
        if doc.suffix.lower() not in ['.docx', '.pdf', '.pptx', '.xlsx']:
            continue
        try:
            result = md.convert(str(doc))
            corpus.append({
                'source': str(doc),
                'filename': doc.name,
                'type': doc.suffix[1:],
                'content': result.text_content,
            })
        except Exception as e:
            print(f"Atlandı {doc.name}: {e}")

    Path(output_file).write_text(
        json.dumps(corpus, ensure_ascii=False, indent=2),
        encoding='utf-8'
    )
    print(f"{len(corpus)} belge corpus'a eklendi.")
    return corpus


create_ai_corpus('./sirket-belgeleri', './corpus.json')
```

---

## 9. Kısıtlamalar

Karmaşık biçimlendirme basitleştirilebilir. Görseller Markdown'a gömülmez (LLM ile açıklama alınabilir). Bazı tablo yapıları mükemmel dönüşmeyebilir. Word'deki izlenen değişiklikler ve yorumlar korunmaz.

---

## 10. Best Practices

Dönüştürülen Markdown'ı kaynak belgesiyle karşılaştırarak kalite kontrol yap. Önemli görseller için LLM entegrasyonunu aktif et. Büyük toplu işlemler için try-except ile hata toleransı ekle. Arşivlenen belgelere kaynak ve tarih metadata'sı ekle. Dönüştürülmüş içerikleri Git ile versiyon kontrolüne al.
