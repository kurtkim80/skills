---
name: stitch-ui-design-skill
description: Expert guide for creating effective prompts for Google Stitch AI UI design tool. Use when designing UI/UX prototypes in Stitch, generating app interfaces, or creating web/mobile design mockups with AI assistance. This is a standalone tool skill, not tied to Talent Architect stack.
---

# Google Stitch UI Design Skill

Google Stitch'te etkili prompt yazarak yüksek kaliteli UI tasarımları üretme rehberi.

## What is Google Stitch?

Google Labs tarafından Gemini 2.5 Flash ile güçlendirilen AI tabanlı UI tasarım aracı. Destekledikleri:

- Metin promptu → UI tasarımı
- Görsel (sketch, wireframe, screenshot) → UI
- Çoklu ekran uygulama akışları
- HTML/CSS, Figma ve kod export
- Annotate ile iteratif düzenleme

---

## 1. Temel Prompt Prensipleri

### Spesifik ve Detaylı Ol

```
❌ Zayıf: "Dashboard oluştur"

✅ Güçlü: "Üye dashboard'u — ders modülleri grid'i, ilerleme takip çubuğu,
community feed sidebar. Mor tema, kart tabanlı layout."
```

**Neden**: Komponent'leri (modüller, ilerleme, feed), layout'u (grid, sidebar), görsel stili (mor, kartlar) ve bağlamı (üye dashboard'u) belirt.

### Her Zaman Görsel Stil Tanımla

- Renk paleti (primary, accent)
- Tasarım stili (minimalist, modern, glassmorphic, playful)
- Yoğunluk (compact, spacious, balanced)

### Çok Ekranlı Akışları Bullet ile Listele

```
Fitness takip uygulaması:
- Hedef seçimli onboarding ekranı
- Günlük istatistik ve aktivite halkaları ile home dashboard
- Kategori filtreli egzersiz kütüphanesi
- Başarılar ve ayarlar ile profil ekranı
```

---

## 2. Prompt Şablonu

```
[Ekran/Komponent Tipi] — [Kullanıcı/Bağlam]

Ana Özellikler:
- [Özellik 1 — detaylı]
- [Özellik 2 — detaylı]
- [Özellik 3 — detaylı]

Görsel Stil:
- [Renk şeması]
- [Tasarım estetiği]
- [Layout yaklaşımı]

Platform: [Mobil / Web / Responsive]
```

**Örnek**:

```
SaaS analitik platformu admin dashboard'u

Ana Özellikler:
- MRR, aktif kullanıcı, churn oranı gösteren üst metrik kartları
- Son 30 gün gelir trendi için çizgi grafiği
- Kullanıcı aksiyonları ile son aktivite beslemesi
- Rapor ve export için hızlı aksiyon butonları

Görsel Stil:
- Dark mode, mavi/mor gradient aksan
- Modern glassmorphic kartlar, hafif gölgeler
- Erişilebilir renklerle temiz veri görselleştirme

Platform: Desktop web (1440px öncelikli)
```

---

## 3. Yaygın Kullanım Senaryoları

### Landing Page

```
[Ürün adı] için SaaS landing page

Bölümler:
- Başlık, alt başlık, CTA ve ürün ekranı ile hero
- Müşteri logoları ile sosyal kanıt
- İkonlu özellikler grid'i (3 sütun)
- Referanslar carousel
- Fiyatlandırma tablosu (3 katman)
- SSS accordion
- Bülten kaydı ile footer

Stil: Modern, profesyonel, güven inşa eden
Renkler: Navy mavi primary, açık mavi aksan
```

### Mobil Uygulama

```
Yemek teslimat uygulaması ana ekranı

Komponentler:
- Konum seçici ile arama çubuğu
- Kategori chipsleri (Pizza, Burger, Sushi vb.)
- Resim, ad, rating, teslimat süresi ve fiyat aralıklı restoran kartları
- Alt navigasyon (Ana Sayfa, Ara, Siparişler, Profil)

Stil: Canlı, iştah açıcı, kolay taranabilir
Platform: iOS mobil (375px)
```

### Form / Checkout

```
B2B platform çok adımlı kayıt formu

Adımlar:
1. Hesap bilgileri (şirket adı, email, şifre)
2. Şirket bilgileri (sektör, boyut, rol)
3. Takım kurulumu (üye davet)
4. Onay mesajlı doğrulama

Özellikler:
- Üstte ilerleme göstergesi
- Inline hatalar ile alan doğrulama
- İleri/Geri navigasyon
- 3. adım için atla seçeneği

Stil: Minimal, odaklı, düşük sürtünme
```

---

## 4. İterasyon Stratejileri

### Annotation ile Düzenleme

```
1. Prompttan başlangıç tasarımı oluştur
2. Değiştirilmesi gereken öğeleri annotate et
3. Değişikliği doğal dille açıkla
4. Stitch yalnızca annotated alanı günceller
```

### Variant Oluşturma

```
Bu hero section'ın 3 varyantını oluştur:
1. Minimal metinli görsel odaklı
2. Destekleyici grafikli metin ağırlıklı
3. Overlay içerikli video arka plan
```

### Aşamalı İyileştirme

```
İlk: "E-ticaret ana sayfası"
→ "Hover efektli 4 sütunlu ürünler bölümü ekle"
→ "Toprak tonları (terracotta, adaçayı, krem) ve üstte promosyon banner güncelle"
```

---

## 5. Design to Code İş Akışı

### Stitch → Figma → Kod

1. Stitch'te detaylı promptla UI oluştur
2. Figma'ya export et (design system entegrasyonu)
3. Design spec'leriyle geliştiriciye handoff
4. Production-ready kodla implement et

### Stitch → HTML → Framework

1. Stitch'te oluştur ve iyileştir
2. HTML/CSS kodunu export et
3. React/Vue component'lerine dönüştür
4. Uygulama codebase'ine entegre et

---

## 6. Kaçınılacaklar

```
❌ Zayıf: "Güzel bir web sitesi yap"
✅ Güçlü: Spesifik bölümler, renkler, hedef kitle

❌ Zayıf: "Login sayfası oluştur"
✅ Güçlü: "Sağlık portalı login — email/şifre, 'beni hatırla',
'şifremi unuttum', SSO seçenekleri (Google, Microsoft).
Mavi medikal tema, profesyonel ve güven verici."

❌ Görsel yön yok: "Görev yönetim uygulaması tasarla"
✅ Net yön: "Kanban board, drag-and-drop, öncelik etiketleri,
bitiş tarihi göstergeleri. Mor/teal gradient, dark mode desteği."
```

---

## 7. Etkili Kullanım İpuçları

1. **Referans görseller kullan** — Sketch, wireframe veya screenshot ekle
2. **Tasarım terminolojisi kullan** — "hero section", "card layout", "glassmorphic", "bento grid"
3. **Etkileşimleri belirt** — Hover state, tıklama aksiyonları, geçişler
4. **Component'ler halinde düşün** — Header, card, form parçalara ayır
5. **Küçük adımlarla iterate et** — Tam tasarım yerine odaklı değişiklikler
6. **Responsive test et** — Mobil, tablet, desktop breakpoint'leri kontrol et
7. **Accessibility belirt** — Kontrast, font boyutu, touch target

---

## 8. Export Sonrası Yapılacaklar

Stitch bir başlangıç noktasıdır, son ürün değil:

- [ ] Semantic HTML tag'lerini düzenle
- [ ] ARIA label ve alt text ekle
- [ ] Görselleri optimize et
- [ ] Animasyon ve micro-interaction ekle
- [ ] Production kod standartlarına refactor et
- [ ] Responsive breakpoint'leri doğrula
- [ ] Erişilebilirlik kontrol listesini tamamla
