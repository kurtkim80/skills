---
name: playwright-skill
description: Browser automation and E2E testing with Playwright. Use when testing web applications, automating browser interactions, validating user flows, checking responsive design, or performing browser-based testing. Auto-detects dev servers and writes clean test scripts.
---

# Playwright Skill — Browser Automation

Playwright ile web uygulaması E2E testi ve browser otomasyonu rehberi.

## When to use this skill

- Web uygulaması fonksiyonel test edilirken
- Kullanıcı flow'ları otomatize edilirken
- Responsive tasarım kontrol edilirken
- Login akışları ve form submission test edilirken
- Screenshot alınırken (görsel doğrulama)

---

## 1. Kurulum

```bash
npm install playwright
npx playwright install chromium
```

---

## 2. Temel Workflow

**Adım 1 — Dev server tespit et:**

```bash
# Çalışan port'ları kontrol et
npx detect-port 3000 3001 3002 4000 8080 | grep -v "available"
```

**Adım 2 — Test script'i `/tmp`'ye yaz:**
Test dosyalarını proje dizinine değil `/tmp/playwright-test-*.js`'e yaz.

**Adım 3 — Çalıştır:**

```bash
node /tmp/playwright-test-example.js
```

---

## 3. Temel Pattern'lar

### Sayfa Yükleme ve Screenshot

```javascript
const { chromium } = require('playwright')

const TARGET_URL = 'http://localhost:3000'

;(async () => {
  const browser = await chromium.launch({ headless: false })
  const page = await browser.newPage()

  try {
    await page.goto(TARGET_URL, { waitUntil: 'networkidle', timeout: 10000 })
    console.log('Başlık:', await page.title())
    await page.screenshot({ path: '/tmp/screenshot.png', fullPage: true })
    console.log('📸 Screenshot: /tmp/screenshot.png')
  } catch (error) {
    console.error('❌ Hata:', error.message)
  } finally {
    await browser.close()
  }
})()
```

### Form Doldurma ve Submit

```javascript
const { chromium } = require('playwright')

const TARGET_URL = 'http://localhost:3000'

;(async () => {
  const browser = await chromium.launch({ headless: false, slowMo: 50 })
  const page = await browser.newPage()
  await page.goto(`${TARGET_URL}/contact`)

  await page.fill('input[name="name"]', 'Test Kullanıcı')
  await page.fill('input[name="email"]', 'test@example.com')
  await page.fill('textarea[name="message"]', 'Test mesajı')
  await page.click('button[type="submit"]')

  await page.waitForSelector('.success-message')
  console.log('✅ Form başarıyla gönderildi')

  await browser.close()
})()
```

### Login Akışı Testi

```javascript
const { chromium } = require('playwright')

const TARGET_URL = 'http://localhost:3000'

;(async () => {
  const browser = await chromium.launch({ headless: false })
  const page = await browser.newPage()

  await page.goto(`${TARGET_URL}/login`)
  await page.fill('input[name="email"]', 'test@example.com')
  await page.fill('input[name="password"]', 'password123')
  await page.click('button[type="submit"]')

  await page.waitForURL('**/dashboard', { timeout: 5000 })
  console.log("✅ Login başarılı, dashboard'a yönlendirildi")

  await browser.close()
})()
```

### Responsive Tasarım Testi

```javascript
const { chromium } = require('playwright')

const TARGET_URL = 'http://localhost:3000'

;(async () => {
  const browser = await chromium.launch({ headless: false })
  const page = await browser.newPage()

  const viewports = [
    { name: 'Desktop', width: 1440, height: 900 },
    { name: 'Tablet', width: 768, height: 1024 },
    { name: 'Mobile', width: 375, height: 667 },
  ]

  for (const viewport of viewports) {
    console.log(`Testing ${viewport.name} (${viewport.width}x${viewport.height})...`)
    await page.setViewportSize({ width: viewport.width, height: viewport.height })
    await page.goto(TARGET_URL)
    await page.waitForTimeout(500)
    await page.screenshot({
      path: `/tmp/${viewport.name.toLowerCase()}.png`,
      fullPage: true,
    })
    console.log(`  📸 /tmp/${viewport.name.toLowerCase()}.png`)
  }

  await browser.close()
})()
```

### Kırık Link Kontrolü

```javascript
const { chromium } = require('playwright')

;(async () => {
  const browser = await chromium.launch({ headless: false })
  const page = await browser.newPage()
  await page.goto('http://localhost:3000')

  const links = await page.locator('a[href^="http"]').all()
  const results = { working: 0, broken: [] }

  for (const link of links) {
    const href = await link.getAttribute('href')
    try {
      const response = await page.request.head(href)
      if (response.ok()) {
        results.working++
      } else {
        results.broken.push({ url: href, status: response.status() })
      }
    } catch (e) {
      results.broken.push({ url: href, error: e.message })
    }
  }

  console.log(`✅ Çalışan linkler: ${results.working}`)
  if (results.broken.length > 0) {
    console.log(`❌ Kırık linkler:`, results.broken)
  }

  await browser.close()
})()
```

### Console Error Monitoring

```javascript
const { chromium } = require('playwright')

;(async () => {
  const browser = await chromium.launch({ headless: false })
  const page = await browser.newPage()

  const consoleErrors = []
  page.on('console', (msg) => {
    if (msg.type() === 'error') consoleErrors.push(msg.text())
  })

  await page.goto('http://localhost:3000')
  await page.waitForTimeout(2000)

  if (consoleErrors.length > 0) {
    console.log('🚨 Console hataları bulundu:')
    consoleErrors.forEach((err) => console.log(`  - ${err}`))
  } else {
    console.log('✅ Console hatası yok')
  }

  await browser.close()
})()
```

---

## 4. Bekleme Stratejileri

```javascript
// ✅ İyi — duruma göre bekle
await page.waitForURL('**/dashboard')
await page.waitForSelector('.success-message')
await page.waitForLoadState('networkidle')
await page.waitForResponse((response) => response.url().includes('/api/'))

// ❌ Kötü — sabit timeout (çok kırılgan)
await page.waitForTimeout(3000) // Sadece gerektiğinde
```

---

## 5. Kullanışlı Seçiciler

```javascript
// En sağlam — test-id ile
await page.locator('[data-testid="submit-button"]').click()

// ARIA role ile
await page.getByRole('button', { name: 'Kaydet' }).click()
await page.getByRole('textbox', { name: 'Email' }).fill('test@example.com')

// Label ile
await page.getByLabel('Email adresi').fill('test@example.com')

// Metin ile
await page.getByText('Başarıyla kaydedildi').waitFor()

// CSS seçici (daha kırılgan)
await page.locator('button[type="submit"]').click()
```

---

## 6. Talent Architect için Özel Test Senaryoları

### CV Yükleme Testi

```javascript
const { chromium } = require('playwright')
const path = require('path')

;(async () => {
  const browser = await chromium.launch({ headless: false })
  const page = await browser.newPage()

  await page.goto('http://localhost:3000/cv/upload')

  const fileChooserPromise = page.waitForEvent('filechooser')
  await page.click('[data-testid="upload-area"]')
  const fileChooser = await fileChooserPromise
  await fileChooser.setFiles(path.join(__dirname, 'test-cv.pdf'))

  await page.waitForSelector('[data-testid="upload-success"]', { timeout: 30000 })
  console.log('✅ CV yükleme başarılı')

  await browser.close()
})()
```

### ATS Analiz Akışı Testi

```javascript
;(async () => {
  const browser = await chromium.launch({ headless: false })
  const page = await browser.newPage()

  await page.goto('http://localhost:3000/ats')
  await page.fill('[data-testid="job-description"]', 'Senior Software Engineer...')
  await page.click('[data-testid="analyze-button"]')

  // AI analizi uzun sürebilir
  await page.waitForSelector('[data-testid="ats-score"]', { timeout: 60000 })
  const score = await page.textContent('[data-testid="ats-score"]')
  console.log('✅ ATS skoru:', score)

  await browser.close()
})()
```

---

## 7. İpuçları

- **DEFAULT**: `headless: false` — görsel debugging için
- **Test dosyaları**: `/tmp/playwright-test-*.js` — projeyi kirletme
- **URL parametrize et**: Her script'te `const TARGET_URL = '...'`
- **Try-catch zorunlu**: Robust automation için
- **Slow mo kullan**: `slowMo: 100` — aksiyonları izlemeyi kolaylaştırır
- **Sabit timeout kullanma**: `waitForSelector`, `waitForURL` tercih et
