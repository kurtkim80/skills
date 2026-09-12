---
name: kaizen-engineering-principles
description: Engineering excellence through continuous improvement, error-proofing by design, standardized work, and just-in-time development. Use when refactoring code, making architecture decisions, reviewing code quality, or discussing process improvements. Covers YAGNI, Poka-Yoke, incremental development, and anti-patterns to avoid.
---

# Kaizen Engineering Principles

Küçük, sürekli iyileştirmeler büyük değişimlerden daha etkilidir. Hataları önce tasarımda engelle, kanıtlanmış pattern'ları takip et ve yalnızca şu an gerekeni yap.

---

## 1. Sürekli İyileştirme (Kaizen)

### Temel Prensip

Büyük değişiklikler yerine küçük, sık iyileştirmeler yapılır. Her adım test edilir, onaylanır ve bir sonrakine geçilir.

```
İterasyon 1: Çalışır hale getir
İterasyon 2: Anlaşılır hale getir
İterasyon 3: Verimli hale getir
← Üçünü aynı anda yapmaya çalışma
```

### Uygulamada

```typescript
// İterasyon 1: Çalışan basit versiyon
const calculateTotal = (items: Item[]) => {
  let total = 0
  for (const item of items) {
    total += item.price * item.quantity
  }
  return total
}

// İterasyon 2: Anlaşılır hale getir
const calculateTotal = (items: Item[]): number => items.reduce((total, item) => total + item.price * item.quantity, 0)

// İterasyon 3: Sağlamlaştır (gerektiğinde)
const calculateTotal = (items: Item[]): number => {
  if (!items.length) return 0
  return items.reduce((total, item) => {
    if (item.price < 0 || item.quantity < 0) {
      throw new Error('Fiyat ve miktar negatif olamaz')
    }
    return total + item.price * item.quantity
  }, 0)
}
```

### Kod İncelerken

Her incelemede en yüksek etkili değişikliklerden başla. "Şu an yeterliden iyi" olan değişiklikleri kabul et — ilerleyen PR'larda iyileştirme yapılabilir.

Öncelik sırası: Kritik → Önemli → Güzel-olurdu

---

## 2. Poka-Yoke (Hata Önleme Tasarımı)

### Temel Prensip

Hataları runtime'da yakalamak yerine compile-time veya tasarım aşamasında imkânsız hale getir.

### Tip Sistemi ile Hata Önleme

```typescript
// ❌ String status — her değer geçerli
type OrderBad = { status: string }

// ✅ Yalnızca geçerli durumlar mümkün
type OrderStatus = 'pending' | 'processing' | 'shipped' | 'delivered'
type Order = { status: OrderStatus }

// ✅ En iyi: Durumla ilişkili veri
type Order =
  | { status: 'pending'; createdAt: Date }
  | { status: 'shipped'; trackingNumber: string; shippedAt: Date }
  | { status: 'delivered'; deliveredAt: Date }
// trackingNumber olmadan shipped durumu artık imkânsız
```

### Erken Validation (Sınırda Doğrulama)

```typescript
// ❌ Kullanımdan sonra doğrulama — geç kalındı
const processPayment = (amount: number) => {
  const fee = amount * 0.03 // Henüz validate edilmedi!
  if (amount <= 0) throw new Error('Geçersiz miktar')
}

// ✅ Sınırda doğrula, her yerde güvende kullan
type PositiveNumber = number & { readonly __brand: 'PositiveNumber' }

const validatePositive = (n: number): PositiveNumber => {
  if (n <= 0) throw new Error('Pozitif olmalı')
  return n as PositiveNumber
}

const processPayment = (amount: PositiveNumber) => {
  const fee = amount * 0.03 // Güvenli — tip garantisi var
}

// API sınırında bir kez doğrula
const handleRequest = (req: Request) => {
  const amount = validatePositive(req.body.amount)
  processPayment(amount) // Her yerde güvenle kullan
}
```

### Guard Clause ile Erken Dönüş

```typescript
// ❌ Derin iç içe geçmiş if — okunması zor
const processUser = (user: User | null) => {
  if (user) {
    if (user.email) {
      if (user.isActive) {
        sendEmail(user.email, 'Hoş geldin!')
      }
    }
  }
}

// ✅ Guard clause — erken dön, ana mantık temiz kalır
const processUser = (user: User | null) => {
  if (!user) return
  if (!user.email) return
  if (!user.isActive) return
  sendEmail(user.email, 'Hoş geldin!')
}
```

### Konfigürasyonu Başlangıçta Doğrula

```typescript
// ❌ Eksik config request sırasında fark edilir
const handler = async () => {
  const key = process.env.API_KEY // Eksikse burada hata
}

// ✅ Uygulama başlarken doğrula — geç teslim yok
const loadConfig = () => {
  const apiKey = process.env.API_KEY
  if (!apiKey) throw new Error('API_KEY zorunlu environment variable')
  return { apiKey }
}

const config = loadConfig() // Deploy sırasında hata → production'a geçemez
```

---

## 3. Standart İş (Standardized Work)

### Temel Prensip

Mevcut codebase pattern'larını takip et. Yeni pattern yalnızca anlamlı bir iyileştirme sunuyorsa ve ekip onayıyla benimsenir.

### Mevcut Pattern'ları Takip Et

```typescript
// Codebase'deki mevcut pattern
class UserAPIClient {
  async getUser(id: string): Promise<User> {
    return this.fetch(`/users/${id}`)
  }
}

// ✅ Yeni kod aynı pattern'ı takip eder
class OrderAPIClient {
  async getOrder(id: string): Promise<Order> {
    return this.fetch(`/orders/${id}`)
  }
}

// ❌ "Ben function tercih ederim" gerekçesiyle farklı pattern
const getOrder = async (id: string): Promise<Order> => { ... }
// → Tutarsızlık kafa karıştırır
```

### Hata Yönetimi Standardı

```typescript
// Proje standardı: Result type — tüm servisler bunu kullanır
type Result<T, E = Error> = { ok: true; value: T } | { ok: false; error: E }

const fetchCv = async (id: string): Promise<Result<CvDocument>> => {
  try {
    const cv = await db.cvs.findById(id)
    if (!cv) return { ok: false, error: new Error('CV bulunamadı') }
    return { ok: true, value: cv }
  } catch (err) {
    return { ok: false, error: err as Error }
  }
}

// Caller tutarlı pattern kullanır
const result = await fetchCv('123')
if (!result.ok) {
  logger.error('CV alınamadı', result.error)
  return
}
const cv = result.value // Type-safe!
```

### Import Organizasyonu (Standard)

```typescript
// Sıralama: external → internal → relative
import { z } from 'zod' // external
import { NextResponse } from 'next/server' // external framework
import { requireAuth } from '@/lib/server/auth' // internal absolute
import { CvDocument } from '../types' // relative
import type { Metadata } from 'next' // type-only
```

### Otomasyon ile Standardı Zorla

```bash
# Stil — otomatik uygulama
prettier --write .

# Tip kontrolü — CI'da zorunlu
tsc --noEmit

# Lint — standard ihlallerini yakala
eslint src --ext .ts,.tsx
```

---

## 4. Just-In-Time (JIT) — Sadece Gereken Kadar

### YAGNI Prensibi

"You Aren't Gonna Need It" — şu anki gereksinimler dışında kod yazma. "Belki ileride lazım olur" gerekçesiyle yapılan eklentiler teknik borç yaratır.

```typescript
// ❌ Spekülatif karmaşıklık
class Logger {
  private transports: LogTransport[] = []
  private queue: LogEntry[] = []
  private rateLimiter: RateLimiter
  // 200 satır — "belki ileride farklı transport gerekir" için
}

// ✅ Şu anki ihtiyacı karşıla
const logError = (error: Error) => {
  console.error(error.message)
}
// İhtiyaç ortaya çıktığında genişlet
```

### Rule of Three — Soyutlama Zamanı

```typescript
// 1. kullanım — direkt yaz
const filterActiveCvs = (cvs: CvDocument[]) => cvs.filter((cv) => cv.status === 'active')

// 2. kullanım — tekrar yaz (henüz soyutlama zamanı değil)
const filterActiveJobs = (jobs: Job[]) => jobs.filter((job) => job.status === 'active')

// 3. kullanım — pattern kanıtlandı, soyutla
const filterActive = <T extends { status: string }>(items: T[]) => items.filter((item) => item.status === 'active')
```

### Ölç, Sonra Optimize Et

```typescript
// Önce: Basit ve okunabilir
const getMatchingCvs = (cvs: CvDocument[], query: string) =>
  cvs.filter((cv) => cv.title.toLowerCase().includes(query.toLowerCase()))

// Benchmark: 10.000 CV için 12ms — kabul edilebilir
// → Ship et, optimizasyon yapma

// Sonra: Profiling ile darboğaz kanıtlandıktan sonra
const cvSearchIndex = new Map(cvs.map((cv) => [cv.id, cv.title.toLowerCase()]))
const getMatchingCvs = (query: string) => {
  const q = query.toLowerCase()
  return [...cvSearchIndex.entries()].filter(([, title]) => title.includes(q)).map(([id]) => cvMap.get(id)!)
}
```

### Erken Soyutlamadan Kaçın

```typescript
// ❌ Tek kullanım için generic framework
abstract class BaseCRUDService<T> {
  abstract getAll(): Promise<T[]>
  abstract getById(id: string): Promise<T>
  // 300 satır — tek tablo için
}

// ✅ Spesifik fonksiyonlar — pattern çıktığında soyutla
const getCvs = async (userId: string): Promise<CvDocument[]> => db.collection('cvs').where('userId', '==', userId).get()
```

---

## Kırmızı Bayraklar

### Sürekli İyileştirme İhlalleri

"Sonra düzeltirim" (genellikle gerçekleşmez), bulduğunuzdan daha kötü bırakmak, artımlı yerine büyük yeniden yazma tercih etmek.

### Poka-Yoke İhlalleri

"Kullanıcılar dikkatli olmalı" yaklaşımı, kullanımdan sonra validation, başlangıçta doğrulanmayan konfigürasyon.

### Standart İş İhlalleri

"Ben böyle yapmayı tercih ederim" gerekçesiyle mevcut pattern'lardan ayrılmak, proje konvansiyonlarını görmezden gelmek.

### JIT İhlalleri

"Belki ileride lazım olur", ölçülmeden optimizasyon, 3+ kullanım kanıtlanmadan soyutlama.

---

## Özet

**Kaizen şunu söyler**: Mükemmellik bir seferlik değil, sürekli küçük adımlarla gelir. Bugün yeterince iyi, yarın daha iyi.

**Pratikte**: Her PR'da kodu bulduğunuzdan biraz daha iyi bırakın. Hataları yakalamadan önce imkânsız hale getirin. Kanıtlanmış pattern'ları takip edin. Yalnızca gerçekten gereken şeyi inşa edin.
