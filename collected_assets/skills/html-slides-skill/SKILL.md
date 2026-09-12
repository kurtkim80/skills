---
name: html-slides-skill
description: Create interactive HTML presentations using reveal.js. Use when building slide decks, tech talks, product launch presentations, or any interactive HTML presentation. Generates self-contained HTML files with animations, code highlighting, speaker notes, and responsive layouts.
---

# HTML Slides Skill (reveal.js)

reveal.js ile interaktif, web tabanlı sunumlar oluşturma rehberi.

## When to use this skill

- Teknik sunum, konferans konuşması veya ürün lansmanı için slayt hazırlanırken
- Kod walthrough içeren sunum gerektiğinde
- Speaker notes ve zamanlayıcılı sunum istendiğinde
- Self-contained HTML sunum dosyası oluşturulacağında

---

## 1. Temel Yapı

```html
<!doctype html>
<html>
  <head>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4/dist/reveal.css " />
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4/dist/theme/black.css " />
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4/plugin/highlight/monokai.css " />
  </head>
  <body>
    <div class="reveal">
      <div class="slides">
        <section>Slayt 1</section>
        <section>Slayt 2</section>
      </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/reveal.js@4/dist/reveal.js "></script>
    <script src="https://cdn.jsdelivr.net/npm/reveal.js@4/plugin/highlight/highlight.js "></script>
    <script src="https://cdn.jsdelivr.net/npm/reveal.js@4/plugin/notes/notes.js "></script>
    <script>
      Reveal.initialize({
        hash: true,
        plugins: [RevealHighlight, RevealNotes],
      })
    </script>
  </body>
</html>
```

---

## 2. Slayt Yapıları

### Yatay ve Dikey Slaytlar

```html
<!-- Yatay slaytlar -->
<section>Slayt 1</section>
<section>Slayt 2</section>

<!-- Dikey slaytlar (nested) -->
<section>
  <section>Dikey 1</section>
  <section>Dikey 2</section>
</section>

<!-- Markdown slayt -->
<section data-markdown>
  <textarea data-template>
    ## Başlık
    - Madde 1
    - Madde 2
  </textarea>
</section>
```

### Tema Seçenekleri

`black`, `white`, `league`, `beige`, `sky`, `night`, `serif`, `simple`, `solarized`, `blood`, `moon`

```html
<link rel="stylesheet" href="reveal.js/dist/theme/moon.css" />
```

---

## 3. Animasyonlar (Fragments)

```html
<section>
  <p class="fragment">İlk görünen</p>
  <p class="fragment fade-in">Sonra bu</p>
  <p class="fragment fade-up">Sonra bu</p>
  <p class="fragment highlight-red">Vurgulanan</p>
</section>
```

Fragment stilleri: `fade-in`, `fade-out`, `fade-up`, `fade-down`, `fade-left`, `fade-right`, `highlight-red`, `highlight-blue`, `highlight-green`, `strike`

---

## 4. Kod Bloğu

```html
<section>
  <pre><code data-trim data-line-numbers="1|3-4">
const kullanici = {
  ad: 'Zafer',
  meslek: 'Geliştirici'
};
console.log(kullanici.ad);
  </code></pre>
</section>
```

---

## 5. Speaker Notes

```html
<section>
  <h2>Başlık</h2>
  <p>İçerik</p>
  <aside class="notes">Konuşmacı notları. 'S' tuşuyla görmek için.</aside>
</section>
```

---

## 6. Arka Plan Seçenekleri

```html
<!-- Renk arka planı -->
<section data-background-color="#4d7e65">
  <!-- Gradient arka planı -->
  <section data-background-gradient="linear-gradient(to bottom, #283b95, #17b2c3)">
    <!-- Görsel arka planı -->
    <section data-background-image="resim.jpg" data-background-size="cover">
      <!-- Video arka planı -->
      <section data-background-video="video.mp4"></section>
    </section>
  </section>
</section>
```

---

## 7. Konfigürasyon

```javascript
Reveal.initialize({
  controls: true,
  progress: true,
  slideNumber: true,
  hash: true,
  history: true,
  keyboard: true,
  overview: true,
  center: true,
  touch: true,
  transition: 'slide', // none, fade, slide, convex, concave, zoom
  transitionSpeed: 'default', // default, fast, slow
  autoSlide: 0, // 0 = devre dışı
  width: 960,
  height: 700,
  margin: 0.04,
  plugins: [RevealMarkdown, RevealHighlight, RevealNotes],
})
```

---

## 8. Hazır Örnek — Teknik Sunum

```html
<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>API Tasarımı</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4/dist/reveal.css " />
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4/dist/theme/night.css " />
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4/plugin/highlight/monokai.css " />
  </head>
  <body>
    <div class="reveal">
      <div class="slides">
        <section data-background-gradient="linear-gradient(to bottom right, #1a1a2e, #16213e)">
          <h1>API Tasarımı</h1>
          <h3>2025 En İyi Pratikler</h3>
          <p><small>Geliştirici Ekibi</small></p>
        </section>

        <section>
          <h2>Gündem</h2>
          <ol>
            <li class="fragment">RESTful Prensipler</li>
            <li class="fragment">Kimlik Doğrulama</li>
            <li class="fragment">Hata Yönetimi</li>
            <li class="fragment">Dokümantasyon</li>
          </ol>
        </section>

        <section>
          <section>
            <h2>RESTful Prensipler</h2>
          </section>
          <section>
            <h3>Resource Naming</h3>
            <pre><code data-trim class="language-http">
GET    /users           # Koleksiyon
GET    /users/123       # Tek kaynak
POST   /users          # Oluştur
PUT    /users/123       # Güncelle
DELETE /users/123      # Sil
          </code></pre>
          </section>
        </section>

        <section>
          <h2>Sorular?</h2>
          <p>api-ekibi@sirket.com</p>
          <aside class="notes">Sorular için 10 dakika ayırıldı.</aside>
        </section>
      </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/reveal.js@4/dist/reveal.js "></script>
    <script src="https://cdn.jsdelivr.net/npm/reveal.js@4/plugin/highlight/highlight.js "></script>
    <script src="https://cdn.jsdelivr.net/npm/reveal.js@4/plugin/notes/notes.js "></script>
    <script>
      Reveal.initialize({ hash: true, plugins: [RevealHighlight, RevealNotes] })
    </script>
  </body>
</html>
```

---

## 9. Auto-Animate

```html
<section data-auto-animate>
  <h2>Çözümümüz</h2>
  <div data-id="box" style="background: #3182ce; padding: 20px;">AI Destekli Otomasyon</div>
</section>

<section data-auto-animate>
  <h2>Çözümümüz</h2>
  <div data-id="box" style="background: #38a169; padding: 40px; width: 400px;">
    <p>AI Destekli Otomasyon</p>
    <p>%90 daha hızlı</p>
  </div>
</section>
```

---

## 10. Kaynaklar

- Resmi Dokümantasyon: https://revealjs.com/
- Demo: https://revealjs.com/demo/
- GitHub: https://github.com/hakimel/reveal.js
