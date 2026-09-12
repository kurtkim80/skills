---
name: system-monitoring-expert
description: Design, implement, and evolve professional monitoring dashboards. Covers KPI selection, telemetry schema, admin dashboard layout, alert design, and observability best practices. Use when working on monitoring dashboards, API routes, telemetry events, or platform health visualization.
---

# System Monitoring Expert Skill

Modern yazılım platformlarının monitoring altyapısını ve admin dashboard'larını tasarlama ve geliştirme skill'i.

## When to use this skill

- Admin monitoring sayfaları üzerinde çalışılırken
- Monitoring altyapısı geliştirilirken
- Monitoring API route'ları eklenirken/değiştirilirken
- Yeni telemetry event tipi tanımlanırken
- Monitoring dashboard layout'u gözden geçirilirken
- Platform health KPI'ları belirlenirken

## How to use it

- Her zaman içsel olarak İngilizce düşün
- Her zaman kullanıcıya Türkçe yanıt ver
- Kod veya konfigürasyon dosyalarına comment satırı yazma

---

## 1. KPI Hiyerarşisi

### Temel KPI'lar

#### Platform Health (Operasyonel — Real-time)

```yaml
Kullanılabilirlik:
  - Route başarı oranı (%)
  - Aktif incident sayısı
  - Son 1 saatte hata sayısı

Performans:
  - Median yanıt süresi (ms)
  - P95 yanıt süresi (ms)
  - Yavaş route'lar (>2s)

AI Servisleri:
  - AI completion başarı oranı (%)
  - Ortalama AI yanıt süresi (ms)
  - Rate limit isabetleri (saatlik)
```

#### Kullanıcı Metrikleri (Taktik — Günlük/Haftalık)

```yaml
Kullanım:
  - Günlük aktif kullanıcı (DAU)
  - Feature başına kullanım oranları
  - Oturum başına ortalama işlem sayısı

Dönüşüm:
  - Ücretsiz → Ücretli dönüşüm oranı
  - Feature adoption rate

Kalite:
  - Kullanıcı memnuniyet skorları
  - İş akışı tamamlanma oranları
  - Oturum başarı oranları
```

---

## 2. Best Practices

### Dashboard Tasarımı

- Maksimum 5–7 KPI tek ekranda — odak yeteneği sınırlı
- Trend olmadan tek değer anlamsız — zaman karşılaştırması ekle
- Metodoloji gizleme — hesaplama açıklaması her metrik yanında
- Dashboard responsive olmalı
- 3D grafik kullanma — algıyı bozar
- Actionable olmayan "vanity metric"lerden kaçın

### Veri Güvenliği

- Admin route'ları yetkilendirme ile korunmalı
- Monitoring event'lerinde PII (Kişisel Veri) bulunmamalı (redaction zorunlu)
- TTL field'ı her event'e yazılmalı — otomatik temizlik
- Rate limiting monitoring intake endpoint'lerine uygulanmalı
