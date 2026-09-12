---
name: api-design-skill
description: Master REST and GraphQL API design principles to build intuitive, scalable, and maintainable APIs. Use when designing new API endpoints, reviewing API specifications, establishing API standards, or migrating between API paradigms.
---

# API Design Skill

REST ve GraphQL API tasarım prensipleri referansı. Talent Architect'in Next.js Route Handler'ları ve AI servis endpoint'leri için de geçerlidir.

## When to use this skill

- Yeni API endpoint tasarlanırken
- Mevcut API'lar refactor edilirken
- API standartları belirlenmesi gerektiğinde
- REST → GraphQL veya tersi migration yapılırken

---

## 1. RESTful Tasarım Prensipleri

### Resource-Oriented Architecture

```
Resource'lar isim (noun), HTTP method'lar eylem (verb)
URL'ler hiyerarşiyi ifade eder
Tutarlı isimlendirme zorunlu
```

### HTTP Method Semantikleri

| Method   | Kullanım             | Idempotent |
| -------- | -------------------- | ---------- |
| `GET`    | Kaynak getir         | ✅         |
| `POST`   | Yeni kaynak oluştur  | ❌         |
| `PUT`    | Tüm kaynağı değiştir | ✅         |
| `PATCH`  | Kısmi güncelleme     | ✅         |
| `DELETE` | Kaynağı sil          | ✅         |

### Resource Naming

```http
GET    /api/users              # Koleksiyon listesi
POST   /api/users              # Oluştur
GET    /api/users/{id}         # Tekil kaynak
PUT    /api/users/{id}         # Tüm güncelleme
PATCH  /api/users/{id}         # Kısmi güncelleme
DELETE /api/users/{id}         # Sil

GET    /api/users/{id}/orders  # Nested resource
POST   /api/users/{id}/orders  # Nested create
```

**Yasak — Action-oriented endpoint'ler**:

```http
POST /api/createUser     ❌
POST /api/getUserById    ❌
POST /api/deleteUser     ❌
```

---

## 2. HTTP Status Kodları

```
200 OK              — Başarılı GET, PUT, PATCH
201 Created         — Başarılı POST
204 No Content      — Başarılı DELETE
400 Bad Request     — Geçersiz istek
401 Unauthorized    — Kimlik doğrulama gerekli
403 Forbidden       — Yetki yok
404 Not Found       — Kaynak bulunamadı
409 Conflict        — Çakışma (duplicate)
422 Unprocessable   — Validasyon hatası
429 Too Many Req.   — Rate limit
500 Internal Error  — Server hatası
```

---

## 3. Pagination

### Cursor-Based (Büyük Koleksiyonlar)

```typescript
// Yavaş — büyük offset'lerde performans düşer
GET /api/users?page=1&limit=20        // OFFSET tabanlı ❌

// Hızlı — cursor tabanlı
GET /api/users?cursor=eyJpZCI6MTAwfQ  // cursor tabanlı ✅
```

### Response Format

```typescript
interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  pageSize: number
  hasNext: boolean
  hasPrev: boolean
  nextCursor?: string // cursor-based için
}
```

### Filtering ve Sorting

```http
GET /api/users?status=active&sortBy=createdAt&order=desc
GET /api/orders?userId=123&minAmount=100&createdAfter=2024-01-01
```

---

## 4. Error Response Format

```typescript
interface ErrorResponse {
  error: string          // Machine-readable code
  message: string        // Human-readable Türkçe mesaj
  details?: Record<string, unknown>  // Ek bağlam
  timestamp: string
  path: string
}

// Örnek
{
  "error": "VALIDATION_ERROR",
  "message": "Email adresi geçersiz",
  "details": { "field": "email", "value": "notanemail" },
  "timestamp": "2025-03-22T10:30:00Z",
  "path": "/api/users"
}
```

**Asla yapma**: Stack trace veya SQL hatası client'a gönderme.

---

## 5. Next.js Route Handler Pattern (Talent Architect)

```typescript
// src/app/api/feature/route.ts
import { NextResponse } from 'next/server'
import { requireAuth } from '@/lib/server/auth'
import { z } from 'zod'

const schema = z.object({
  title: z.string().min(1).max(200),
})

export async function POST(request: Request) {
  try {
    const session = await requireAuth(request) // 1. Auth

    const raw = await request.json()
    const body = schema.parse(raw) // 2. Validation

    const result = await featureService(session.userId, body) // 3. Logic

    return NextResponse.json(result, { status: 201 }) // 4. Response
  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { error: 'VALIDATION_ERROR', message: 'Geçersiz veri', details: error.issues },
        { status: 422 },
      )
    }
    console.error('[POST /api/feature]', error)
    return NextResponse.json({ error: 'INTERNAL_ERROR', message: 'İşlem gerçekleştirilemedi' }, { status: 500 })
  }
}
```

---

## 6. GraphQL Tasarım Prensipleri

### Schema Tasarımı

```graphql
type User {
  id: ID!
  email: String!
  name: String!
  createdAt: DateTime!
  orders(first: Int = 20, after: String): OrderConnection!
}

type OrderConnection {
  edges: [OrderEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

type Query {
  user(id: ID!): User
  users(first: Int = 20, after: String, search: String): UserConnection!
}

type Mutation {
  createUser(input: CreateUserInput!): CreateUserPayload!
}

type CreateUserPayload {
  user: User
  errors: [FieldError!]
}

type FieldError {
  field: String
  message: String!
}
```

### N+1 Sorunu — DataLoader Pattern

```typescript
class UserOrdersLoader extends DataLoader<string, Order[]> {
  async batchLoadFn(userIds: string[]) {
    const orders = await db.orders.findMany({
      where: { userId: { in: userIds } },
    })
    const byUser = Object.groupBy(orders, (o) => o.userId)
    return userIds.map((id) => byUser[id] ?? [])
  }
}
```

---

## 7. API Versioning

```
URL Versioning (önerilen):
  /api/v1/users
  /api/v2/users

Header Versioning:
  Accept: application/vnd.api+json; version=1

Query Parameter:
  /api/users?version=1
```

**Talent Architect**: Şu an versioning yok. Yeni endpoint'lerde breaking change yaratma — yeni field ekle, eskiyi koru.

---

## 8. Rate Limiting

```typescript
// AI endpoint'leri için özellikle önemli
// lib/server/auth.ts veya middleware'de uygula

const LIMITS = {
  '/api/chat': { requests: 20, window: '1m' },
  '/api/cv/generate': { requests: 5, window: '10m' },
  '/api/ats/analyze': { requests: 10, window: '1h' },
}
```

Rate limit aşıldığında `429 Too Many Requests` döndür, `Retry-After` header'ı ekle.

---

## 9. Best Practices Özeti

**Yapılacaklar**:

- Tutarlı naming convention (çoğul isimler: `/users`, `/orders`)
- Uygun HTTP status kodları
- Pagination tüm koleksiyonlarda
- Input validation her endpoint'te (Zod)
- Error response format standart
- Rate limiting AI ve pahalı endpoint'lerde

**Yapılmayacaklar**:

- Fiil içeren URL'ler (`/createUser`, `/getOrder`)
- Stack trace client'a gönderme
- POST'u idempotent işlemler için kullanma
- Büyük koleksiyonlarda offset-based pagination
- Auth olmadan sensitive veri

---

## 10. API Tasarım Kontrol Listesi

- [ ] Resource isimleri isim, çoğul format
- [ ] HTTP method doğru seçildi
- [ ] Uygun status kodu döndürülüyor
- [ ] Input Zod ile validate ediliyor
- [ ] Auth kontrolü ilk satırda
- [ ] Error response standart format
- [ ] Büyük koleksiyonlarda pagination var
- [ ] Rate limiting uygulandı (AI endpoint'leri)
- [ ] Breaking change yok (mevcut field'lar korundu)

---

## 11. API Tasarım Anti-Pattern'ları

### Kesinlikle Yapılmaması Gerekenler

```
❌ Tüm endpoint'ler için varsayılan olarak REST seçmek
❌ REST endpoint URL'lerinde fiil kullanmak (/getUsers, /createOrder)
❌ Tutarsız response formatları döndürmek
❌ Internal hata detaylarını (stack trace, SQL) client'a göndermek
❌ Rate limiting uygulamadan public endpoint açmak
❌ Versiyonlama stratejisi belirlenmeden API yayımlamak
```

### API Tasarım Öncesi Kontrol Listesi

Bir API tasarlamadan önce yanıtlanması gereken sorular:

- [ ] API'yi kim tüketecek? (SDK, web app, mobile, third-party)
- [ ] Bu bağlam için doğru stil seçildi mi? (REST / GraphQL / tRPC)
- [ ] Tutarlı response formatı tanımlandı mı?
- [ ] Versiyonlama stratejisi belirlendi mi?
- [ ] Authentication ihtiyacı belirlendi mi?
- [ ] Rate limiting planlandı mı?
- [ ] Dokümantasyon yaklaşımı tanımlandı mı?

### API Stili Seçim Rehberi

```
TypeScript monorepo, tek ekip → tRPC (compile-time type safety)
Karmaşık veri ilişkileri, esnek sorgular → GraphQL
Standart CRUD, çoklu istemci → REST
Basit webhook veya integration → REST
```

---

## 12. API Versioning Stratejisi

### Temel Prensip: Expand-Contract Pattern

Her zaman en güncel formatta yaz, geriye dönük dönüşüm yap.

```
Kullanıcı V1.2 ← transformResponse ← Sunucu (V2.0 Latest)
Kullanıcı V1.2 → transformRequest  → Sunucu (V2.0 Latest)
```

**Response transforms**: Yeniden eskiye gider (new → old). Kullanıcı eski formatı bekler.
**Request transforms**: Eskiden yeniye gider (old → new). Handler güncel formatı bekler.

### Versioning Yöntemi Seçimi

```
URL Versioning (önerilen Next.js için):
  /api/v1/cv
  /api/v2/cv

Header Versioning:
  Accept: application/vnd.api+json; version=1

Query Parameter:
  /api/cv?version=1
```

### Response Dönüşümü (Next.js Route Handler)

```typescript
// lib/api-versioning.ts
type ApiVersion = 'v1' | 'v2'

function transformCvResponse(data: CvDocumentV2, version: ApiVersion) {
  if (version === 'v1') {
    return {
      ...data,
      // V1'de "score" yoktu, "atsResult" objesindeydi
      atsResult: { score: data.score, details: data.atsDetails },
      score: undefined,
    }
  }
  return data // V2: güncel format
}

// app/api/v1/cv/[id]/route.ts
export async function GET(request: Request, { params }: { params: { id: string } }) {
  const session = await requireAuth(request)
  const cv = await cvService.getById(params.id, session.userId)
  return NextResponse.json(transformCvResponse(cv, 'v1'))
}
```

### Breaking Change Tespiti

Breaking change kategorileri (mutlaka yeni versiyon gerektirir):

```
❌ Breaking:
- Field silme (score → kaldırıldı)
- Field yeniden adlandırma (userId → user_id)
- Tip değişikliği (string → number)
- Zorunlu yeni field ekleme

✅ Non-breaking (mevcut versiyonda güvenli):
- Yeni opsiyonel field ekleme
- Yeni endpoint ekleme
- Mevcut field'a yeni enum değeri ekleme
```

### Versiyon Geçiş Checklist

- [ ] Breaking change belirlendi ve belgelendi
- [ ] Eski versiyon için dönüşüm fonksiyonu yazıldı
- [ ] Deprecation notice eklendi (sunset tarihi ile)
- [ ] Changelog güncellendi
- [ ] Migration rehberi hazırlandı

---

## 13. API Entegrasyonu — Production Pattern'ları

### OAuth 2.0 Authorization Code Flow

```typescript
class OAuth2Client {
  constructor(
    private config: {
      clientId: string
      clientSecret: string
      redirectUri: string
      scopes: string[]
      authorizationUrl: string
      tokenUrl: string
    },
  ) {}

  getAuthorizationUrl(state: string): string {
    const params = new URLSearchParams({
      client_id: this.config.clientId,
      redirect_uri: this.config.redirectUri,
      scope: this.config.scopes.join(' '),
      response_type: 'code',
      state,
    })
    return `${this.config.authorizationUrl}?${params}`
  }

  async exchangeCode(code: string): Promise<{ accessToken: string; refreshToken: string }> {
    const response = await fetch(this.config.tokenUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({
        grant_type: 'authorization_code',
        code,
        redirect_uri: this.config.redirectUri,
        client_id: this.config.clientId,
        client_secret: this.config.clientSecret,
      }),
    })
    const data = await response.json()
    return { accessToken: data.access_token, refreshToken: data.refresh_token }
  }
}
```

### Retry with Exponential Backoff

```typescript
async function retryWithBackoff<T>(
  fn: () => Promise<T>,
  options: { maxRetries?: number; baseDelay?: number } = {},
): Promise<T> {
  const { maxRetries = 3, baseDelay = 1000 } = options

  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await fn()
    } catch (error) {
      const isLastAttempt = attempt === maxRetries - 1
      const isRetryable = error instanceof ApiError && error.statusCode >= 500

      if (isLastAttempt || !isRetryable) throw error

      const delay = baseDelay * Math.pow(2, attempt) // 1s, 2s, 4s
      await new Promise((resolve) => setTimeout(resolve, delay))
    }
  }
  throw new Error('Max retries exceeded') // TypeScript exhaustiveness
}
```

### Client-Side Rate Limiter

```typescript
class RateLimiter {
  private requests: number[] = []

  constructor(
    private maxRequests: number,
    private windowMs: number
  ) {}

  async acquire(): Promise<void> {
    const now = Date.now()
    this.requests = this.requests.filter(t => now - t < this.windowMs)

    if (this.requests.length >= this.maxRequests) {
      const waitTime = this.windowMs - (now - this.requests[0]!)
      await new Promise(resolve => setTimeout(resolve, waitTime))
      return this.acquire()
    }

    this.requests.push(now)
  }
}

// AI endpoint'leri için kullanım
const aiLimiter = new RateLimiter(10, 60_000)  // 10 istek/dakika

async function callAI(prompt: string) {
  await aiLimiter.acquire()
  return anthropic.messages.create({ ... })
}
```

### Webhook Signature Doğrulama

```typescript
// Stripe, GitHub, vb. webhook'lar için
function verifyWebhookSignature(payload: string, signature: string, secret: string): boolean {
  const expected = crypto.createHmac('sha256', secret).update(payload).digest('hex')

  // Timing-safe compare — timing attack önleme
  return crypto.timingSafeEqual(Buffer.from(signature), Buffer.from(expected))
}

// Next.js route handler
export async function POST(request: Request) {
  const payload = await request.text()
  const signature = request.headers.get('x-webhook-signature') ?? ''

  if (!verifyWebhookSignature(payload, signature, process.env.WEBHOOK_SECRET!)) {
    return NextResponse.json({ error: 'Invalid signature' }, { status: 401 })
  }

  const event = JSON.parse(payload)
  await handleWebhookEvent(event)
  return NextResponse.json({ received: true })
}
```
