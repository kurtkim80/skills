---
name: code-reviewer-skill
description: Comprehensive code review methodology — both requesting reviews (structured workflow) and receiving feedback (technical evaluation, not performative agreement). Use when conducting code reviews, preparing PRs for review, or receiving and evaluating review feedback.
---

# Code Reviewer Skill

Kod inceleme sürecinin her iki tarafı: review talep etme ve review almak için metodoloji.

## When to use this skill

- PR öncesi kendi kodunu gözden geçirirken
- Başka birinin kodunu review ederken
- Review feedback alındığında (uygulama öncesi değerlendirme)
- Major feature tamamlandığında

---

## 1. Code Review İsteme

### Ne Zaman Review İste

**Zorunlu:**

- Her major feature tamamlandığında
- Main branch'e merge öncesi
- Karmaşık bug fix sonrasında

**İsteğe Bağlı (değerli):**

- Takıldığında (taze bakış açısı)
- Büyük refactoring öncesi (baseline)

### Review Request Workflow

```bash
# 1. Değişiklikleri hazırla
git status && git diff

# 2. SHA'ları al
BASE_SHA=$(git rev-parse origin/main)
HEAD_SHA=$(git rev-parse HEAD)

# 3. Review talebi formatı
Konu: [Feature/Fix] Kısa açıklama
SHA aralığı: BASE..HEAD
Neyi kontrol etmemi istiyorsun: [auth, performance, accessibility...]
```

### Kapsamlı Review Süreci

**Adım 1 — Preflight:**

```bash
npm run type-check    # TypeScript
npx eslint src        # Lint
npm run locales:check # i18n parity
```

**Adım 2 — Değişiklik Analizi:**

```bash
git log --oneline BASE..HEAD   # Commit geçmişi
git diff --stat BASE..HEAD     # Etkilenen dosyalar
git diff BASE..HEAD            # Tam diff
```

**Adım 3 — Analiz Kriterleri:**

- **Doğruluk**: Kod istenen davranışı sağlıyor mu? Bug veya mantık hatası?
- **Sürdürülebilirlik**: Temiz yapı, modüler, değiştirilebilir mi?
- **Okunabilirlik**: Naming, comment gereksinimi, tutarlılık
- **Güvenlik**: Input validation, auth, secret exposure, XSS
- **Performans**: N+1, bundle size, waterfall
- **Edge case**: Boş state, hata, timeout, network failure
- **Test**: Yeni kod için yeterli test coverage var mı?

### Bulgu Formatı

```markdown
## Bulgu #N: [Başlık]

**Önem**: [KRİTİK/YÜKSEK/ORTA/DÜŞÜK]
**Konum**: dosya:satır
**Kategori**: [Güvenlik/Performans/Doğruluk/UX]

### Açıklama

[Net açıklama]

### Öneri

[Spesifik düzeltme]
```

### Review Özet Formatı

```markdown
## Kod Review Özeti

**Genel Değerlendirme**: [ONAY / REVİZYON GEREKLİ / KOŞULLU ONAY]

### Güçlü Yönler

- [Olumlu nokta 1]
- [Olumlu nokta 2]

### Kritik Sorunlar (Merge öncesi düzeltilmeli)

- [Sorun 1]

### Öneriler (Takdire bırakılmış)

- [Öneri 1]
```

---

## 2. Review Almak

### Temel Prensip

Review feedback = teknik değerlendirme gerektiren öneri, körü körüne uyulacak emir değil.

### Yanıt Süreci

```
1. OKU      → Tüm feedback'i tamamen oku, tepki verme
2. ANLA     → Her maddeyi kendi cümlelerinle ifade et (veya sor)
3. DOĞRULA  → Codebase'de gerçekten sorun var mı kontrol et
4. DEĞERLENDİR → Bu codebase için teknik olarak doğru mu?
5. YANIT VER → Teknik onay veya gerekçeli itiraz
6. UYGULA   → Birer birer, her birini test et
```

### Yasak Yanıtlar

```
❌ "Kesinlikle haklısın!"
❌ "Harika nokta!"
❌ "Hemen uygulayayım" (doğrulamadan)
❌ "Teşekkürler" (performatif şükran)

✅ "Kontrol ettim — [sorun gerçekten var]. Düzeltiyorum."
✅ "Doğruladım — [sorun yok]. Çünkü [teknik gerekçe]."
✅ Sadece düzeltmeyi yap, eylem konuşur
```

### Belirsiz Feedback Durumu

```
Eğer herhangi bir madde belirsizse:
  DURUR — hiçbir şey uygulanmaz
  Tüm belirsiz maddeleri açıkla sor
  SONRA başla

Neden: Maddeler birbiriyle ilgili olabilir.
Kısmi anlama = yanlış uygulama.
```

### Dış Reviewer Feedback'ini Değerlendirme

```
Uygulamadan önce kontrol et:
  1. Bu codebase için teknik olarak doğru mu?
  2. Mevcut fonksiyonu kırıyor mu?
  3. Mevcut implementasyonun nedeni var mıydı?
  4. Tüm platform/versiyon için çalışıyor mu?
  5. Reviewer tam context'e sahip mi?

Öneri yanlış görünüyorsa → teknik gerekçeyle itiraz et
```

### Doğru Feedback Onaylama

```
✅ "Düzelttim. [Ne değişti - kısa]"
✅ "Yakaladın — [spesifik sorun]. Düzeltme: [konum]"
✅ [Sadece düzelt, kod gösterir]

❌ Uzun özür
❌ Neden itiraz ettiğini savunma
❌ Aşırı açıklama
```

### Gerekçeli İtiraz

```
Teknik gerekçeyle itiraz et:
  - Mevcut testleri/kodu göster
  - Neden şu anki implementasyonun doğru olduğunu göster
  - Spesifik soru sor
  - Mimari ise önce teknik lider ile tartış
```

---

## 3. Talent Architect Özel Kontrol Noktaları

### Her PR İçin Zorunlu Kontroller

```bash
# Type check
npm run type-check

# Locale parity
node scripts/check-locale-parity.mjs

# ESLint
npx eslint src --ext .ts,.tsx
```

### Feature-Specific Kontrol Listesi

```markdown
Auth değişikliği:

- [ ] requireAuth() ilk satırda
- [ ] Session cookie firebase pattern'ı korunuyor
- [ ] Admin route'ları requireAdminAuth() kullanıyor

AI endpoint değişikliği:

- [ ] Rate limiting uygulandı
- [ ] Error response stack trace içermiyor
- [ ] Monitoring event loglandı
- [ ] Token limiti set edildi (max_tokens)

i18n değişikliği:

- [ ] TR ve EN key'leri her ikisine eklendi
- [ ] locales:check geçiyor
- [ ] Placeholder sayısı eşleşiyor

Firestore değişikliği:

- [ ] Query'ler server-side filtreli (tüm döküman çekilmiyor)
- [ ] Composite index gereksinimi kontrol edildi
- [ ] Security rules güncellendi (gerekiyorsa)
```

---

## 4. Ortak Hatalar

| Hata                                         | Düzeltme                        |
| -------------------------------------------- | ------------------------------- |
| Doğrulamadan uygulama                        | Codebase'de kontrol et önce     |
| Belirsizlik varken devam                     | Önce tüm belirsiz maddeleri sor |
| Performatif kabul                            | Teknik onay veya itiraz et      |
| Toplu test (hepsini birden)                  | Birer birer uygula ve test et   |
| Reviewer'ın her zaman haklı olduğu varsayımı | Teknik doğruluğu kontrol et     |

---

## 5. Large PR Review (500+ Satır)

500 satırı aşan PR'larda standart review'a ek olarak şu kontroller uygulanır:

### Mimari Analiz

- Yeni bağımlılıklar mevcut mimari sınırlarını ihlal ediyor mu?
- Feature domain ownership'e uyuluyor mu (`features/*/server/` pattern'ı)?
- God-object veya god-service oluşuyor mu?
- Circular dependency riski var mı?

### Breaking Change Değerlendirmesi

- Public API veya tip tanımları değişti mi?
- Mevcut Firestore/database schema'sını kıran değişiklik var mı?
- i18n key'leri kaldırıldı veya yeniden adlandırıldı mı?
- Route veya endpoint yapısı değişti mi?

### Performans Etkisi

- Büyük tablo/koleksiyon üzerinde sorgular optimize mi?
- N+1 query riski var mı?
- Bundle size anlamlı şekilde artıyor mu?
- Re-render kaskaları yaratılıyor mu?

### Güvenlik Gözden Geçirmesi (OWASP Top 10)

- Injection riski (Firestore query, AI prompt)
- Broken Authentication
- Sensitive data exposure
- Security misconfiguration
- XSS veya CSRF riski

### Teknik Borç

- Refactor edilmesi gereken duplicated logic yaratıldı mı?
- Geçici çözümler kalıcı mı görünüyor?
- TODO/FIXME yorum sayısı kabul edilebilir mi?

### Sonuç Formatı (Large PR)

```markdown
## Large PR Review — [PR Başlığı]

**Satır Sayısı**: [N] satır değişiklik
**Etkilenen Domain'ler**: [cv, ats, auth, ...]

### Kritik Bulgular (Merge öncesi zorunlu)

- [Bulgu 1]

### Mimari Gözlemler

- [Gözlem 1]

### Performans/Güvenlik Notları

- [Not 1]

### Genel Değerlendirme

[ONAY / REVİZYON GEREKLİ] — [1-2 cümle gerekçe]

### Önerilen İlk 3 Aksiyon

1. ...
2. ...
3. ...
```

---

## 6. TypeScript Code Review Framework

TypeScript dosyalarını incelerken standart review'a ek olarak şu kategoriler sistematik olarak kontrol edilir.

### Tip Güvenliği Kontrolü

```typescript
// ❌ Tehlikeli tip assertion — tip sistemi bypass ediliyor
const user = response.data as User

// ✅ Runtime doğrulama ile güvenli parse
function parseUser(data: unknown): User {
  if (!isUser(data)) throw new ValidationError('Invalid user shape')
  return data
}

// ❌ Non-null assertion — runtime crash riski
const name = user!.profile!.name

// ✅ Optional chaining + fallback
const name = user?.profile?.name ?? 'Bilinmiyor'
```

### tsconfig Önerileri (Optimum Strict Ayarları)

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "noImplicitReturns": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  }
}
```

### Severity Sistemi (TypeScript Review İçin)

```markdown
🔴 KRİTİK — Merge engelleyici:

- Type error veya tsc hata veriyor
- Security açığı (any → user input → SQL/AI prompt)
- Runtime crash riski (non-null assertion, unsafe cast)

🟡 ÖNEMLİ — Düzeltilmesi şiddetle önerilir:

- Gereksiz any kullanımı
- Missing return type annotation (public API)
- Unsafe type assertion (as SomeType)
- noUnusedLocals/Parameters ihlali

🔵 ÖNERİ — Sonraki PR'a bırakılabilir:

- satisfies yerine as kullanımı
- Utility type fırsatı (Partial, Pick, Omit)
- Template literal type fırsatı
- import type eksikliği
```

### TypeScript Review Çıktı Formatı

```markdown
## TypeScript Code Review — [Dosya/Modül]

**TypeScript Versiyonu**: [x.x]
**strict mode**: [Aktif / Kapalı]

### Tip Güvenliği Bulguları

🔴 **[Dosya:Satır]** — Unsafe type assertion

- Mevcut: `const data = response as UserData`
- Beklenen: Zod schema ile parse et
- Neden: runtime'da shape uyumsuzluğu crash'e yol açar

### Önerilen Araçlar

- `npx tsc --noEmit` — tip hata kontrolü
- `ts-prune` — kullanılmayan export tespiti
- `madge --circular` — circular dependency tespiti
```
