---
name: nodejs-backend-skill
description: Build production-ready Node.js backend services with Express/Fastify — middleware patterns, authentication, database integration, caching, and API design. Use when creating REST APIs, microservices, or Node.js servers outside the Next.js App Router context.
---

# Node.js Backend Skill

Scalable, maintainable Node.js backend servisleri için production-ready pattern'lar.

**Not**: Next.js App Router route handler'ları için `talent-architect-senior-skill` kullan. Bu skill standalone Express/Fastify servisleri içindir.

## When to use this skill

- Standalone Node.js REST API oluştururken
- Express veya Fastify server kurulumunda
- Microservice mimarisi tasarlarken
- Node.js backend code review yaparken

---

## 1. Framework Seçimi

| Kriter            | Express    | Fastify  |
| ----------------- | ---------- | -------- |
| Ekosistem         | Çok zengin | Zengin   |
| Performans        | İyi        | Çok iyi  |
| TypeScript        | Plugin     | Native   |
| Schema validation | Manuel     | Yerleşik |
| Öğrenme eğrisi    | Düşük      | Orta     |

---

## 2. Express Kurulumu (TypeScript)

```typescript
import express, { Request, Response, NextFunction } from 'express'
import helmet from 'helmet'
import cors from 'cors'
import compression from 'compression'

const app = express()

app.use(helmet())
app.use(cors({ origin: process.env.ALLOWED_ORIGINS?.split(',') }))
app.use(compression())
app.use(express.json({ limit: '10mb' }))

app.listen(process.env.PORT || 3000, () => {
  console.log('Server ready')
})
```

---

## 3. Katmanlı Mimari

```
src/
├── controllers/    HTTP request/response
├── services/       İş mantığı
├── repositories/   Veri erişimi
├── middleware/     Auth, validation, logging
├── routes/         Route tanımları
└── utils/          Yardımcı fonksiyonlar
```

### Controller

```typescript
export class UserController {
  constructor(private userService: UserService) {}

  async createUser(req: Request, res: Response, next: NextFunction) {
    try {
      const user = await this.userService.createUser(req.body)
      res.status(201).json(user)
    } catch (error) {
      next(error)
    }
  }

  async getUser(req: Request, res: Response, next: NextFunction) {
    try {
      const user = await this.userService.getUserById(req.params.id)
      res.json(user)
    } catch (error) {
      next(error)
    }
  }
}
```

### Service

```typescript
export class UserService {
  constructor(private userRepository: UserRepository) {}

  async createUser(userData: CreateUserDTO): Promise<User> {
    const existing = await this.userRepository.findByEmail(userData.email)
    if (existing) throw new ValidationError('Email zaten kayıtlı')

    const hashed = await bcrypt.hash(userData.password, 10)
    const user = await this.userRepository.create({ ...userData, password: hashed })
    const { password, ...safe } = user
    return safe as User
  }
}
```

### Repository

```typescript
export class UserRepository {
  constructor(private db: Pool) {}

  async findById(id: string): Promise<UserEntity | null> {
    const { rows } = await this.db.query('SELECT * FROM users WHERE id = $1', [id])
    return rows[0] || null
  }

  async create(data: CreateUserDTO & { password: string }): Promise<UserEntity> {
    const { rows } = await this.db.query('INSERT INTO users (name, email, password) VALUES ($1, $2, $3) RETURNING *', [
      data.name,
      data.email,
      data.password,
    ])
    return rows[0]
  }
}
```

---

## 4. Middleware Pattern'ları

### JWT Authentication

```typescript
export const authenticate = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const token = req.headers.authorization?.replace('Bearer ', '')
    if (!token) throw new UnauthorizedError('Token bulunamadı')

    const payload = jwt.verify(token, process.env.JWT_SECRET!) as JWTPayload
    req.user = payload
    next()
  } catch {
    next(new UnauthorizedError('Geçersiz token'))
  }
}
```

### Validation (Zod)

```typescript
export const validate = (schema: AnyZodObject) => {
  return async (req: Request, res: Response, next: NextFunction) => {
    try {
      await schema.parseAsync({ body: req.body, query: req.query, params: req.params })
      next()
    } catch (error) {
      if (error instanceof ZodError) {
        next(new ValidationError('Validation hatası', error.errors))
      } else {
        next(error)
      }
    }
  }
}
```

### Rate Limiting

```typescript
import rateLimit from 'express-rate-limit'

export const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 dakika
  max: 100,
  message: 'Çok fazla istek',
  standardHeaders: true,
})

export const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5,
  skipSuccessfulRequests: true,
})
```

---

## 5. Custom Error Sınıfları

```typescript
export class AppError extends Error {
  constructor(
    public message: string,
    public statusCode: number = 500,
    public isOperational: boolean = true,
  ) {
    super(message)
    Error.captureStackTrace(this, this.constructor)
  }
}

export class ValidationError extends AppError {
  constructor(
    message: string,
    public errors?: any[],
  ) {
    super(message, 400)
  }
}

export class NotFoundError extends AppError {
  constructor(message = 'Bulunamadı') {
    super(message, 404)
  }
}

export class UnauthorizedError extends AppError {
  constructor(message = 'Yetkisiz erişim') {
    super(message, 401)
  }
}
```

### Global Error Handler

```typescript
export const errorHandler = (err: Error, req: Request, res: Response, next: NextFunction) => {
  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      error: err.message,
      ...(err instanceof ValidationError && { details: err.errors }),
    })
  }

  console.error('[Error]', err)
  res.status(500).json({
    error: process.env.NODE_ENV === 'production' ? 'İşlem gerçekleştirilemedi' : err.message,
  })
}
```

---

## 6. PostgreSQL Connection Pool

```typescript
import { Pool } from 'pg'

export const pool = new Pool({
  host: process.env.DB_HOST,
  port: parseInt(process.env.DB_PORT || '5432'),
  database: process.env.DB_NAME,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
})
```

### Transaction Pattern

```typescript
async function createOrder(userId: string, items: OrderItem[]) {
  const client = await pool.connect()
  try {
    await client.query('BEGIN')

    const { rows } = await client.query('INSERT INTO orders (user_id) VALUES ($1) RETURNING id', [userId])
    const orderId = rows[0].id

    for (const item of items) {
      await client.query('INSERT INTO order_items (order_id, product_id, qty) VALUES ($1, $2, $3)', [
        orderId,
        item.productId,
        item.qty,
      ])
    }

    await client.query('COMMIT')
    return orderId
  } catch (error) {
    await client.query('ROLLBACK')
    throw error
  } finally {
    client.release()
  }
}
```

---

## 7. Redis Cache

```typescript
import Redis from 'ioredis'

const redis = new Redis({ host: process.env.REDIS_HOST })

export class CacheService {
  async get<T>(key: string): Promise<T | null> {
    const data = await redis.get(key)
    return data ? JSON.parse(data) : null
  }

  async set(key: string, value: unknown, ttlSeconds?: number): Promise<void> {
    const serialized = JSON.stringify(value)
    if (ttlSeconds) {
      await redis.setex(key, ttlSeconds, serialized)
    } else {
      await redis.set(key, serialized)
    }
  }

  async delete(key: string): Promise<void> {
    await redis.del(key)
  }
}
```

---

## 8. JWT Auth Service

```typescript
export class AuthService {
  async login(email: string, password: string) {
    const user = await this.userRepository.findByEmail(email)
    if (!user || !(await bcrypt.compare(password, user.password))) {
      throw new UnauthorizedError('Geçersiz kimlik bilgileri')
    }

    return {
      token: jwt.sign({ userId: user.id }, process.env.JWT_SECRET!, { expiresIn: '15m' }),
      refreshToken: jwt.sign({ userId: user.id }, process.env.REFRESH_SECRET!, { expiresIn: '7d' }),
      user: { id: user.id, name: user.name, email: user.email },
    }
  }
}
```

---

## 9. API Response Format

```typescript
export class ApiResponse {
  static success<T>(res: Response, data: T, statusCode = 200) {
    return res.status(statusCode).json({ status: 'success', data })
  }

  static error(res: Response, message: string, statusCode = 500) {
    return res.status(statusCode).json({ status: 'error', message })
  }

  static paginated<T>(res: Response, data: T[], page: number, limit: number, total: number) {
    return res.json({
      status: 'success',
      data,
      pagination: { page, limit, total, pages: Math.ceil(total / limit) },
    })
  }
}
```

---

## 10. Best Practices

- `express-async-errors` veya `asyncHandler` wrapper kullan — try-catch tekrarını önle
- Her endpoint'te rate limiting uygula
- Sensitive veriyi log'a yazma (şifre, token, kart numarası)
- Production'da error stack trace gösterme
- Connection pool kullan — her request'te yeni bağlantı açma
- Graceful shutdown implement et (SIGTERM handler)
- Health check endpoint ekle (`/health`)

---

## 10. Framework Seçim Rehberi (2025)

### Deployment Hedefine Göre Karar Ağacı

```
Nereye deploy ediyorsunuz?
│
├── Edge/Serverless (Cloudflare Workers, Vercel Edge)
│   └── Hono — sıfır bağımlılık, ultra-hızlı cold start
│
├── Yüksek Performans API
│   └── Fastify — Express'ten 2-3x daha hızlı, TypeScript native
│
├── Enterprise / Büyük Ekip
│   └── NestJS — yapılandırılmış, DI container, decorator-based
│
├── Legacy / Maksimum Ekosistem
│   └── Express — olgun, en geniş middleware ekosistemi
│
└── Next.js ile Full-Stack
    └── Next.js API Routes veya tRPC
```

### Framework Karşılaştırma Tablosu

| Kriter            | Hono             | Fastify           | Express         | NestJS   |
| ----------------- | ---------------- | ----------------- | --------------- | -------- |
| Cold start        | En hızlı         | Hızlı             | Orta            | Yavaş    |
| TypeScript        | Native           | Mükemmel          | İyi             | Mükemmel |
| Ekosistem         | Büyüyor          | İyi               | En geniş        | Geniş    |
| Öğrenme eğrisi    | Düşük            | Orta              | Düşük           | Yüksek   |
| En iyi olduğu yer | Edge, serverless | Perf-critical API | Legacy, öğrenme | Kurumsal |

### Runtime Seçimi (2025)

```
Node.js 22+ — --experimental-strip-types ile .ts direkt çalışır
  → Genel amaç, en geniş ekosistem

Bun — Node.js uyumlu, built-in bundler, 3x daha hızlı
  → Performans kritik, yeni proje

Deno 2 — güvenlik-öncelikli, built-in TypeScript
  → Güvenlik kritik, edge deployment
```

### Native TypeScript (Node.js 22+)

```bash
# Build adımı olmadan .ts dosyasını direkt çalıştır
node --experimental-strip-types server.ts

# Basit script'ler ve API'lar için idealdir
# Karmaşık projeler için hâlâ tsup/esbuild önerilir
```

### Modül Sistemi Kararı

```
ESM (import/export) — yeni projeler için tercih
├── Modern standart, tree-shaking daha iyi
├── Top-level await desteği
└── package.json: "type": "module"

CommonJS (require) — mevcut codebase için
├── Daha geniş npm uyumluluğu
└── Bazı paketler henüz ESM desteklemiyor
```

### Async Pattern Seçimi

| Pattern              | Ne Zaman Kullan                                 |
| -------------------- | ----------------------------------------------- |
| `async/await`        | Sıralı async operasyonlar                       |
| `Promise.all`        | Bağımsız paralel operasyonlar                   |
| `Promise.allSettled` | Bazılarının başarısız olabileceği paralel işler |
| `Promise.race`       | Timeout veya ilk yanıt kazanır senaryosu        |

### CPU-Bound İş İçin Worker Threads

```typescript
// ❌ Event loop'u bloklar
app.get('/analyze', async (req, res) => {
  const result = heavyCpuComputation(data) // 5 saniye bloklar!
  res.json(result)
})

// ✅ Worker thread ile offload
import { Worker, isMainThread, parentPort } from 'worker_threads'

app.get('/analyze', async (req, res) => {
  const result = await runInWorker('./analysis-worker.js', data)
  res.json(result)
})
```

### Node.js Backend Anti-Pattern'ları

```
❌ Edge/serverless için Express seçmek → Hono kullan
❌ Production'da sync dosya okuma (fs.readFileSync) → async kullan
❌ Controller içine business logic koymak → Service layer'a taşı
❌ Input validation'ı atlamak → Zod ile her endpoint'te validate et
❌ Secret'ları hardcode etmek → Environment variable kullan
❌ CPU-bound işi async yapmak → worker_threads veya offload et
```
