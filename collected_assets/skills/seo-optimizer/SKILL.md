---
name: seo-optimizer
description: Search Engine Optimization specialist for Next.js and web projects. Covers keyword research, on-page SEO, technical SEO, schema markup, Core Web Vitals, and content strategy. Use when optimizing pages for search rankings, implementing meta tags, adding structured data, auditing SEO issues, or improving organic visibility.
---

# SEO Optimizer

Next.js ve genel web projeleri için kapsamlı SEO rehberi — içerik optimizasyonu, teknik SEO ve ölçüm stratejileri.

---

## 1. Keyword Araştırması ve Strateji

### Arama Niyeti Kategorileri

Her keyword dört niyetten birine hizmet eder. İçeriği buna göre yaz.

| Niyet          | Örnek                        | İçerik Tipi             |
| -------------- | ---------------------------- | ----------------------- |
| Bilgilendirici | "React hooks nedir"          | Rehber, makale          |
| Gezinme        | "Next.js docs"               | Landing page            |
| İşlemsel       | "CV oluşturma aracı indir"   | Ürün sayfası            |
| Ticari         | "En iyi ATS analiz araçları" | Karşılaştırma, inceleme |

### Keyword Optimizasyon Formülü

Primary keyword şu yerlerde geçmeli: başlık tag'i, H1, ilk paragrafın ilk 100 kelimesi, URL, meta description. Yoğunluk hedefi %1-2, doğal kullanım esas.

---

## 2. On-Page SEO

### Title Tag

```html
<!-- ✅ Anahtar kelime başta, 60 karakter altı, açıklayıcı -->
<title>CV Oluşturma Rehberi 2024 — Talent Architect</title>

<!-- ❌ Çok uzun, keyword stuffing, jenerik -->
<title>CV Oluştur CV Yap CV Hazırla CV Örneği CV Şablonu Online CV</title>
```

Next.js App Router'da:

```typescript
// app/cv-guide/page.tsx
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'CV Oluşturma Rehberi 2024 — Talent Architect',
  description:
    'ATS uyumlu profesyonel CV nasıl oluşturulur? Adım adım rehber, şablonlar ve uzman ipuçları. 10 dakikada etkileyici CV hazırlayın.',
}
```

### Meta Description

150-160 karakter, değer önerisi + CTA içermeli, her sayfada benzersiz olmalı.

```typescript
export const metadata: Metadata = {
  description:
    'ATS uyumlu profesyonel CV nasıl oluşturulur? Adım adım rehber, şablonlar ve uzman ipuçları. 10 dakikada etkileyici CV hazırlayın.',
  openGraph: {
    title: 'CV Oluşturma Rehberi',
    description: '...',
    images: [{ url: '/og/cv-guide.jpg', width: 1200, height: 630 }],
  },
}
```

### Heading Hiyerarşisi

```html
<h1>Ana Sayfa Başlığı (Primary Keyword)</h1>
<h2>Bölüm Başlığı (İlgili Keyword)</h2>
<h3>Alt Bölüm</h3>
<h3>Alt Bölüm</h3>
<h2>Başka Bölüm</h2>
```

Her sayfada yalnızca bir H1. H2/H3 başlıkları anlam taşımalı, dekoratif olmamalı.

### URL Yapısı

```
✅ /rehber/ats-uyumlu-cv-hazirlama
✅ /arac/cv-olusturucu
✅ /blog/is-basvurusu-ipuclari

❌ /page.php?id=123&ref=xyz
❌ /kategori-1/alt-kategori-2/item-999
```

### Görsel Optimizasyonu

```tsx
import Image from 'next/image'

// ✅ next/image — otomatik optimizasyon + CLS önleme
;<Image
  src='/images/cv-ornek.webp'
  alt='ATS uyumlu CV örneği — bölüm başlıkları ve anahtar kelimeler vurgulanmış'
  width={800}
  height={600}
  priority // Above-fold görseller için
/>
```

Alt text: bilgi içeren görseller için açıklayıcı, dekoratif görseller için `alt=""`.

---

## 3. Teknik SEO

### Schema Markup

```typescript
// app/blog/[slug]/page.tsx
export default function BlogPage({ post }: { post: BlogPost }) {
  const schema = {
    '@context': 'https://schema.org ',
    '@type': 'Article',
    headline: post.title,
    datePublished: post.publishedAt,
    dateModified: post.updatedAt,
    author: {
      '@type': 'Person',
      name: post.author.name,
    },
    publisher: {
      '@type': 'Organization',
      name: 'Talent Architect',
      logo: { '@type': 'ImageObject', url: 'https://example.com/logo.png ' },
    },
  }

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
      />
      {/* sayfa içeriği */}
    </>
  )
}
```

### Sık Kullanılan Schema Tipleri

`Article` — blog yazıları, `Product` — araçlar ve özellikler, `FAQ` — soru-cevap bölümleri, `HowTo` — adım adım rehberler, `BreadcrumbList` — navigasyon yolu, `Organization` — şirket bilgisi.

### Canonical Tag

```typescript
export const metadata: Metadata = {
  alternates: {
    canonical: 'https://example.com/orijinal-sayfa ',
  },
}
```

URL parametreleri olan sayfalar (filtreleme, sıralama) için özellikle önemli.

### Robots ve Sitemap (Next.js)

```typescript
// app/robots.ts
import type { MetadataRoute } from 'next'

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      { userAgent: '*', allow: '/' },
      { userAgent: '*', disallow: ['/admin/', '/api/', '/private/'] },
    ],
    sitemap: 'https://example.com/sitemap.xml ',
  }
}

// app/sitemap.ts
export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const posts = await fetchAllPosts()

  return [
    { url: 'https://example.com ', lastModified: new Date(), priority: 1.0 },
    ...posts.map((post) => ({
      url: `https://example.com/blog/ ${post.slug}`,
      lastModified: new Date(post.updatedAt),
      changeFrequency: 'monthly' as const,
      priority: 0.8,
    })),
  ]
}
```

---

## 4. Core Web Vitals

### Hedef Değerler

| Metrik                          | Hedef   | Ölçüm                   |
| ------------------------------- | ------- | ----------------------- |
| LCP (Largest Contentful Paint)  | < 2.5s  | En büyük içerik yükleme |
| INP (Interaction to Next Paint) | < 200ms | Etkileşim yanıt süresi  |
| CLS (Cumulative Layout Shift)   | < 0.1   | Layout kayması          |

### LCP İyileştirme

```tsx
// Hero görsel için priority ekle — preload tetikler
;<Image src='/hero.webp' alt='...' width={1200} height={600} priority />

// Kritik kaynakları preload et
// app/layout.tsx
export default function RootLayout() {
  return (
    <html>
      <head>
        <link rel='preload' href='/fonts/main.woff2' as='font' crossOrigin='' />
      </head>
    </html>
  )
}
```

### CLS Önleme

```tsx
// ✅ Her zaman width/height belirt — alan rezerve edilir
;<Image width={800} height={600} src='...' alt='...' />

// ✅ Skeleton ile layout rezervasyonu
{
  isLoading ? <Skeleton className='h-48 w-full' /> : <Content />
}

// ❌ Dinamik içerik mevcut içeriğin üstüne ekleme
// (banner, cookie notice, reklam — sayfa yüklendikten sonra ekleme)
```

### JavaScript Optimizasyonu (INP)

```typescript
// Ağır hesaplamayı defer et
const [isPending, startTransition] = useTransition()

startTransition(() => {
  setFilteredResults(heavyFilter(data))
})

// Büyük modülleri lazy load et
const HeavyChart = dynamic(() => import('./HeavyChart'), { ssr: false })
```

---

## 5. İçerik Stratejisi

### İçerik Uzunluğu Rehberi

| Sayfa Tipi           | Minimum      | Optimum     |
| -------------------- | ------------ | ----------- |
| Blog yazısı          | 1.000 kelime | 1.500-2.500 |
| Ürün/özellik sayfası | 300 kelime   | 500-800     |
| Kategori sayfası     | 500 kelime   | 800-1.200   |
| Ana sayfa            | 400 kelime   | 600+        |

### Featured Snippet İçin Optimizasyon

```markdown
## ATS Nedir?

ATS (Applicant Tracking System), işverenler tarafından iş başvurularını
otomatik olarak taramak ve filtrelemek için kullanılan yazılımdır.
Başvurular anahtar kelimeler, deneyim ve nitelikler bazında puanlanır.

## ATS Uyumlu CV Nasıl Hazırlanır?

1. İş ilanındaki anahtar kelimeleri CV'ye ekleyin
2. Standart bölüm başlıkları kullanın (Deneyim, Eğitim, Beceriler)
3. Sade format tercih edin — tablo ve grafik kullanmayın
4. PDF yerine DOCX formatında gönderin (belirtilmemişse)
```

### Dahili Linkleme Stratejisi

Her 1.000 kelime için 3-5 dahili link hedefle. Açıklayıcı anchor text kullan. "Buraya tıklayın" yerine "ATS analiz rehberi" gibi bağlamsal ifadeler seç. Eski içeriklere yeni içeriklerden link ver.

---

## 6. SEO Kontrol Listesi

Yayın öncesi kontrol:

- [ ] Primary keyword title tag'de (60 karakter altı)
- [ ] Meta description 150-160 karakter, CTA içeriyor
- [ ] H1 primary keyword içeriyor, sayfada yalnızca bir tane
- [ ] URL slug optimize ve okunabilir
- [ ] Görseller WebP formatında, açıklayıcı alt text içeriyor
- [ ] 3-5 dahili link mevcut
- [ ] Schema markup uygulandı (gerekiyorsa)
- [ ] Canonical tag doğru
- [ ] Mobil uyumlu
- [ ] Sayfa yükleme süresi < 3s
- [ ] Kırık link yok
- [ ] Open Graph ve Twitter Card meta tag'leri var

---

## 7. İzleme ve Analiz

Temel araçlar: Google Search Console (performans, indeksleme sorunları), Google Analytics 4 (trafik, dönüşüm), PageSpeed Insights (Core Web Vitals), Screaming Frog (teknik denetim).

İzlenecek temel metrikler: organik trafik trendi, keyword sıralamaları, tıklama oranı (CTR), hemen çıkma oranı, organik trafikten dönüşüm, Core Web Vitals puanları.
