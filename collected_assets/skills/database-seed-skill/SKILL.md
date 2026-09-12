---
name: database-seed-skill
description: Generate realistic test data and database seed scripts using Faker libraries. Use when populating development databases, creating test fixtures, generating demo data with relational integrity, or setting up automated database seeding workflows.
---

# Database Seed Skill

Faker kütüphaneleri ile gerçekçi test verisi ve veritabanı seed script'leri oluşturma rehberi.

## When to use this skill

- Geliştirme veritabanını gerçekçi veriyle doldurmak için
- Otomatik test fixture'ları oluşturmak için
- Demo uygulaması için örnek veri hazırlamak için
- CI/CD pipeline'ında database setup otomasyonu için

---

## 1. JavaScript/TypeScript — @faker-js/faker

### Kurulum

```bash
npm install --save-dev @faker-js/faker
```

### Temel Kullanım

```typescript
import { faker } from '@faker-js/faker'

// Tekil kayıt üret
const user = {
  id: faker.string.uuid(),
  name: faker.person.fullName(),
  email: faker.internet.email(),
  phone: faker.phone.number(),
  createdAt: faker.date.past({ years: 2 }),
}

// Çoklu kayıt (50 kullanıcı)
const users = Array.from({ length: 50 }, () => ({
  id: faker.string.uuid(),
  name: faker.person.fullName(),
  email: faker.internet.email(),
  role: faker.helpers.arrayElement(['admin', 'user', 'guest']),
  isActive: faker.datatype.boolean({ probability: 0.8 }),
  createdAt: faker.date.past({ years: 2 }),
}))
```

### Türkçe Veri

```typescript
import { faker, fakerTR } from '@faker-js/faker'

const turkishUser = {
  name: fakerTR.person.fullName(),
  city: fakerTR.location.city(),
  phone: fakerTR.phone.number('+90 5## ### ## ##'),
}
```

---

## 2. Relational Integrity (İlişkisel Bütünlük)

```typescript
import { faker } from '@faker-js/faker'

// Önce parent kayıtları oluştur
const users = Array.from({ length: 20 }, () => ({
  id: faker.string.uuid(),
  name: faker.person.fullName(),
  email: faker.internet.email(),
}))

// Sonra child kayıtları parent'a bağla
const departments = ['Engineering', 'Design', 'Marketing', 'Sales']
const employees = Array.from({ length: 100 }, () => ({
  id: faker.string.uuid(),
  userId: faker.helpers.arrayElement(users).id, // Mevcut user'a bağla
  department: faker.helpers.arrayElement(departments),
  salary: faker.number.int({ min: 50000, max: 200000 }),
  startDate: faker.date.past({ years: 5 }),
}))

// Orders → Users + Products ilişkisi
const orders = Array.from({ length: 200 }, () => {
  const user = faker.helpers.arrayElement(users)
  const itemCount = faker.number.int({ min: 1, max: 5 })
  return {
    id: faker.string.uuid(),
    userId: user.id,
    status: faker.helpers.arrayElement(['pending', 'processing', 'shipped', 'delivered']),
    total: faker.number.float({ min: 10, max: 500, fractionDigits: 2 }),
    createdAt: faker.date.past({ years: 1 }),
    items: Array.from({ length: itemCount }, () => ({
      productId: faker.string.uuid(),
      quantity: faker.number.int({ min: 1, max: 10 }),
      price: faker.number.float({ min: 5, max: 100, fractionDigits: 2 }),
    })),
  }
})
```

---

## 3. SQL Seed Script

```typescript
import { faker } from '@faker-js/faker'
import { writeFileSync } from 'fs'

function escapeStr(str: string): string {
  return str.replace(/'/g, "''")
}

const users = Array.from({ length: 50 }, () => ({
  id: faker.string.uuid(),
  name: faker.person.fullName(),
  email: faker.internet.email().toLowerCase(),
  createdAt: faker.date.past({ years: 2 }).toISOString(),
}))

const sql = `
-- Seed data generated ${new Date().toISOString()}
BEGIN;

TRUNCATE TABLE users RESTART IDENTITY CASCADE;

INSERT INTO users (id, name, email, created_at) VALUES
${users.map((u) => `  ('${u.id}', '${escapeStr(u.name)}', '${u.email}', '${u.createdAt}')`).join(',\n')};

COMMIT;
`

writeFileSync('seed.sql', sql)
console.log(`Generated ${users.length} users → seed.sql`)
```

---

## 4. Prisma Seed

```typescript
// prisma/seed.ts
import { PrismaClient } from '@prisma/client'
import { faker } from '@faker-js/faker'

const prisma = new PrismaClient()

async function main() {
  console.log('Seeding database...')

  // Kullanıcıları temizle ve yeniden oluştur
  await prisma.user.deleteMany()

  const users = await Promise.all(
    Array.from({ length: 30 }, () =>
      prisma.user.create({
        data: {
          name: faker.person.fullName(),
          email: faker.internet.email().toLowerCase(),
          role: faker.helpers.arrayElement(['ADMIN', 'USER']),
        },
      }),
    ),
  )

  // Her kullanıcı için 1-5 post oluştur
  for (const user of users) {
    const postCount = faker.number.int({ min: 1, max: 5 })
    await Promise.all(
      Array.from({ length: postCount }, () =>
        prisma.post.create({
          data: {
            title: faker.lorem.sentence(),
            content: faker.lorem.paragraphs(3),
            published: faker.datatype.boolean({ probability: 0.7 }),
            authorId: user.id,
          },
        }),
      ),
    )
  }

  console.log(`✅ Seeded ${users.length} users with posts`)
}

main()
  .catch(console.error)
  .finally(() => prisma.$disconnect())
```

```json
// package.json
{
  "prisma": {
    "seed": "ts-node --transpile-only prisma/seed.ts"
  }
}
```

```bash
npx prisma db seed
```

---

## 5. Firestore Seed (Talent Architect İçin)

```typescript
// scripts/seed-firestore.ts
import { initializeApp } from 'firebase/app'
import { getFirestore, collection, addDoc, writeBatch, doc } from 'firebase/firestore'
import { faker } from '@faker-js/faker'

const app = initializeApp({
  projectId: process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID,
  // diğer config...
})
const db = getFirestore(app)

async function seedCvs(userId: string, count: number = 5) {
  const batch = writeBatch(db)

  for (let i = 0; i < count; i++) {
    const cvRef = doc(collection(db, 'cvs'))
    batch.set(cvRef, {
      userId,
      title: `${faker.person.jobTitle()} CV`,
      summary: faker.lorem.paragraph(),
      skills: faker.helpers.arrayElements(['TypeScript', 'React', 'Node.js', 'Python', 'SQL', 'Docker', 'AWS'], {
        min: 3,
        max: 6,
      }),
      createdAt: faker.date.past({ years: 1 }),
      updatedAt: new Date(),
    })
  }

  await batch.commit()
  console.log(`✅ Seeded ${count} CVs for user ${userId}`)
}

// Çalıştır
seedCvs('test-user-id', 10)
```

---

## 6. Best Practices

```typescript
// 1. Seed verilerini deterministik yap (aynı seed = aynı veri)
faker.seed(12345)
const user = { name: faker.person.fullName() } // Her çalıştırmada aynı

// 2. Idempotent seed — birden fazla çalıştırılabilir
await prisma.user.upsert({
  where: { email: 'admin@example.com' },
  update: {},
  create: { email: 'admin@example.com', name: 'Admin' },
})

// 3. Environment check
if (process.env.NODE_ENV === 'production') {
  throw new Error('Seed script production ortamında çalışamaz!')
}

// 4. Batch işlem (büyük veri setleri için)
const BATCH_SIZE = 100
for (let i = 0; i < 1000; i += BATCH_SIZE) {
  const batch = Array.from({ length: BATCH_SIZE }, () => createUser())
  await db.users.createMany({ data: batch })
  console.log(`Progress: ${i + BATCH_SIZE}/1000`)
}
```

---

## 7. Yaygın Faker Kategorileri

| Kategori     | Örnekler                                         |
| ------------ | ------------------------------------------------ |
| **person**   | `fullName()`, `firstName()`, `jobTitle()`        |
| **internet** | `email()`, `url()`, `password()`, `userAgent()`  |
| **phone**    | `number()`                                       |
| **location** | `city()`, `country()`, `zipCode()`, `latitude()` |
| **lorem**    | `sentence()`, `paragraph()`, `words()`           |
| **date**     | `past()`, `future()`, `between()`, `recent()`    |
| **number**   | `int()`, `float()`, `binary()`                   |
| **string**   | `uuid()`, `alphanumeric()`, `nanoid()`           |
| **helpers**  | `arrayElement()`, `arrayElements()`, `shuffle()` |
| **datatype** | `boolean()`                                      |
| **image**    | `url()`, `avatar()`                              |
