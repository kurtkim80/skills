---
name: sql-optimization-skill
description: Master SQL query optimization, indexing strategies, and EXPLAIN analysis to dramatically improve database performance. Use when debugging slow queries, designing database schemas, optimizing application response times, or working with large datasets. Also applicable to Firestore query optimization patterns.
---

# SQL Optimization Skill

Yavaş sorguları sistematik optimizasyon, doğru indexleme ve query plan analizi ile hızlı operasyonlara dönüştürme rehberi.

## When to use this skill

- Yavaş çalışan sorgular debug edilirken
- Veritabanı şeması tasarlanırken
- Uygulama response süresi optimize edilirken
- N+1 query sorunu çözülürken

---

## 1. EXPLAIN ile Query Plan Analizi (PostgreSQL)

```sql
-- Temel explain
EXPLAIN SELECT * FROM users WHERE email = 'user@example.com';

-- Gerçek istatistiklerle
EXPLAIN ANALYZE
SELECT * FROM users WHERE email = 'user@example.com';

-- Detaylı çıktı
EXPLAIN (ANALYZE, BUFFERS, VERBOSE)
SELECT u.*, o.order_total
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE u.created_at > NOW() - INTERVAL '30 days';
```

### İzlenecek Metrikler

| Metrik            | Açıklama                | Durum                 |
| ----------------- | ----------------------- | --------------------- |
| `Seq Scan`        | Tüm tablo taranıyor     | Büyük tablolarda kötü |
| `Index Scan`      | Index kullanıyor        | İyi                   |
| `Index Only Scan` | Sadece index, tablo yok | En iyi                |
| `Hash Join`       | Büyük veri seti join    | İyi                   |
| `Nested Loop`     | Küçük veri seti join    | İyi, büyükte kötü     |
| Cost              | Tahmini maliyet         | Düşük = iyi           |

---

## 2. Index Stratejileri

```sql
-- Standart B-Tree index
CREATE INDEX idx_users_email ON users(email);

-- Composite index (sıralama önemli!)
CREATE INDEX idx_orders_user_status ON orders(user_id, status);

-- Partial index (subset indexleme — çok verimli)
CREATE INDEX idx_active_users ON users(email)
WHERE status = 'active';

-- Expression index
CREATE INDEX idx_users_lower_email ON users(LOWER(email));

-- Covering index (ek kolonlar dahil)
CREATE INDEX idx_users_email_covering ON users(email)
INCLUDE (name, created_at);

-- Full-text search
CREATE INDEX idx_posts_search ON posts
USING GIN(to_tsvector('english', title || ' ' || body));

-- JSONB index
CREATE INDEX idx_metadata ON events USING GIN(metadata);
```

---

## 3. N+1 Query Sorunu

```python
# ❌ N+1 — Her kullanıcı için ayrı sorgu
users = db.query("SELECT * FROM users LIMIT 10")
for user in users:
    orders = db.query("SELECT * FROM orders WHERE user_id = ?", user.id)

# ✅ JOIN ile tek sorgu
SELECT u.id, u.name, o.id as order_id, o.total
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.id IN (1, 2, 3, 4, 5);

# ✅ Batch yükleme
user_ids = [u.id for u in users]
orders = db.query("SELECT * FROM orders WHERE user_id IN (?)", user_ids)
orders_by_user = {}
for order in orders:
    orders_by_user.setdefault(order.user_id, []).append(order)
```

---

## 4. Cursor-Based Pagination

```sql
-- ❌ OFFSET büyük tablolarda yavaş
SELECT * FROM users
ORDER BY created_at DESC
LIMIT 20 OFFSET 100000;  -- ÇOK YAVAŞ!

-- ✅ Cursor-based — her zaman hızlı
SELECT * FROM users
WHERE created_at < '2024-01-15 10:30:00'  -- Son cursor
ORDER BY created_at DESC
LIMIT 20;

-- Composite sorting için
SELECT * FROM users
WHERE (created_at, id) < ('2024-01-15 10:30:00', 12345)
ORDER BY created_at DESC, id DESC
LIMIT 20;

-- Gerekli index
CREATE INDEX idx_users_cursor ON users(created_at DESC, id DESC);
```

---

## 5. Temel Optimizasyon Kuralları

### SELECT \* Kullanma

```sql
-- ❌ Gereksiz kolon çekiyor
SELECT * FROM users WHERE id = 123;

-- ✅ Sadece gerekli kolonlar
SELECT id, email, name FROM users WHERE id = 123;
```

### WHERE Clause Optimizasyonu

```sql
-- ❌ Fonksiyon index kullanımını engeller
SELECT * FROM users WHERE LOWER(email) = 'user@example.com';

-- ✅ Expression index + aynı sorgu
CREATE INDEX idx_users_email_lower ON users(LOWER(email));
SELECT * FROM users WHERE LOWER(email) = 'user@example.com';

-- ✅ Normalize edilmiş veri ile direkt arama
SELECT * FROM users WHERE email = 'user@example.com';
```

### JOIN Optimizasyonu

```sql
-- ❌ Filter sonra join
SELECT u.name, o.total
FROM users u, orders o
WHERE u.id = o.user_id AND u.created_at > '2024-01-01';

-- ✅ Filter önce, sonra join
SELECT u.name, o.total
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE u.created_at > '2024-01-01';
```

---

## 6. Aggregate Optimizasyonu

```sql
-- ❌ Büyük tablolarda yavaş
SELECT COUNT(*) FROM orders;

-- ✅ Tahmini değer (istatistikler)
SELECT reltuples::bigint AS estimate
FROM pg_class
WHERE relname = 'orders';

-- ✅ Filtrelenmiş sayım + index
CREATE INDEX idx_orders_created ON orders(created_at);
SELECT COUNT(*) FROM orders
WHERE created_at > NOW() - INTERVAL '7 days';
```

---

## 7. Batch Operasyonlar

```sql
-- ❌ Tek tek insert
INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com');
INSERT INTO users (name, email) VALUES ('Bob', 'bob@example.com');

-- ✅ Toplu insert
INSERT INTO users (name, email) VALUES
  ('Alice', 'alice@example.com'),
  ('Bob', 'bob@example.com'),
  ('Carol', 'carol@example.com');

-- ✅ Çok büyük veri için COPY (PostgreSQL)
COPY users (name, email) FROM '/tmp/users.csv' CSV HEADER;

-- ✅ Toplu güncelleme
UPDATE users
SET status = 'active'
WHERE id IN (1, 2, 3, 4, 5);
```

---

## 8. Materialized View

```sql
-- Pahalı sorguyu önceden hesapla
CREATE MATERIALIZED VIEW user_order_summary AS
SELECT
  u.id,
  u.name,
  COUNT(o.id) as total_orders,
  SUM(o.total) as total_spent
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.name;

-- Index ekle
CREATE INDEX idx_user_summary ON user_order_summary(total_spent DESC);

-- Yenile
REFRESH MATERIALIZED VIEW CONCURRENTLY user_order_summary;

-- Çok hızlı sorgula
SELECT * FROM user_order_summary WHERE total_spent > 1000;
```

---

## 9. Yavaş Sorguları Bul

```sql
-- En yavaş sorgular (pg_stat_statements gerekli)
SELECT query, calls, total_time, mean_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;

-- Seq Scan yapan tablolar (index eksik?)
SELECT tablename, seq_scan, seq_tup_read, idx_scan
FROM pg_stat_user_tables
WHERE seq_scan > 0
ORDER BY seq_tup_read DESC
LIMIT 10;

-- Kullanılmayan indexler (sil bunları!)
SELECT schemaname, tablename, indexname, idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0
ORDER BY pg_relation_size(indexrelid) DESC;
```

---

## 10. Firestore Optimizasyon Notları (Talent Architect)

Firestore, SQL veritabanı değil ama benzer prensipler geçerli:

```typescript
// ❌ Tüm dökümanları çek, client'ta filtrele
const all = await db.collection('cvs').get()
const filtered = all.docs.filter((d) => d.data().userId === userId)

// ✅ Server-side filtrele
const filtered = await db.collection('cvs').where('userId', '==', userId).orderBy('createdAt', 'desc').limit(20).get()
```

```typescript
// Composite index gerektiren sorgular
// Firestore Console'da index oluştur
await db
  .collection('cvs')
  .where('userId', '==', userId)
  .where('status', '==', 'active') // Composite index gerekli
  .orderBy('createdAt', 'desc')
  .get()
```

**Firestore'da cursor-based pagination:**

```typescript
const first = await db.collection('cvs').where('userId', '==', userId).orderBy('createdAt', 'desc').limit(10).get()

const lastDoc = first.docs[first.docs.length - 1]

const next = await db
  .collection('cvs')
  .where('userId', '==', userId)
  .orderBy('createdAt', 'desc')
  .startAfter(lastDoc) // Cursor
  .limit(10)
  .get()
```

---

## 11. Yaygın Hatalar

- **Aşırı indexleme**: Her index INSERT/UPDATE/DELETE'i yavaşlatır
- **Index kullanılmıyor**: Sütunda fonksiyon çağrısı varsa (LOWER, UPPER)
- **OR koşulları**: Index kullanımını zorlaştırır — UNION kullan
- **Leading wildcard LIKE**: `LIKE '%abc'` index kullanamaz
- **Implicit type conversion**: `WHERE id = '123'` (string vs int) index bypass
