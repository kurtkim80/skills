---
name: brainstorming-skill
description: Turn ideas into fully formed designs and specifications through structured collaborative dialogue. Use BEFORE any creative or implementation work — when exploring feature ideas, designing user flows, evaluating approaches, or planning architecture. Prevents scope creep and ensures alignment before coding.
---

# Brainstorming Skill

Fikirleri doğal diyalog yoluyla tam gelişmiş tasarım ve spesifikasyonlara dönüştürme metodolojisi. Herhangi bir implementasyondan önce kullanılmalı.

## When to use this skill

- Yeni feature veya component geliştirilmeden önce
- Mimari karar verilirken alternatifler değerlendirilecekken
- Kullanıcı akışı veya UX tasarımı yapılırken
- Karmaşık bir problemi çözüm uzayını keşfetmeden önce
- Scope netleştirilmesi gerektiğinde

---

## 1. Süreç

### Faz 1 — Fikri Anlama

```
1. Mevcut proje durumunu kontrol et (dosyalar, son değişiklikler)
2. Soru sor — bir seferde TEK soru
3. Tercih et: çoktan seçmeli sorular > açık uçlu sorular
4. Odaklan: amaç, kısıtlar, başarı kriterleri
```

**Sorulacak sorular:**

- Bu ne için? Kim kullanacak?
- Başarı nasıl ölçülecek?
- Hard constraint var mı? (teknik, zaman, bütçe)
- Mevcut sistemle nasıl entegre olacak?

### Faz 2 — Alternatifleri Keşfet

```
2-3 farklı yaklaşım öner:
- Her birinin trade-off'larını açıkla
- Önerileni ve nedenini belirt
- Önce önerilen yaklaşımı sun
```

### Faz 3 — Tasarımı Sun (Bölümler Halinde)

```
Anlaşılınca tasarımı sun:
- 200-300 kelimelik bölümler halinde
- Her bölümden sonra kontrol et: "Bu doğru mu?"
- Geri al ve netleştir — esnek ol
```

**Kapsanacak alanlar:**

- Mimari / Veri akışı
- Component'ler ve sorumluluklar
- Hata durumları
- Test stratejisi

---

## 2. Temel Prensipler

### Bir Seferde Bir Soru

```
❌ Kötü:
"Kimler kullanacak? Hangi platformda? API mi yoksa local mi?
Performance target nedir? Budget var mı?"

✅ İyi:
"Bu özelliği kim kullanacak — iş arayanlar mı, işverenler mi?"
[Yanıt bekle]
"Hangi platformda öncelikle çalışmalı — web mi, mobil mi?"
```

### YAGNI — Gereksiz Feature Yok

Her tasarım kararında sor: "Bu şu an gerçekten gerekli mi?"

Tasarımdan çıkar:

- "İleride lazım olabilir" assumption'ları
- Kullanıcının talep etmediği esneklikler
- Over-engineering

### 2-3 Alternatif Öneri

```
Yaklaşım A — En Basit
  Açıklama, avantajlar, dezavantajlar

Yaklaşım B — Dengeli
  Açıklama, avantajlar, dezavantajlar

Yaklaşım C — En Güçlü
  Açıklama, avantajlar, dezavantajlar

→ Öneri: Yaklaşım B, çünkü [somut neden]
```

---

## 3. Talent Architect Bağlamı

Brainstorming yaparken şu soruları yanıtla:

```
1. Hangi feature domain'i?
   → features/{domain}/ altına mı gidecek?

2. Kullanıcı yolculuğu nasıl?
   → Mevcut UI flow'a nasıl entegre olacak?

3. AI kullanıyor mu?
   → Anthropic mı, OpenRouter mı?
   → Prompt stratejisi ne olacak?

4. Subscription gerektiriyor mu?
   → Free/Pro/Premium limitleri neler?

5. i18n?
   → TR + EN key'leri planlanıyor mu?

6. Monitoring?
   → Hangi event'ler loglanacak?
```

---

## 4. Tasarım Sonrası

### Dokümantasyon

```bash
# Tasarımı kaydet
docs/plans/YYYY-MM-DD-{konu}-design.md

# İçerik:
# - Seçilen yaklaşım ve gerekçe
# - Component listesi
# - Veri akışı
# - Open questions
```

### Implementasyon Hazırlığı

```
Tasarım onaylandıktan sonra:
1. project-planner-skill ile requirements.md oluştur
2. Design.md oluştur
3. Tasks.md (implementation plan) oluştur
4. İlk PR'ı küçük tut — MVP önce
```

---

## 5. Soru Bankası

### Fonksiyon Soruları

- "Bu özellik olmadan kullanıcı ne yapıyor şu an?"
- "Minimum viable versiyon ne olur?"
- "Edge case'ler neler? (boş state, hata, yavaş network)"

### Teknik Soruları

- "Mevcut bir pattern var mı buna benzer?"
- "Performance constraint var mı?"
- "Ölçeklenme gerekeceği var mı?"

### Kullanıcı Deneyimi Soruları

- "Kullanıcı bu akışta nerede takılabilir?"
- "Loading, empty ve error state nasıl görünecek?"
- "Mobile'da nasıl çalışacak?"

---

## 6. Anti-Pattern'lar

```
❌ Soru listesi vermek (overwhelming)
❌ Implementasyona detaya girmek (design aşamasında)
❌ Tek çözüm önermek (alternatifler göster)
❌ Kullanıcının talep etmediği özellikler eklemek
❌ "Belki ileride lazım olur" ile scope genişletmek
❌ Tasarımı tek seferde sunmak (bölümler halinde sun)
```
