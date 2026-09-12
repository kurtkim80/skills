---
name: project-planner-skill
description: Generate comprehensive project planning documents — requirements, system design, and task breakdown plans. Use when starting a new feature or project, defining specifications, creating technical designs, or breaking down complex implementations into traceable tasks.
---

# Project Planner Skill

Yazılım projelerini yapılandırılmış requirements, design ve implementation plan dokümanlarına dönüştürme rehberi.

## When to use this skill

- Yeni feature veya proje başlatılırken
- Teknik spesifikasyon dokümantasyonu gerektiğinde
- Karmaşık implementasyonlar görevlere ayrılacakken
- PR'dan önce teknik tasarım netleştirilecekken

---

## 1. Üç Temel Doküman

| Doküman      | Amaç                                         | Dosya             |
| ------------ | -------------------------------------------- | ----------------- |
| Requirements | Kullanıcı hikayeleri + kabul kriterleri      | `requirements.md` |
| Design       | Mimari + component + veri akışı              | `design.md`       |
| Tasks        | Görev kırılımı + requirement izlenebilirliği | `tasks.md`        |

---

## 2. Requirements Dokümanı Şablonu

```markdown
# Requirements — [Feature Adı]

## Giriş

[Sistem açıklaması 2-3 cümle. Hedef kullanıcı ve kapsam.]

## Sözlük

- **Terim**: Bu sisteme özgü tanım

## Gereksinimler

### Gereksinim 1

**Kullanıcı Hikayesi**: Bir [kullanıcı tipi] olarak, [yetenek] istiyorum, böylece [fayda] sağlayayım.

#### Kabul Kriterleri

1. BİR [tetikleyici/koşul] OLDUĞUNDA, [bileşen] [eylem/davranış] OLMALI
2. [bağlam/mod]'DA, [bileşen] [eylem] OLMALI
3. [koşul] İSE, [bileşen] [eylem] OLMALI
4. [bileşen] [ölçülebilir hedef ile yetenek] OLMALI
```

### Kabul Kriteri Kalıpları

```
Davranış:
- BİR [olay gerçekleştiğinde], sistem [yanıt vermeli]
- Sistem [kural/limit] UYGULAMALI

Koşullu:
- [koşul] İSE, sistem [eylem] ETMELI
- [mod aktifken], sistem [davranış] SERGILEMELI

Performans:
- Sistem [işlemi] [süre içinde] TAMAMLAMALI
- Sistem [N] eş zamanlı [işlemi] DESTEKLEMELİ
```

---

## 3. Design Dokümanı Şablonu

```markdown
# Design — [Feature Adı]

## Genel Bakış

[Mimari özeti 3-4 cümle.]

## Sistem Mimarisi

### Component Haritası

| Component ID | Ad           | Tip     | Sorumluluk        | Etkileştiği |
| ------------ | ------------ | ------- | ----------------- | ----------- |
| COMP-1       | Web Frontend | UI      | Kullanıcı arayüzü | COMP-2      |
| COMP-2       | API Routes   | Service | İstek yönlendirme | COMP-3      |

### Yüksek Seviye Mimari Diyagramı

[ASCII diyagram — tüm component'ler ve ilişkileri]

## Veri Akışı

### Akış 1: [Akış Adı]
```

1. [Kaynak] → [Bileşen]: [Veri açıklaması]
2. [Bileşen] → [Bileşen]: [Dönüşüm]
3. [Bileşen] → [Hedef]: [Son format]

```

## Entegrasyon Noktaları

| Kaynak | Hedef | Protokol | Format | Amaç |
|--------|-------|----------|--------|------|
| Frontend | API | HTTPS/REST | JSON | API çağrıları |

## Veri Modelleri

[Entity tanımları ve ilişkileri]

## Hata Yönetimi

[Hata kategorileri ve strateji]

## Test Stratejisi

- Unit: [Ne test edilecek]
- Integration: [Hangi akış]
- E2E: [Kritik user journey]
```

---

## 4. Task Breakdown Şablonu

```markdown
# Implementation Plan — [Feature Adı]

## Proje Sınırları

**Must-have**: Core özellikler
**Nice-to-have**: İyileştirmeler
**Kapsam dışı**: Açıkça dışlananlar

---

- [ ] 1. Altyapı Kurulumu
  - [ ] 1.1 Proje yapısı
    - Dizin oluştur
    - Type tanımları
    - _Gereksinimler: REQ-1.1_
  - [ ] 1.2 Veri katmanı
    - Firestore schema
    - _Gereksinimler: REQ-2.1_
    - _Bağımlılıklar: 1.1_

- [ ] 2. İş Mantığı
  - [ ] 2.1 [Core feature]
    - Implementasyon adımları
    - _Gereksinimler: REQ-3.1, REQ-3.2_
    - _Bağımlılıklar: Faz 1_

- [ ] 3. API Katmanı
  - [ ] 3.1 Route handler'lar
    - _Gereksinimler: REQ-4.1_

- [ ] 4. Frontend
  - [ ] 4.1 Component'ler
    - _Gereksinimler: REQ-5.1_

- [ ] 5. Test
  - [ ] 5.1 Unit testler
  - [ ] 5.2 Integration testler
```

---

## 5. Talent Architect Feature Planning

Talent Architect'e yeni feature eklerken şu soruları yanıtla:

### Mimari Sorular

```
1. Bu feature hangi domain'e ait?
   → features/{domain}/server/ altına mı gidecek?

2. Firebase'de ne depolanacak?
   → Firestore collection adı ve document yapısı?

3. AI kullanıyor mu?
   → Anthropic SDK mi, OpenRouter mi?
   → Rate limit gerekiyor mu?

4. Subscription gerektirir mi?
   → Free tier limiti nedir?
   → Monitoring'e event yazılacak mı?

5. i18n gerekiyor mu?
   → TR + EN key'leri eklenecek mi?
```

### Feature Checklist

- [ ] `features/{feature}/` dizini oluşturuldu
- [ ] `features/{feature}/server/` servis dosyası oluşturuldu
- [ ] `features/{feature}/types.ts` type'ları tanımlandı
- [ ] Firestore şema tasarlandı
- [ ] API route handler yazıldı (`src/app/api/`)
- [ ] Auth kontrolü eklenecek route'lar belirlendi
- [ ] i18n key'leri TR + EN eklendi
- [ ] `npm run locales:check` geçiyor
- [ ] Monitoring event'leri tanımlandı
- [ ] Subscription kontrolü eklendi (gerekiyorsa)

---

## 6. Yaygın Uygulama Fazları

```
Faz 1: Altyapı
  - Proje yapısı, type tanımları, Firestore şema

Faz 2: Veri Katmanı
  - Firestore CRUD operasyonları, validation

Faz 3: İş Mantığı
  - Core algoritmalar, servis sınıfları, AI entegrasyon

Faz 4: API Katmanı
  - Route handler'lar, auth, rate limiting

Faz 5: Frontend
  - Component'ler, state management, form validation

Faz 6: Test
  - Unit, integration, E2E

Faz 7: Monitoring
  - Event logging, error tracking
```

---

## 7. Kalite Kontrol Listesi

### Requirements Dokümanı

- [ ] Her gereksinim için kullanıcı hikayesi var
- [ ] Tüm kabul kriterleri ölçülebilir/test edilebilir
- [ ] Non-functional gereksinimler belirtildi (performans, güvenlik)
- [ ] Sözlük domain terimlerini kapsıyor
- [ ] Gereksinimler trace için numaralandırıldı

### Design Dokümanı

- [ ] Tüm component'lerin sorumlulukları net
- [ ] Veri akışı diyagramları mevcut
- [ ] Hata yönetimi stratejisi belgelenmiş
- [ ] Performans hedefleri belirtilmiş

### Task Breakdown

- [ ] Görevler mantıklı fazlara gruplandı
- [ ] Bağımlılıklar belirtildi
- [ ] Her göreve requirement izlenebilirliği eklendi
- [ ] Görevler bağımsız tamamlanabilir
- [ ] Checkbox formatı kullanıldı
