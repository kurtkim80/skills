---
name: react-email-skill
description: Build and send HTML email templates using React Email components. Use when creating welcome emails, password resets, notifications, order confirmations, or any transactional email template. Works with Resend (already integrated in Talent Architect via lib/server/integrations).
---

# React Email Skill

React bileşenleriyle HTML email şablonları oluşturma ve Resend ile gönderme rehberi.

**Talent Architect Notu**: Proje Resend SDK'yı zaten kullanıyor (`resend: ^6.9.3`). Email gönderimi `lib/server/integrations/` altındaki servis katmanı üzerinden geçmeli.

## When to use this skill

- Yeni email şablonu oluşturulurken (welcome, password reset, bildirim, hesap onay)
- Mevcut email template'i refactor edilirken
- Email i18n (TR/EN) implementasyonu yapılırken
- Email preview geliştirme ortamında test edilirken

---

## 1. Kurulum

```bash
npx create-email@latest
cd react-email-starter
npm install
npm run dev
```

Mevcut projeye eklemek için `package.json`'a:

```json
{
  "scripts": {
    "email": "email dev --dir emails --port 3000"
  }
}
```

---

## 2. Temel Şablon Yapısı

```tsx
import {
  Html,
  Head,
  Preview,
  Body,
  Container,
  Heading,
  Text,
  Button,
  Tailwind,
  pixelBasedPreset,
} from '@react-email/components'

interface WelcomeEmailProps {
  name: string
  verificationUrl: string
}

export default function WelcomeEmail({ name, verificationUrl }: WelcomeEmailProps) {
  return (
    <Html lang='tr'>
      <Tailwind config={{ presets: [pixelBasedPreset] }}>
        <Head />
        <Preview>Talent Architect — Email adresinizi doğrulayın</Preview>
        <Body className='bg-gray-100 font-sans'>
          <Container className='max-w-xl mx-auto p-5 bg-white'>
            <Heading className='text-2xl text-gray-800'>Hoş geldiniz, {name}!</Heading>
            <Text className='text-base text-gray-700'>Hesabınızı aktifleştirmek için aşağıdaki butona tıklayın.</Text>
            <Button
              href={verificationUrl}
              className='bg-blue-600 text-white px-5 py-3 rounded block text-center no-underline box-border'
            >
              Email Adresimi Doğrula
            </Button>
          </Container>
        </Body>
      </Tailwind>
    </Html>
  )
}

WelcomeEmail.PreviewProps = {
  name: 'Zafer',
  verificationUrl: 'https://talent-architect.com/verify/abc123 ',
} satisfies WelcomeEmailProps
```

---

## 3. Temel Component'ler

| Component        | Amaç                                            |
| ---------------- | ----------------------------------------------- |
| `Html`           | Root wrapper (`lang` attribute ile)             |
| `Head`           | Meta, stiller                                   |
| `Body`           | Ana içerik sarmalayıcı                          |
| `Container`      | İçeriği ortalar (max-width)                     |
| `Preview`        | Gelen kutusunda preview metni — `Body`'den önce |
| `Heading`        | h1–h6 başlıklar                                 |
| `Text`           | Paragraflar                                     |
| `Button`         | Link buton — `box-border` zorunlu               |
| `Link`           | Hyperlink                                       |
| `Img`            | Resim — absolute URL zorunlu                    |
| `Hr`             | Yatay bölücü — `border-solid` zorunlu           |
| `Row` + `Column` | Çok sütunlu layout                              |
| `Section`        | Layout bölümleri                                |
| `Tailwind`       | Tailwind CSS'i aktif eder                       |

---

## 4. Kritik Stil Kuralları

### Zorunlu Class'lar

| Component          | Zorunlu Class                       | Neden                          |
| ------------------ | ----------------------------------- | ------------------------------ |
| `Button`           | `box-border`                        | Padding overflow önler         |
| `Hr` / border      | `border-solid`                      | Email client'lar inherit etmez |
| Tek taraflı border | `border-none border-t border-solid` | Diğer kenarları sıfırla        |

### Email Client Kısıtlamaları — Asla Yapma

- SVG veya WEBP kullanma — email client'larda render sorunları
- Flexbox veya CSS Grid kullanma — `Row/Column` kullan
- Tailwind responsive prefix (`sm:`, `md:`) kullanma — desteklenmez
- Dark mode class'ları (`dark:`) kullanma — desteklenmez
- Media query kullanma — email client'larda çalışmaz

### Görsel Değişkenler

```tsx
const baseURL = process.env.NODE_ENV === 'production'
  ? 'https://cdn.talent-architect.com '
  : ''

<Img src={`${baseURL}/static/logo.png`} alt='Talent Architect' width='150' height='50' />
```

---

## 5. Resend ile Gönderme

```typescript
import { Resend } from 'resend'
import { WelcomeEmail } from '@/emails/welcome'

const resend = new Resend(process.env.RESEND_API_KEY)

const { data, error } = await resend.emails.send({
  from: 'Talent Architect <noreply@talent-architect.com>',
  to: [user.email],
  subject: 'Email adresinizi doğrulayın',
  react: <WelcomeEmail name={user.name} verificationUrl={verificationUrl} />
})

if (error) {
  console.error('Email gönderilemedi:', error)
}
```

**Talent Architect entegrasyonu**: Bu kodu doğrudan route handler'a yazmak yerine `lib/server/integrations/` altına taşı.

---

## 6. i18n (next-intl ile)

```tsx
import { createTranslator } from 'next-intl'

interface EmailProps {
  name: string
  locale: 'tr' | 'en'
}

export default async function WelcomeEmail({ name, locale }: EmailProps) {
  const t = createTranslator({
    messages: await import(`../messages/${locale}.json`),
    namespace: 'welcome-email',
    locale,
  })

  return (
    <Html lang={locale}>
      <Body>
        <Text>
          {t('greeting')} {name},
        </Text>
        <Button href='...'>{t('cta')}</Button>
      </Body>
    </Html>
  )
}
```

---

## 7. HTML Render

```typescript
import { render } from '@react-email/components'
import { WelcomeEmail } from './emails/welcome'

const html = await render(<WelcomeEmail name='Zafer' verificationUrl='...' />)
const text = await render(<WelcomeEmail name='Zafer' verificationUrl='...' />, { plainText: true })
```

---

## 8. Statik Dosya Yapısı

```
emails/
  welcome.tsx
  password-reset.tsx
  static/
    logo.png        ← PNG/JPG (SVG/WEBP değil)
    banner.jpg
```

---

## 9. Best Practices

1. Her email için `PreviewProps` tanımla — geliştirme testi için
2. Max dosya boyutu 102KB — Gmail büyük email'leri kırpar
3. `plainText` versiyonu her zaman oluştur — accessibility ve bazı email client'lar
4. Absolute URL kullan tüm görsellerde
5. Test et: Gmail, Outlook, Apple Mail, Yahoo Mail
6. `{{variableName}}` pattern'ını template içine yazma — TypeScript prop olarak geç
7. `lang` attribute her zaman `Html` component'inde olmalı

---

## 10. Email Türleri (Talent Architect)

| Email Türü           | Tetikleyici       | Template                   |
| -------------------- | ----------------- | -------------------------- |
| Email doğrulama      | Kayıt             | `verify-email.tsx`         |
| Şifre sıfırlama      | Şifre sıfırla     | `password-reset.tsx`       |
| Subscription onay    | Ödeme başarılı    | `subscription-confirm.tsx` |
| CV analiz tamamlandı | ATS analizi bitti | `analysis-complete.tsx`    |
| Hesap uyarısı        | Güvenlik olayı    | `security-alert.tsx`       |
