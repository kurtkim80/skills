---
name: better-auth-skill
description: Integrate Better Auth — the comprehensive TypeScript-first authentication framework. Use when implementing authentication with Better Auth library, setting up OAuth, email/password, 2FA, passkeys, organizations, or migrating from other auth solutions. Note: Talent Architect uses Firebase Auth; this skill is for projects using Better Auth.
---

# Better Auth Skill

TypeScript-first, framework-agnostic authentication framework entegrasyon rehberi.

**Önemli**: Talent Architect Firebase Auth kullanıyor. Bu skill Better Auth kullanan **ayrı projeler** içindir.

Resmi dokümantasyon: https://better-auth.com/docs

---

## 1. Hızlı Başlangıç

### Kurulum

```bash
npm install better-auth
```

### Environment Variables

```bash
BETTER_AUTH_SECRET=min-32-karakter-secret  # openssl rand -base64 32
BETTER_AUTH_URL=https://example.com
```

Config'de yalnızca env var set edilmemişse `baseURL`/`secret` tanımla.

### CLI Komutları

```bash
npx @better-auth/cli@latest generate      # Prisma/Drizzle için schema üret
npx @better-auth/cli@latest migrate       # Schema uygula (built-in adapter)
```

**Plugin ekledikten sonra CLI'ı yeniden çalıştır.**

---

## 2. Temel Konfigürasyon

```typescript
// lib/auth.ts
import { betterAuth } from 'better-auth'
import { drizzleAdapter } from 'better-auth/adapters/drizzle'

export const auth = betterAuth({
  database: drizzleAdapter(db, { provider: 'pg' }),

  emailAndPassword: {
    enabled: true,
    autoSignIn: true,
    sendResetPassword: async ({ user, url }) => {
      await sendEmail({ to: user.email, subject: 'Şifre Sıfırlama', body: url })
    },
  },

  socialProviders: {
    github: {
      clientId: process.env.GITHUB_CLIENT_ID!,
      clientSecret: process.env.GITHUB_CLIENT_SECRET!,
    },
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    },
  },

  session: {
    expiresIn: 60 * 60 * 24 * 7, // 7 gün
    updateAge: 60 * 60 * 24, // 1 günde bir refresh
    cookieCache: {
      enabled: true,
      maxAge: 60 * 5, // 5 dakika
    },
  },

  plugins: [],
})
```

---

## 3. Feature Selection Matrix

| Özellik                | Plugin Gerekli   | Kullanım               |
| ---------------------- | ---------------- | ---------------------- |
| Email/Password         | Hayır (built-in) | Temel auth             |
| OAuth (GitHub, Google) | Hayır (built-in) | Social login           |
| Email Verification     | Hayır (built-in) | Email doğrulama        |
| Password Reset         | Hayır (built-in) | Şifre sıfırlama        |
| Two-Factor Auth (TOTP) | `twoFactor`      | Gelişmiş güvenlik      |
| Passkeys/WebAuthn      | `passkey`        | Passwordless           |
| Magic Link             | `magicLink`      | Email-based login      |
| Username Auth          | `username`       | Kullanıcı adı girişi   |
| Organizations          | `organization`   | Multi-tenant           |
| Rate Limiting          | Hayır (built-in) | Kötüye kullanım önleme |

---

## 4. Route Handler (Next.js)

```typescript
// app/api/auth/[...all]/route.ts
import { auth } from '@/lib/auth'
import { toNextJsHandler } from 'better-auth/next-js'

export const { GET, POST } = toNextJsHandler(auth)
```

---

## 5. Client Kullanımı

```typescript
// lib/auth-client.ts
import { createAuthClient } from 'better-auth/react'

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_APP_URL,
})

export const { signIn, signUp, signOut, useSession } = authClient
```

```typescript
// components/LoginButton.tsx
'use client'
import { authClient } from '@/lib/auth-client'

export function LoginButton() {
  const { data: session } = authClient.useSession()

  if (session) {
    return (
      <div>
        <span>{session.user.name}</span>
        <button onClick={() => authClient.signOut()}>Çıkış</button>
      </div>
    )
  }

  return (
    <div>
      <button onClick={() => authClient.signIn.social({ provider: 'google' })}>
        Google ile Giriş
      </button>
      <button onClick={() => authClient.signIn.social({ provider: 'github' })}>
        GitHub ile Giriş
      </button>
    </div>
  )
}
```

---

## 6. Session Yönetimi

### Storage Önceliği

1. `secondaryStorage` tanımlanmışsa → session oraya gider (DB değil)
2. `session.storeSessionInDatabase: true` → DB'ye de kaydet
3. DB yok + `cookieCache` → tamamen stateless

### Cookie Cache Stratejileri

| Strateji               | Açıklama         | Boyut        |
| ---------------------- | ---------------- | ------------ |
| `compact` (varsayılan) | Base64url + HMAC | En küçük     |
| `jwt`                  | Standard JWT     | Okunabilir   |
| `jwe`                  | Encrypted        | Max güvenlik |

---

## 7. Plugin Örnekleri

```typescript
// ✅ Tree-shaking için plugin-name yolu kullan
import { twoFactor } from 'better-auth/plugins/two-factor'
import { organization } from 'better-auth/plugins/organization'
import { admin } from 'better-auth/plugins/admin'
import { passkey } from 'better-auth/plugins/passkey'

export const auth = betterAuth({
  plugins: [twoFactor(), organization(), admin(), passkey()],
})
```

---

## 8. Database Hook'ları

```typescript
export const auth = betterAuth({
  databaseHooks: {
    user: {
      create: {
        before: async (user) => {
          return { data: { ...user, role: 'user' } }
        },
        after: async (user) => {
          await sendWelcomeEmail(user.email)
        },
      },
    },
  },
})
```

---

## 9. Middleware Protection (Next.js)

```typescript
// middleware.ts
import { auth } from '@/lib/auth'
import { NextRequest, NextResponse } from 'next/server'

export async function middleware(request: NextRequest) {
  const session = await auth.api.getSession({ headers: request.headers })

  if (!session && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/dashboard/:path*', '/api/protected/:path*'],
}
```

---

## 10. Type Safety

```typescript
// Server tarafında session tipi
type Session = typeof auth.$Infer.Session
type User = typeof auth.$Infer.Session.user

// Ayrı client/server projesi varsa
import { createAuthClient } from 'better-auth/react'
import type { auth } from './server/auth'

const authClient = createAuthClient<typeof auth>()
```

---

## 11. Implementation Checklist

- [ ] `better-auth` paketi kuruldu
- [ ] `BETTER_AUTH_SECRET` ve `BETTER_AUTH_URL` env var set edildi
- [ ] Auth server instance oluşturuldu (database config ile)
- [ ] Schema migration çalıştırıldı (`npx @better-auth/cli generate`)
- [ ] API handler mount edildi
- [ ] Client instance oluşturuldu
- [ ] Sign-up/sign-in UI implement edildi
- [ ] Session management component'lere eklendi
- [ ] Protected routes / middleware kuruldu
- [ ] Plugin'ler eklendi (ekleme sonrası schema yeniden üret)
- [ ] Email gönderimi yapılandırıldı (verification/reset)
- [ ] Rate limiting production için aktif

---

## 12. Yaygın Hatalar

1. **Model vs tablo adı**: Config ORM model adını kullanır, DB tablo adını değil
2. **Plugin schema**: Plugin eklendikten sonra CLI tekrar çalıştır
3. **Secondary storage**: Session varsayılan olarak oraya gider, DB'ye değil
4. **Cookie cache**: Custom session field'ları cache'lenmez, her zaman yeniden fetch
5. **Email doğrulama**: `sendVerificationEmail` tanımlanmadan çalışmaz
6. **Import path**: `better-auth/plugins` değil `better-auth/plugins/plugin-name` kullan

---

## 13. Kaynaklar

- Resmi Docs: https://better-auth.com/docs
- Options Reference: https://better-auth.com/docs/reference/options
- Plugins: https://better-auth.com/docs/plugins
- GitHub: https://github.com/better-auth/better-auth
