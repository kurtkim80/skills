---
name: database-migrations-skill
description: SQL database migration strategies with zero-downtime deployment, rollback plans, and data integrity validation for PostgreSQL, MySQL, and SQL Server. Use when designing schema changes, adding columns/indexes, renaming tables, or planning production migrations with minimal downtime.
---

# Database Migrations Skill

Zero-downtime SQL database migration stratejileri — PostgreSQL, MySQL ve SQL Server için.

---

## 1. Temel İlkeler

Her production migration için şu dört soruyu yanıtla:

1. **Backward compatible mi?** — Eski kod yeni schema ile çalışabilir mi?
2. **Rollback planı var mı?** — Sorun çıkınca geri alınabilir mi?
3. **Büyük tablo mu?** — Lock süresi kaç saniye?
4. **Veri kaybı riski var mı?** — Hangi data validation yapılmalı?

---

## 2. Expand-Contract Pattern (Sıfır Downtime)

Büyük schema değişikliklerinin standart yaklaşımı üç aşamadan oluşur.

### Aşama 1 — Expand (Genişlet)

Yeni yapıyı ekle, eskisini koru:

```sql
-- Yeni kolonu NULL olarak ekle (lock minimal)
ALTER TABLE users ADD COLUMN display_name VARCHAR(255);

-- Mevcut veriyi backfill et (batch ile)
UPDATE users
SET display_name = full_name
WHERE display_name IS NULL
  AND id BETWEEN :start AND :end;
```

### Aşama 2 — Migrate (Uygulama Geçişi)

Uygulama kodunu yeni kolonu okuyup yazacak şekilde güncelle, eski kolonu da yazmaya devam et.

### Aşama 3 — Contract (Daralt)

Eski kolonu kaldır:

```sql
-- Önce constraint ekle
ALTER TABLE users ALTER COLUMN display_name SET NOT NULL;

-- Sonra eski kolonu kaldır
ALTER TABLE users DROP COLUMN full_name;
```

---

## 3. Yaygın Migration Pattern'ları

### Kolona DEFAULT Ekleme (PostgreSQL)

```sql
-- ❌ Tüm tabloyu kilitler (büyük tablolarda tehlikeli)
ALTER TABLE orders ADD COLUMN status VARCHAR(50) DEFAULT 'pending' NOT NULL;

-- ✅ Güvenli: önce nullable ekle, sonra backfill, sonra constraint
ALTER TABLE orders ADD COLUMN status VARCHAR(50);
UPDATE orders SET status = 'pending' WHERE status IS NULL;
ALTER TABLE orders ALTER COLUMN status SET DEFAULT 'pending';
ALTER TABLE orders ALTER COLUMN status SET NOT NULL;
```

### Index Oluşturma (Lock Olmadan)

```sql
-- ❌ Tabloyu kilitler
CREATE INDEX idx_users_email ON users(email);

-- ✅ CONCURRENTLY — lock olmadan (daha yavaş ama güvenli)
CREATE INDEX CONCURRENTLY idx_users_email ON users(email);
```

### Tablo Yeniden Adlandırma

```sql
-- Aşama 1: Yeni tabloyu oluştur
CREATE TABLE user_profiles AS SELECT * FROM users WHERE 1=0;

-- Aşama 2: Trigger ile senkron tut
CREATE OR REPLACE FUNCTION sync_user_profiles()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO user_profiles VALUES (NEW.*) ON CONFLICT DO UPDATE SET ...;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER sync_on_user_change
AFTER INSERT OR UPDATE ON users
FOR EACH ROW EXECUTE FUNCTION sync_user_profiles();

-- Aşama 3: Backfill
INSERT INTO user_profiles SELECT * FROM users;

-- Aşama 4: Uygulama geçişi + trigger kaldır + eski tabloyu sil
```

### Foreign Key Ekleme

```sql
-- ❌ Validation lock yaratır
ALTER TABLE orders ADD CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id);

-- ✅ NOT VALID ile ekle, sonra validate et
ALTER TABLE orders
  ADD CONSTRAINT fk_user
  FOREIGN KEY (user_id) REFERENCES users(id)
  NOT VALID;

-- Ayrı transaction'da validate (AccessShareLock — daha hafif)
ALTER TABLE orders VALIDATE CONSTRAINT fk_user;
```

---

## 4. Rollback Stratejileri

### Her Migration Dosyasına `down` Ekle

```sql
-- V1__add_display_name.sql (up)
ALTER TABLE users ADD COLUMN display_name VARCHAR(255);
CREATE INDEX CONCURRENTLY idx_users_display_name ON users(display_name);

-- V1__add_display_name.down.sql (rollback)
DROP INDEX CONCURRENTLY IF EXISTS idx_users_display_name;
ALTER TABLE users DROP COLUMN IF EXISTS display_name;
```

### Veri Kaybı Riski Olan Migration'larda Backup

```sql
-- Migration öncesi snapshot tablo oluştur
CREATE TABLE users_backup_20240315 AS SELECT * FROM users;

-- Migration sonrası doğrula
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM users_backup_20240315;
-- Sayılar eşleşmeli

-- Onay sonrası backup'ı sil (belirli süre sonra)
DROP TABLE users_backup_20240315;
```

---

## 5. Büyük Tablo Migration'ları

```sql
-- Batch update — lock süresini minimize et
DO $$
DECLARE
  batch_size INT := 1000;
  last_id BIGINT := 0;
  max_id BIGINT;
BEGIN
  SELECT MAX(id) INTO max_id FROM users;

  WHILE last_id < max_id LOOP
    UPDATE users
    SET display_name = full_name
    WHERE id > last_id
      AND id <= last_id + batch_size
      AND display_name IS NULL;

    last_id := last_id + batch_size;
    PERFORM pg_sleep(0.1);  -- Replication lag'ı önle
  END LOOP;
END $$;
```

---

## 6. Pre/Post Migration Validation

```sql
-- Pre-migration: Mevcut durumu kaydet
SELECT
  COUNT(*) AS total_rows,
  COUNT(email) AS email_count,
  COUNT(DISTINCT user_id) AS unique_users
FROM orders
INTO migration_baseline;

-- Post-migration: Karşılaştır
SELECT
  (SELECT COUNT(*) FROM orders) = baseline.total_rows AS row_count_ok,
  (SELECT COUNT(DISTINCT user_id) FROM orders) = baseline.unique_users AS users_ok
FROM migration_baseline baseline;
```

---

## 7. Migration Araçları

| Araç              | Stack              | Özellik                             |
| ----------------- | ------------------ | ----------------------------------- |
| Flyway            | Java/Kotlin/Node   | Versioned migrations, SQL-first     |
| Liquibase         | Java               | XML/YAML/JSON/SQL, rollback desteği |
| Prisma Migrate    | Node.js/TypeScript | ORM entegrasyonu                    |
| Drizzle Kit       | Node.js/TypeScript | TypeScript-first                    |
| `node-pg-migrate` | Node.js            | Minimal, PostgreSQL odaklı          |

---

## 8. Production Deployment Checklist

Canlıya almadan önce kontrol listesi:

- [ ] Migration dry-run staging ortamında çalıştırıldı
- [ ] Estimated lock time hesaplandı (büyük tablolar için CONCURRENTLY kullanıldı)
- [ ] Rollback script'i hazır ve test edildi
- [ ] Pre-migration backup alındı veya snapshot oluşturuldu
- [ ] Maintenance window (gerekiyorsa) planlandı
- [ ] Post-migration validation sorguları hazır
- [ ] Monitoring/alerting aktif
- [ ] Uygulama yeni ve eski schema ile backward compatible

---

## 9. Dikkat Edilecekler

**Asla yapma:**

- Production'da `DROP TABLE` veya `DROP COLUMN` direkt çalıştırma (önce expand-contract)
- Büyük tabloda `NOT NULL` constraint olmadan veri backfill etme
- Migration sırasında uzun transaction açık tutma
- Lock timeout ayarı yapmadan DDL çalıştırma

**PostgreSQL için özel:**

```sql
-- Lock timeout set et — uzun bekleme yerine hata al
SET lock_timeout = '5s';

-- Statement timeout — uzun sorguları durdur
SET statement_timeout = '30s';
```
