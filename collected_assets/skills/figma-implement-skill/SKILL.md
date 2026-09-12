---
name: figma-implement-skill
description: Translate Figma designs into production-ready code with 1:1 visual fidelity using the Figma MCP workflow. Use when given Figma URLs or node IDs, or asked to implement designs that must match Figma specs. Requires a working Figma MCP server connection.
---

# Figma Implement Skill

Figma tasarımlarını Figma MCP Server kullanarak pixel-perfect koda dönüştürme rehberi.

## When to use this skill

- Figma URL veya node ID verildiğinde
- "Bu Figma tasarımını implement et" denildiğinde
- Design-to-code fidelity kontrolü gerektiğinde

**Gereksinim**: Figma MCP Server bağlantısı aktif olmalı.

---

## 1. URL'den Node ID Çıkarma

```
https://figma.com/design/ :fileKey/:fileName?node-id=1-2

fileKey: URL'de /design/ sonrası segment
nodeId:  node-id parametresinin değeri (1-2)
```

**Örnek:**

```
https://figma.com/design/kL9xQn2VwM8pYrTb4ZcHjF/DesignSystem?node-id=42-15
→ fileKey: kL9xQn2VwM8pYrTb4ZcHjF
→ nodeId:  42-15
```

---

## 2. Zorunlu Adımlar (Sıra Değişmez)

### Adım 1 — Design Context Al

```
get_design_context(fileKey=":fileKey", nodeId="1-2")
```

Layout, typography, renk, spacing, component yapısı buradan gelir.

**Yanıt çok büyükse:**

```
get_metadata(fileKey=":fileKey", nodeId="1-2")
→ Child node'ları belirle
→ Her major bölüm için ayrı get_design_context çağrısı
```

### Adım 2 — Screenshot Al

```
get_screenshot(fileKey=":fileKey", nodeId="1-2")
```

Bu screenshot implementasyon süresince görsel referans olarak kullanılır.

### Adım 3 — Asset'leri İndir

- Figma MCP'nin döndürdüğü `localhost` URL'li asset'leri direkt kullan
- Yeni icon paketi ekleme — asset'ler Figma payload'dan gelir
- Placeholder kullanma — `localhost` source varsa onu kullan

### Adım 4 — Proje Convention'larına Çevir

Figma çıktısı (genellikle React + Tailwind) tasarımın temsilidir, final kod stili değil.

```
Yap:
✅ Proje token'larını kullan (semantic colors, spacing)
✅ Mevcut component'leri yeniden kullan
✅ Proje routing/state pattern'larını uygula

Yapma:
❌ Tailwind class'larını direkt kopyalama (proje farklı sistem kullanıyor olabilir)
❌ Hardcode renk — design token kullan
❌ Mevcut button/input/card component varken sıfırdan yazma
```

### Adım 5 — 1:1 Visual Parity Sağla

Teslim öncesi kontrol:

- [ ] Layout eşleşiyor (spacing, alignment, sizing)
- [ ] Typography eşleşiyor (font, boyut, weight, line-height)
- [ ] Renkler tam eşleşiyor
- [ ] Interactive state'ler çalışıyor (hover, active, disabled)
- [ ] Responsive davranış Figma constraint'lerine uyuyor
- [ ] Asset'ler doğru render ediliyor
- [ ] Accessibility standartları karşılanıyor

---

## 3. Yaygın Sorunlar

### Figma çıktısı truncated

```
→ get_metadata ile node yapısına bak
→ Her major bölüm için ayrı ayrı get_design_context çağır
```

### Tasarım eşleşmiyor

```
→ Step 2'deki screenshot ile karşılaştır
→ Design context'teki spacing/color/typography değerlerini kontrol et
```

### Asset yüklenmiyor

```
→ Figma MCP assets endpoint erişilebilir mi kontrol et
→ localhost URL'leri doğrudan kullan, değiştirme
```

### Design token farkı

```
→ Proje token'larını Figma değerleri yerine tercih et
→ Visual fidelity için spacing/sizing minimal ayarla
```

---

## 4. Desktop App ile Kullanım (figma-desktop MCP)

Figma desktop app açık ve node seçiliyse URL gerekmez:

```
get_design_context(nodeId="seçili-node-id")
```

Sadece `figma-desktop` MCP ile çalışır. Remote MCP URL gerektirir.

---

## 5. Prensip Özeti

```
Figma çıktısı = Tasarımın temsili
Proje kodu  = Uygulamanın gerçeği

Design system first:
→ Mevcut component varsa extend et, yeniden yazma
→ Proje token sistemi Figma değerlerinden önce gelir
→ Her sayfanın nasıl görüneceğini Figma söyler
→ Nasıl kodlanacağını proje convention'ı söyler
```
