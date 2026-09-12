---
name: markdown-to-html-skill
description: Convert Markdown files to HTML using marked.js, pandoc, gomarkdown, or static site generators (Jekyll, Hugo). Use when converting .md files to HTML, building static sites from Markdown, or implementing template systems that process Markdown content.
---

# Markdown to HTML Skill

Markdown dokümanlarını HTML'e dönüştürme — marked.js, pandoc, gomarkdown, Jekyll ve Hugo için kapsamlı rehber.

## When to use this skill

- `.md` dosyasını HTML'e dönüştürmek için
- Static site (Jekyll, Hugo) kurulumu veya template geliştirmek için
- Blog, dokümantasyon veya içerik sitesi oluştururken
- Custom markdown → HTML dönüştürme scripti yazarken

---

## 1. Temel Dönüşüm Referansı

```markdown
# Başlık 1 → <h1>Başlık 1</h1>

## Başlık 2 → <h2>Başlık 2</h2>

[link](https://x.com) → <a href="https://x.com ">link</a>
`kod` → <code>kod</code>
**kalın** → <strong>kalın</strong>
_italik_ → <em>italik</em>

- madde 1 → <ul><li>madde 1</li></ul>

1. madde 1 → <ol><li>madde 1</li></ol>
```

### Tablo

```markdown
| Ad  | Değer |
| --- | ----- |
| A   | 1     |
```

```html
<table>
  <thead>
    <tr>
      <th>Ad</th>
      <th>Değer</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>A</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
```

### Kod Bloğu

````markdown
```js
console.log('hello')
```
````

````

```html
<pre><code class="language-js">
console.log("hello");
</code></pre>
````

---

## 2. marked.js (Node.js)

### Kurulum

```bash
npm install -g marked      # CLI
npm install marked         # Programmatic
```

### CLI Kullanımı

```bash
# Dosya dönüştür
marked -i input.md -o output.html

# Standalone HTML (head/body dahil)
marked -i input.md -o output.html --gfm

# Config dosyasıyla
marked -i input.md -o output.html -c config.json
```

### CLI Seçenekleri

| Seçenek    | Açıklama                 |
| ---------- | ------------------------ |
| `-i`       | Input dosyası            |
| `-o`       | Output dosyası           |
| `--gfm`    | GitHub Flavored Markdown |
| `--breaks` | Newline → `<br>`         |

### Programmatic Kullanım

```javascript
const { marked } = require('marked')

const markdown = '# Merhaba\nBu **markdown**.'
const html = marked.parse(markdown)
console.log(html)
// <h1>Merhaba</h1><p>Bu <strong>markdown</strong>.</p>
```

### Güvenlik (Önemli)

marked.js HTML'i sanitize **etmez**. Güvenilmeyen input için:

```javascript
import { marked } from 'marked'
import DOMPurify from 'dompurify'

const unsafeHtml = marked.parse(untrustedMarkdown)
const safeHtml = DOMPurify.sanitize(unsafeHtml)
```

---

## 3. Pandoc

### Kurulum

https://pandoc.org/installing.html — OS'a göre indir

### Temel Kullanım

```bash
# Markdown → HTML
pandoc input.md -o output.html

# Standalone (head/body dahil)
pandoc input.md -s -o output.html

# Format belirterek
pandoc input.md -f markdown -t html -s -o output.html

# HTML → Markdown
pandoc -f html -t markdown input.html -o output.md

# Markdown → PDF (LaTeX gerekli)
pandoc input.md -s -o output.pdf

# Markdown → Word
pandoc input.md -s -o output.docx
```

### Pandoc Seçenekleri

| Seçenek     | Açıklama                            |
| ----------- | ----------------------------------- |
| `-f`        | Input format                        |
| `-t`        | Output format                       |
| `-s`        | Standalone (head/body)              |
| `--mathml`  | Math → MathML                       |
| `--toc`     | İçindekiler tablosu                 |
| `--sandbox` | Güvenli mod (dış dosya erişimi yok) |

---

## 4. Jekyll (Ruby Static Site)

### Kurulum

```bash
gem install jekyll bundler
jekyll new myblog
cd myblog
bundle exec jekyll serve
# http://localhost:4000
```

### Markdown Yapısı

```
_posts/
  2025-03-22-baslik.md     ← YYYY-MM-DD-slug.md formatı

_layouts/
  default.html             ← Ana layout

_includes/
  header.html

index.md                   ← Ana sayfa
```

### Post Yapısı

```markdown
---
layout: default
title: 'Yazı Başlığı'
date: 2025-03-22
tags: [react, nextjs]
---

# İçerik buraya
```

### Build ve Deploy

```bash
bundle exec jekyll build              # _site/ klasörü oluşturur
JEKYLL_ENV=production bundle exec jekyll build
bundle exec jekyll serve --livereload # Live reload ile geliştirme
```

### Config (\_config.yml)

```yaml
markdown: kramdown
kramdown:
  input: GFM
  syntax_highlighter: rouge

exclude:
  - Gemfile
  - Gemfile.lock
```

---

## 5. Hugo (Go Static Site)

### Kurulum

https://gohugo.io/installation/

```bash
hugo new site mysite
cd mysite
git init
git submodule add https://github.com/theNewDynamic/gohugo-theme-ananke  themes/ananke
echo "theme = 'ananke'" >> hugo.toml

hugo new content posts/ilk-yazi.md
hugo server -D   # Draft dahil
```

### İçerik Yapısı

```
content/
  posts/
    ilk-yazi.md

layouts/
  _default/
    single.html
    list.html
```

### Post Yapısı

```markdown
---
title: 'İlk Yazım'
date: 2025-03-22T10:00:00+03:00
draft: false
tags: ['react', 'nextjs']
---

İçerik buraya.
```

### Build Komutları

```bash
hugo                  # public/ klasörü oluşturur
hugo --minify         # Minified output
hugo server -D        # Draft dahil geliştirme sunucusu
```

### Hugo Config (hugo.toml)

```toml
[markup]
  [markup.goldmark]
    [markup.goldmark.renderer]
      unsafe = false  # Raw HTML için true yap
    [markup.goldmark.extensions]
      table = true
      strikethrough = true
      taskList = true
```

---

## 6. Karşılaştırma

| Araç       | Dil    | Hız       | Kullanım Kolaylığı |
| ---------- | ------ | --------- | ------------------ |
| marked.js  | JS     | Hızlı     | ⭐⭐⭐⭐⭐         |
| pandoc     | Binary | Orta      | ⭐⭐⭐⭐           |
| Jekyll     | Ruby   | Orta      | ⭐⭐⭐             |
| Hugo       | Go     | Çok hızlı | ⭐⭐⭐⭐           |
| gomarkdown | Go     | Çok hızlı | ⭐⭐⭐             |

**Öneri:**

- Hızlı dönüşüm scripti → marked.js
- Çok format desteği → pandoc
- Blog/içerik sitesi → Hugo (hız) veya Jekyll (ekosistem)

---

## 7. Sorun Giderme

| Sorun                   | Çözüm                                          |
| ----------------------- | ---------------------------------------------- |
| Tablo render olmuyor    | `gfm: true` / `table` extension aktif et       |
| Line break yok          | `breaks: true` seçeneği ekle                   |
| Raw HTML render olmuyor | Hugo: `unsafe = true`, marked: varsayılan açık |
| XSS riski               | DOMPurify ile sanitize et                      |
| Türkçe karakter sorunu  | UTF-8 encoding, `chcp 65001` (Windows)         |
