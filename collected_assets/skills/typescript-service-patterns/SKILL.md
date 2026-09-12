---
name: typescript-service-patterns
description: TypeScript service layer architecture with Result types, typed error definitions, and domain service patterns. Use when building service layers, defining domain errors, implementing error handling without exceptions, or creating testable business logic. Framework-agnostic — works with Next.js, Node.js, and any TypeScript project.
---

# TypeScript Service Layer Patterns

Tip-güvenli hata yönetimi ve domain servis mimarisi için production-ready pattern'lar. Framework'ten bağımsız — Next.js, Node.js ve TypeScript destekleyen her projede kullanılabilir.

---

## 1. Result Type Pattern

Exception fırlatmak yerine başarı veya hata durumunu explicit olarak döndür.

```typescript
type Result<T, E = Error> = { ok: true; value: T } | { ok: false; error: E }

const Ok = <T>(value: T): Result<T, never> => ({ ok: true, value })
const Err = <E>(error: E): Result<never, E> => ({ ok: false, error })
```

### Neden Result Type?

```typescript
// ❌ Exception tabanlı — hata durumu tip sisteminde görünmez
async function fetchUser(id: string): Promise<User> {
  const user = await db.findById(id)
  if (!user) throw new Error('Bulunamadı') // Caller bunu bilmez
  return user
}

// ✅ Result tabanlı — hata durumu imzada görünür
async function fetchUser(id: string): Promise<Result<User, 'NOT_FOUND' | 'DB_ERROR'>> {
  try {
    const user = await db.findById(id)
    if (!user) return Err('NOT_FOUND')
    return Ok(user)
  } catch {
    return Err('DB_ERROR')
  }
}

// Caller her iki durumu handle etmek zorunda
const result = await fetchUser('123')
if (!result.ok) {
  if (result.error === 'NOT_FOUND') redirect('/404')
  else showErrorToast('Bir hata oluştu')
  return
}
const user = result.value // Type-safe: User
```

### Async Result Helper

```typescript
async function tryAsync<T>(fn: () => Promise<T>): Promise<Result<T, Error>> {
  try {
    return Ok(await fn())
  } catch (err) {
    return Err(err instanceof Error ? err : new Error(String(err)))
  }
}

// Kullanım
const result = await tryAsync(() => db.cvs.findById(id))
```

---

## 2. Typed Error Definitions

Domain hatalarını string literal union ile tanımla — runtime overhead yok, compile-time güvenlik var.

### Basit Error Union

```typescript
type CvServiceError = 'CV_NOT_FOUND' | 'CV_TOO_LARGE' | 'INVALID_FORMAT' | 'STORAGE_FULL'

async function uploadCv(file: File, userId: string): Promise<Result<CvDocument, CvServiceError>> {
  if (file.size > MAX_SIZE) return Err('CV_TOO_LARGE')
  if (!VALID_FORMATS.includes(file.type)) return Err('INVALID_FORMAT')

  const result = await tryAsync(() => storageService.upload(file, userId))
  if (!result.ok) return Err('STORAGE_FULL')

  return Ok(result.value)
}
```

### Structured Error Objects

Ek bağlam taşıması gereken hatalar için:

```typescript
type CvError =
  | { code: 'NOT_FOUND'; cvId: string }
  | { code: 'TOO_LARGE'; sizeMb: number; limitMb: number }
  | { code: 'INVALID_FORMAT'; received: string; expected: string[] }
  | { code: 'UNAUTHORIZED'; userId: string }

async function getCv(cvId: string, requestingUserId: string): Promise<Result<CvDocument, CvError>> {
  const cv = await db.cvs.findById(cvId)

  if (!cv) return Err({ code: 'NOT_FOUND', cvId })
  if (cv.userId !== requestingUserId) {
    return Err({ code: 'UNAUTHORIZED', userId: requestingUserId })
  }

  return Ok(cv)
}

// Caller discriminated union ile handler yazar
const result = await getCv(cvId, userId)
if (!result.ok) {
  switch (result.error.code) {
    case 'NOT_FOUND':
      return NextResponse.json({ error: 'CV bulunamadı' }, { status: 404 })
    case 'UNAUTHORIZED':
      return NextResponse.json({ error: 'Yetkisiz erişim' }, { status: 403 })
    case 'TOO_LARGE':
      return NextResponse.json(
        {
          error: `Dosya boyutu ${result.error.sizeMb}MB, limit ${result.error.limitMb}MB`,
        },
        { status: 400 },
      )
  }
}
```

---

## 3. Service Layer Mimarisi

### Katmanlı Yapı

```
UI / API Route Layer
  ↓ HTTP request/response
Service Layer          ← Business logic burada
  ↓ Domain operations
Repository Layer       ← Data access burada
  ↓ Database queries
Database / External API
```

### Service Tanımı Kuralları

Servisler şunları YAPMAMALIDI:

- UI state veya toast notification import etmemeli
- HTTP request/response nesnesi bilmemeli
- Exception fırlatmak yerine Result döndürmeli
- Framework'e özgü bağımlılıklar içermemeli

```typescript
// ✅ Pure service — framework bağımsız, test edilebilir
export class CvAnalysisService {
  constructor(
    private readonly cvRepository: CvRepository,
    private readonly aiService: AiService,
  ) {}

  async analyzeAts(
    cvId: string,
    userId: string,
    jobDescription: string,
  ): Promise<Result<AtsAnalysis, 'CV_NOT_FOUND' | 'AI_ERROR' | 'UNAUTHORIZED'>> {
    const cvResult = await this.cvRepository.findById(cvId)
    if (!cvResult.ok) return Err('CV_NOT_FOUND')

    const cv = cvResult.value
    if (cv.userId !== userId) return Err('UNAUTHORIZED')

    const analysisResult = await this.aiService.analyzeAts(cv.content, jobDescription)
    if (!analysisResult.ok) return Err('AI_ERROR')

    return Ok(analysisResult.value)
  }
}
```

### API Route'ta Kullanım (Next.js)

```typescript
// app/api/cv/[id]/analyze/route.ts
export async function POST(request: Request, { params }: { params: Promise<{ id: string }> }) {
  const session = await requireAuth(request)
  const { id: cvId } = await params
  const { jobDescription } = await request.json()

  const service = new CvAnalysisService(cvRepository, aiService)
  const result = await service.analyzeAts(cvId, session.userId, jobDescription)

  if (!result.ok) {
    const statusMap = {
      CV_NOT_FOUND: 404,
      UNAUTHORIZED: 403,
      AI_ERROR: 500,
    } as const

    return NextResponse.json({ error: result.error }, { status: statusMap[result.error] })
  }

  return NextResponse.json(result.value)
}
```

---

## 4. Repository Pattern

```typescript
// Tip-güvenli repository interface
interface CvRepository {
  findById(id: string): Promise<Result<CvDocument, 'NOT_FOUND'>>
  findByUserId(userId: string): Promise<CvDocument[]>
  save(cv: CvDocument): Promise<Result<CvDocument, 'SAVE_ERROR'>>
  delete(id: string): Promise<Result<void, 'NOT_FOUND' | 'DELETE_ERROR'>>
}

// Firestore implementasyonu
class FirestoreCvRepository implements CvRepository {
  async findById(id: string): Promise<Result<CvDocument, 'NOT_FOUND'>> {
    const doc = await db.collection('cvs').doc(id).get()
    if (!doc.exists) return Err('NOT_FOUND')
    return Ok({ id: doc.id, ...doc.data() } as CvDocument)
  }

  async save(cv: CvDocument): Promise<Result<CvDocument, 'SAVE_ERROR'>> {
    return tryAsync(async () => {
      await db.collection('cvs').doc(cv.id).set(cv)
      return cv
    }).then((result) => (result.ok ? result : Err('SAVE_ERROR' as const)))
  }
}

// Test için mock implementasyonu
class MockCvRepository implements CvRepository {
  constructor(private cvs: Map<string, CvDocument> = new Map()) {}

  async findById(id: string): Promise<Result<CvDocument, 'NOT_FOUND'>> {
    const cv = this.cvs.get(id)
    return cv ? Ok(cv) : Err('NOT_FOUND')
  }
}
```

---

## 5. Test Edilebilirlik

```typescript
// Service test — gerçek DB veya AI yok
describe('CvAnalysisService', () => {
  it('unauthorized kullanıcıya UNAUTHORIZED döndürür', async () => {
    const mockCv = { id: 'cv-1', userId: 'user-1', content: '...' }
    const repository = new MockCvRepository(new Map([['cv-1', mockCv]]))
    const aiService = { analyzeAts: jest.fn() }

    const service = new CvAnalysisService(repository, aiService)
    const result = await service.analyzeAts('cv-1', 'user-2', 'job desc')

    expect(result.ok).toBe(false)
    expect(result.error).toBe('UNAUTHORIZED')
    expect(aiService.analyzeAts).not.toHaveBeenCalled()
  })
})
```

---

## 6. Best Practices Özeti

Exception fırlatmak yerine `Result<T, E>` döndür. Hata tiplerini string literal union olarak tanımla. Servisler UI bağımlılığı içermemeli. Repository interface'leri sayesinde test'te mock kullan. Her service metodu tek bir iş yapmalı. Bağımlılıkları constructor'dan enjekte et — `new Service()` yerine DI kullan.

```typescript
// ❌ Hataları swallow etme
try {
  await service.doSomething()
} catch {
  // sessizce görmezden gel
}

// ✅ Her zaman handle et
const result = await service.doSomething()
if (!result.ok) {
  logger.error('[ServiceName]', result.error)
  // uygun yanıt ver
}
```
