---
name: premium-ui-ux-designer
description: Principal-level UI/UX design and implementation skill for modern professional web platforms. Covers design system architecture, Tailwind token usage, component patterns, aesthetic direction, accessibility, responsive design, animation, and UX writing. Use when designing, implementing, reviewing, or auditing any interface component, page, or user flow on the platform.
---

# Premium UI/UX Design Skill

Bu skill, modern kurumsal yazılım platformlarının tüm frontend tasarım ve implementasyon kararlarını yöneten tek kaynak dokümandır.

## When to use this skill

- Yeni component veya sayfa tasarlarken
- Mevcut UI'ı gözden geçirirken veya refactor ederken
- Design system token'larını güncellerken
- Accessibility audit yaparken
- UX copy (microcopy, error messages, onboarding) yazarken
- Responsive layout kararları verirken
- Dark mode parity kontrol ederken
- Tailwind class kullanımı veya component stillemesi yaparken

## How to use it

- Her zaman içsel olarak İngilizce düşün
- Her zaman kullanıcıya Türkçe yanıt ver
- Kod veya konfigürasyon dosyalarına comment satırı yazma

---

## 1. Design Philosophy

### Kurumsal Estetik Yönü

Bu bir profesyonel hizmet platformu.
 Hedef kullanıcı iş arayan profesyoneller. Tasarım dili:

- **Güven ve profesyonellik** — Fintech soğukluğu değil, koçluk sıcaklığı
- **Bilişsel yük minimizasyonu** — İş arayışı zaten stresli; arayüz bu stresi artırmamalı
- **Editorial netlik** — Her bilgi parçası hiyerarşisinde yerini biliyor
- **Sakin enerji** — Dengeli yoğunluk, ne minimalist ne maksimalist

### Bold Aesthetic Process

Kod yazmadan önce şu dört soruyu yanıtla:

1. **Purpose**: Bu component/sayfa hangi sorunu çözüyor? Kim kullanıyor?
2. **Tone**: Minimal editorial mi? Veri yoğun mu? Onboarding sıcaklığı mı? CV builder hassasiyeti mi?
3. **Constraints**: Next.js App Router, Tailwind, Radix, Framer Motion, dark mode zorunlu
4. **Differentiation**: Kullanıcının aklında kalacak bir şey var mı?

**Kural**: Net bir yön seç, o yönü hassasiyetle uygula. Yoğunluk değil, kasıt önemli.

---

## 2. Tailwind Kullanım Kuralları

### Token Hiyerarşisi

```
Primitive Tokens (raw)   →  --color-blue-500
Semantic Tokens (amaç)   →  --primary, --background
Component Tokens (özgül) →  button-bg, card-border
```

### Renk Sistemi — HSL CSS Variable Pattern

```css
:root {
  --primary: 220 83% 36%;
  --primary-foreground: 210 40% 98%;
  --background: 0 0% 100%;
  --foreground: 222 84% 5%;
  --muted: 210 40% 96%;
  --muted-foreground: 215 16% 47%;
  --border: 214 32% 91%;
  --ring: 220 83% 36%;
  --destructive: 0 84% 60%;
  --warning: 38 92% 50%;
  --success: 142 76% 36%;
}

.dark {
  --primary: 220 70% 60%;
  --background: 222 84% 5%;
  --foreground: 210 40% 98%;
  --muted: 217 33% 17%;
  --muted-foreground: 215 20% 65%;
  --border: 217 33% 17%;
}
```

### Tailwind Kuralları (Zorunlu)

```typescript
// ✅ Semantic token kullan
<div className='bg-background text-foreground border-border'>
<button className='bg-primary text-primary-foreground hover:bg-primary/90'>
<span className='text-muted-foreground'>

// ❌ Ham primitive kullanma
<div className='bg-white text-gray-900 border-gray-200'>
<button className='bg-blue-600 text-white'>
```

**Kuralllar**:

- Hardcoded renk değerleri yasak (`text-blue-500`, `bg-gray-900`)
- `tailwind.config.mjs`'teki token'ların dışına çıkma
- Dark mode her token için otomatik — CSS variable sayesinde
- Arbitrary value (`w-[347px]`) — yalnızca `width` ve `height` için kabul edilir
- Design system component'lerine `className` override'ı — yalnızca `h-*` ve `w-*`

### Mevcut Custom Token'lar

```typescript
// tailwind.config.mjs'te tanımlı — kullan, değiştirme
animation: {
  'fade-in':      'fade-in 0.3s ease-out',
  'slide-in':     'slide-in 0.3s ease-out',
  'slide-up':     'slide-up 0.3s ease-out',
  'scale-in':     'scale-in 0.2s ease-out',
  shimmer:        'shimmer 2s infinite',
  'pulse-subtle': 'pulse-subtle 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
}

boxShadow: {
  primary:       '0 4px 6px -1px hsl(220 83% 36% / 0.12)...',
  'primary-glow': '0 0 0 3px hsl(220 83% 36% / 0.2)',
  editorial:     '0 1px 3px rgb(0 0 0 / 0.06)',
}
```

### Typography

```typescript
fontFamily: {
  display: ['var(--font-body)', 'sans-serif'],
  heading: ['var(--font-heading)', 'serif'],
  body:    ['var(--font-body)', 'sans-serif'],
}
```

**Kesinlikle kullanma**: Arial, Inter, Roboto, system-ui, Space Grotesk — layout.tsx'te inject edilen font variable'larını kullan.

---

## 3. Component Architecture

### CVA (Class Variance Authority) Pattern

Tüm variant'lı component'ler CVA ile yazılmalı:

```typescript
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '@/lib/utils'

const buttonVariants = cva(
  'inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50',
  {
    variants: {
      variant: {
        default: 'bg-primary text-primary-foreground hover:bg-primary/90',
        destructive: 'bg-destructive text-destructive-foreground hover:bg-destructive/90',
        outline: 'border border-input bg-background hover:bg-accent hover:text-accent-foreground',
        secondary: 'bg-secondary text-secondary-foreground hover:bg-secondary/80',
        ghost: 'hover:bg-accent hover:text-accent-foreground',
        link: 'text-primary underline-offset-4 hover:underline',
      },
      size: {
        sm: 'h-9 rounded-md px-3',
        default: 'h-10 px-4 py-2',
        lg: 'h-11 rounded-md px-8',
        icon: 'h-10 w-10',
      },
    },
    defaultVariants: { variant: 'default', size: 'default' },
  },
)
```

### Compound Component + forwardRef

```typescript
const Card = forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn('rounded-lg border bg-card text-card-foreground shadow-sm', className)} {...props} />
  )
)
Card.displayName = 'Card'
```

### Polymorphic Components (asChild)

```typescript
<Dialog.Trigger asChild>
  <Button variant='outline'>Aç</Button>
</Dialog.Trigger>
```

`asChild` — nested button/link accessibility sorunlarını önler. Her zaman kullan.

---

## 4. Radix UI Kullanım Kuralları

Proje: `dialog, dropdown-menu, select, tabs, tooltip, popover, checkbox, switch, slider, progress, scroll-area`

### Her Radix Component İçin Zorunlular

- `Dialog.Title` + `Dialog.Description` — screen reader zorunluluğu
- `Portal` — overflow container sorunlarını önler
- `forceMount + AnimatePresence` — Framer Motion için

### Framer Motion + Radix Animasyon

```typescript
import { motion, AnimatePresence } from 'framer-motion'
import * as Dialog from '@radix-ui/react-dialog'

<Dialog.Portal forceMount>
  <AnimatePresence>
    {open && (
      <Dialog.Content asChild>
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.95 }}
          transition={{ duration: 0.2, ease: 'easeOut' }}
        >
          {children}
        </motion.div>
      </Dialog.Content>
    )}
  </AnimatePresence>
</Dialog.Portal>
```

---

## 5. Responsive Design

### Breakpoint Stratejisi (Mobile-First)

```
Base:  < 640px   — Mobil
sm:    ≥ 640px   — Küçük tablet
md:    ≥ 768px   — Tablet
lg:    ≥ 1024px  — Laptop
xl:    ≥ 1280px  — Desktop
2xl:   ≥ 1400px  — Geniş ekran
```

### Container Query (Component-Level)

```css
.card-container {
  container-type: inline-size;
}

@container (min-width: 400px) {
  .card {
    display: grid;
    grid-template-columns: 200px 1fr;
  }
}
```

### Fluid Typography

```css
:root {
  --text-base: clamp(1rem, 0.9rem + 0.5vw, 1.125rem);
  --text-xl: clamp(1.25rem, 1rem + 1.25vw, 1.5rem);
  --text-4xl: clamp(2.25rem, 1.75rem + 2.5vw, 3.5rem);
}
```

### Kurallar

- Minimum touch target: 44×44px
- `100vh` yerine `100dvh` — mobil browser UI
- Yatay scroll olmayacak şekilde test et
- Mobilde minimum font-size 16px

---

## 6. Accessibility (WCAG AA Zorunlu)

### Kontrol Listesi

- [ ] Tüm interactive element'lerde visible focus state
- [ ] Minimum kontrast 4.5:1 (metin)
- [ ] Tam klavye navigasyonu
- [ ] Anlamlı image alt text
- [ ] Icon-only butonlarda `aria-label`
- [ ] Form input'larında explicit `<label>`
- [ ] Error state'lerde `aria-invalid` + `aria-describedby`
- [ ] Loading'de `aria-busy`
- [ ] `prefers-reduced-motion` desteği

### Focus Ring Utility

```typescript
export const focusRing = cn(
  'focus-visible:outline-none focus-visible:ring-2',
  'focus-visible:ring-ring focus-visible:ring-offset-2',
)
```

### Renk Tek Başına Anlam Taşımamalı

```typescript
// ✅ Renk + ikon + metin
<span className='text-destructive flex items-center gap-1' role='alert'>
  <AlertCircle size={16} aria-hidden='true' />
  Email adresi geçersiz
</span>
```

---

## 7. Motion & Animation

### Prensipler

- Sayfa yüklemesinde tek iyi koreografeli reveal, dağınık micro-interaction'lardan iyidir
- Sadece `transform` + `opacity` animasyonu — layout-affecting property değil
- Döngü süresi ≤ 2s
- `prefers-reduced-motion` her animasyonda korunmalı

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## 8. UX Writing (Microcopy)

### Dört Kalite Standardı

1. **Purposeful** — Kullanıcının hedefini gerçekleştirmeye yardım ediyor mu?
2. **Concise** — Anlam kaybolmadan en az kelime
3. **Conversational** — Doğal ve insancıl
4. **Clear** — Tek anlam, belirsizlik yok

### Buton/CTA Format

```
[Fiil] [Nesne]

✅ CV Oluştur / Analizi Başlat / Hesabı Sil
❌ Tamam / Gönder / Tıkla
```

### Error Message Pattern

```
[Ne başarısız oldu]. [Neden]. [Ne yapılmalı].

✅ "CV yüklenemedi. Dosya boyutu 5MB'ı aşıyor. Daha küçük bir dosya seçin."
❌ "Hata oluştu." / "Geçersiz giriş."
```

### Empty State Pattern

```
[Neden boş]. [Sonraki adım CTA].

✅ "Henüz kayıtlı CV yok. İlk CV'ni oluşturmak için buraya tıkla."
```

### Uzunluk Hedefleri

| Element       | Hedef        |
| ------------- | ------------ |
| Buton/CTA     | 2–4 kelime   |
| Sayfa başlığı | 3–6 kelime   |
| Error mesajı  | 12–18 kelime |
| Yönerge       | ≤ 20 kelime  |

### Türkçe Bağlam

- Türk iş pazarı varsayılanı
- ATS sistemleri ve İK beklentileri göz önünde
- "Sen" hitabı — formal ama sıcak ton
- İngilizce teknik terim zorunluysa açıkla

---

## 9. Anti-Patterns (ASLA)

### Görsel

- Generic fontlar (Inter, Roboto, Arial, Space Grotesk)
- Beyaz arka plan üzerine mor gradient
- Hardcoded renk (`text-blue-500` yerine `text-primary`)
- Solid renk default — atmosfer ve derinlik yarat
- Dark mode'u sonradan düşünme

### Teknik

- `asChild` olmadan nested button/link
- Accessibility feature'larını override etme
- `overflow: hidden` parent'ta Portal kullanmama
- Controlled + uncontrolled state karıştırma
- Component tokenları olmadan DS bileşeni override

### UX Writing

- Generic buton metni ("Tamam", "Gönder")
- Kullanıcıyı suçlayan error mesajı
- Recovery path olmayan error
- Renk tek başına anlam

---

## 10. Pre-Delivery Checklist

- [ ] Hover, focus, active state tüm interactive element'lerde var
- [ ] `cursor-pointer` tüm tıklanabilir element'lere uygulandı
- [ ] WCAG AA kontrast uyumu doğrulandı
- [ ] Klavye navigasyonu test edildi
- [ ] `prefers-reduced-motion` destekleniyor
- [ ] Tüm breakpoint'lerde test edildi (375, 768, 1024, 1440)
- [ ] Dark mode parity kontrol edildi, hydration flash yok
- [ ] Layout shift yok
- [ ] Error ve empty state'ler tasarlandı
- [ ] Loading state için skeleton/spinner var
- [ ] Yalnızca `tailwind.config.mjs`'teki token'lar kullanıldı
- [ ] Arbitrary Tailwind value yalnızca `h-*`/`w-*` için kullanıldı

---

## 11. Tailwind v4 Uyumluluk Notları

Proje şu an Tailwind CSS 3 kullanıyor. Tailwind v4'e geçildiğinde dikkat edilecekler:

### Spacing Değişikliği

```typescript
// ❌ v4'te kaldırıldı
<div className='flex space-x-4'>

// ✅ Her iki versiyonda çalışır
<div className='flex gap-4'>
```

`space-x-*` ve `space-y-*` şu an v3'te çalışıyor. Yeni yazılan kodda `gap-*` kullan — migration kolaylaşır.

### Config Yükleme (v4 farkı)

```css
/* v4'te tailwind.config.ts otomatik yüklenmez */
@import 'tailwindcss';
@config "../tailwind.config.ts";
```

### CSS Reset Çakışması

v4'te custom `* { margin: 0 }` reset'i ekleme — `mx-auto`, `my-*` utility'lerini bozar. Tailwind'in preflight'ına bırak.

### Distinctive Font Listesi (Anti-Generic)

Kullanılabilecek karakterli fontlar (Google Fonts):

| Kategori       | Fontlar                                      |
| -------------- | -------------------------------------------- |
| Editorial      | Playfair Display, Crimson Pro, Newsreader    |
| Technical      | IBM Plex Mono, IBM Plex Sans, Source Sans 3  |
| Modern         | Bricolage Grotesque, Syne, Plus Jakarta Sans |
| Code aesthetic | JetBrains Mono, Fira Code                    |
| Premium        | Cabinet Grotesk, Clash Display, Satoshi      |

**Kesinlikle kullanma**: Inter, Roboto, Open Sans, Lato, Arial, Space Grotesk (artık aşırı kullanılıyor)

### Renk Kontrast Kontrolü

```
Light mode metin: #0F172A (slate-900) veya #1E293B (slate-800)
Muted metin: #475569 (slate-600) minimum
Glass card: bg-white/80 veya üzeri — bg-white/10 karanlık modda görünmez
Border light: border-gray-200 — border-white/10 görünmez
```

---

## 12. Bileşen Tasarımı Öncesi Estetik Commit

Kod yazmadan önce şu dört soruyu yanıtla:

1. **Purpose**: Bu component/sayfa hangi sorunu çözüyor? Kim kullanıyor?
2. **Tone**: Editorial netlik mi? Veri yoğun mu? Onboarding sıcaklığı mı?
3. **Constraints**: Server/Client boundary, Radix primitifler, dark mode zorunlu
4. **Differentiation**: Kullanıcının aklında kalacak bir şey var mı?

### Tasarım Yönü Seçenekleri

| Bağlam      | Ton                  | Örnek                                    |
| ----------- | -------------------- | ---------------------------------------- |
| CV Builder  | Editorial hassasiyet | Temiz beyaz space, typographic hierarchy |
| ATS Analizi | Veri yoğun           | Renk kodlu skorlar, compact card grid    |
| AI Chat     | Konuşma sıcaklığı    | Bubble layout, yumuşak köşeler           |
| Onboarding  | Güven inşası         | Büyük typography, progress indicator     |
| Admin       | Utilitarian          | Dense table, compact spacing             |

### Spatial Composition Kuralları

```typescript
// Kompozisyon — unexpected layout yaratmak için
// Asimetri, overlap, diagonal flow, grid-breaking

// ❌ Generic — tam ortada, eşit padding, standard grid
<div className='grid grid-cols-3 gap-4 p-4'>

// ✅ Distinctive — editorial rhythm
<div className='grid grid-cols-[2fr_1fr] gap-x-12 gap-y-6 py-16 px-8'>
  <section className='-mt-8'>  {/* Vertical rhythm bozarak depth */}
```

### Arka Plan ve Atmosfer

```typescript
// ❌ Solid renk — flat, derinliksiz
<div className='bg-background'>

// ✅ Layered — gradient mesh veya subtle texture
<div
  className='relative bg-background'
  style={{
    backgroundImage: 'radial-gradient(at 40% 20%, hsl(220 83% 36% / 0.05) 0px, transparent 50%)',
  }}
>
```

### Motion Koreografisi

```typescript
// ❌ Her element ayrı ayrı dağınık animate
// ✅ Tek iyi koreografeli page load — staggered reveal

const stagger = {
  container: {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: { staggerChildren: 0.08 },
    },
  },
  item: {
    hidden: { opacity: 0, y: 16 },
    show: { opacity: 1, y: 0, transition: { duration: 0.4, ease: 'easeOut' } },
  },
}

<motion.div variants={stagger.container} initial='hidden' animate='show'>
  {items.map(item => (
    <motion.div key={item.id} variants={stagger.item}>
      <Card item={item} />
    </motion.div>
  ))}
</motion.div>
```

---

## 13. Anthropic Frontend Design — Distinctive Aesthetics

### Tasarım Öncesi Zorunlu Sorular

Her component veya sayfa başlamadan önce şu dört soruyu yanıtla:

1. **Purpose**: Bu arayüz hangi problemi çözüyor? Hedef kullanıcı kim?
2. **Tone**: Belirli bir uçtan seç — editorial minimalizm, maksimalist yoğunluk, retro-fütüristik, organik/doğal, lüks/rafine, oyunsu, endüstriyel, art deco geometrik, vb.
3. **Constraints**: Framework, performans, accessibility gereksinimleri
4. **Differentiation**: Bu tasarımı akılda kalıcı yapan TEK şey nedir?

**Temel kural**: Net bir yön seç ve hassasiyetle uygula. Kasıt yoğunluktan önemlidir.

### Asla Kullanılmayacak "Jenerik AI" Estetiği

```
❌ Inter, Roboto, Arial, Space Grotesk (fazla kullanıldı)
❌ Beyaz arka plan üzerine mor gradient
❌ Öngörülebilir card layout ve component pattern'ları
❌ Bağlamsız, jenerik renk şemaları
❌ Her nesilde aynı font ve renk tercihlerine yakınsamak
```

### Tipografi Seçimi

```
✅ Karakterli font çiftleri:
   - Editorial: Playfair Display + Crimson Pro
   - Teknik: IBM Plex Mono + IBM Plex Sans
   - Modern: Bricolage Grotesque + Syne
   - Premium: Cabinet Grotesk + Clash Display

❌ Jenerik: Inter, Roboto, Open Sans, Lato
```

### Renk ve Arka Plan Derinliği

```typescript
// ❌ Düz renk — derinliksiz
<div className='bg-background'>

// ✅ Layered atmosphere
<div
  className='relative bg-background'
  style={{
    backgroundImage: [
      'radial-gradient(at 40% 20%, hsl(220 83% 36% / 0.06) 0px, transparent 50%)',
      'radial-gradient(at 80% 80%, hsl(220 60% 20% / 0.04) 0px, transparent 50%)',
    ].join(', '),
  }}
>
```

### Spatial Composition (Beklenmedik Layout)

```typescript
// ❌ Simetrik, öngörülebilir grid
<div className='grid grid-cols-3 gap-4 p-8'>

// ✅ Editorial ritim — asimetri, depth
<div className='grid grid-cols-[2fr_1fr] gap-x-16 gap-y-4 py-20 px-10'>
  <section className='-mt-12'>   {/* Vertical offset — depth hissi */}
  <aside className='pt-16'>      {/* Staggered alignment */}
```

### Motion — Koreografili Reveal

```typescript
// ❌ Dağınık micro-interaction'lar her yerde
// ✅ Tek iyi koreografeli sayfa yüklemesi

const staggerVariants = {
  container: {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: { staggerChildren: 0.07, delayChildren: 0.1 },
    },
  },
  item: {
    hidden: { opacity: 0, y: 20 },
    show: { opacity: 1, y: 0, transition: { duration: 0.5, ease: [0.25, 0.1, 0.25, 1] } },
  },
}
```

### Profesyonel Platformlar için Ton Rehberi

| Sayfa       | Ton                     | Renk              | Font Tercihi              |
| ----------- | ----------------------- | ----------------- | ------------------------- |
| CV Builder  | Editorial hassasiyet    | Krem, koyu yeşil  | Serif display + sans body |
| ATS Analizi | Veri yoğun, profesyonel | Mavi, gri tonları | Monospace data + sans     |
| AI Chat     | Sıcak, konuşma hissi    | Yumuşak tonlar    | Yuvarlak sans             |
| Onboarding  | Güven inşası            | Primary palette   | Bold display + clean body |
| Admin Panel | Utilitarian, dense      | Muted, accent     | Compact sans              |
