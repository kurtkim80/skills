---
name: git-workflow-skill
description: Master git commits, interactive rebase, cherry-picking, bisect, worktrees, and reflog. Use when creating commits, cleaning up history before PRs, applying hotfixes across branches, finding bug-introducing commits, or recovering from git mistakes.
---

# Git Workflow Skill

Temiz commit geçmişi oluşturma ve gelişmiş Git operasyonları rehberi.

## When to use this skill

- Commit yazılırken (her commit için)
- PR öncesi geçmiş temizlenirken
- Hotfix birden fazla branch'e uygulanırken
- Bug'ı hangi commit'in getirdiği bulunurken
- Git hatalarından kurtarma gerektiğinde

---

## 1. Commit Yazma

### Temel Workflow

```bash
git status                 # Değişikliklere bak
git diff                   # Farkları incele
git log --oneline -5       # Son commit stilini gör
git add [dosyalar]         # Stage et
git commit -m "mesaj"      # Commit et
```

### Commit Mesajı Formatı

```
<özet satırı — ne ve neden, nasıl değil>

<opsiyonel gövde — daha fazla bağlam>
```

### İyi Commit Mesajı Örnekleri

```bash
# Tek dosya, net değişiklik
git commit -m "Update ATS analysis timeout to 30 seconds"

# İlgili değişiklikler
git commit -m "Add CV upload validation for file size limit

Validate file size on both client and server.
Max 5MB enforced via Zod schema and API route middleware."

# Bug fix
git commit -m "Fix dark mode hydration flash in ThemeProvider

Initialize theme from cookie before first render to prevent
client/server mismatch and visible flash on page load."
```

### Ne Zaman Böl, Ne Zaman Birleştir

**Ayrı commit**:

- CSS vs iş mantığı değişiklikleri
- Farklı feature'lar (aynı dosyada bile)
- Refactoring vs yeni fonksiyon
- Her bug için ayrı fix

**Tek commit**:

- Bir feature için ilgili değişiklikler
- Handler + CSS'i
- Feature + yazılan testler

---

## 2. Interactive Rebase — Geçmiş Temizleme

### Temel Kullanım

```bash
# Son 5 commit'i düzenle
git rebase -i HEAD~5

# Branch'teki tüm commit'ler (main'den ayrıldığından beri)
git rebase -i $(git merge-base HEAD main)
```

### Rebase Operasyonları

| Komut    | Açıklama                                          |
| -------- | ------------------------------------------------- |
| `pick`   | Commit'i olduğu gibi bırak                        |
| `reword` | Sadece mesajı değiştir                            |
| `edit`   | Commit içeriğini değiştir                         |
| `squash` | Önceki commit ile birleştir (mesajları birleştir) |
| `fixup`  | Önceki ile birleştir (bu mesajı sil)              |
| `drop`   | Commit'i tamamen sil                              |

### PR Öncesi Temizlik Workflow

```bash
git checkout feature/my-feature

# Geçmişi temizle
git rebase -i main

# Tipik operasyonlar:
# - "fix typo" commit'lerini squash et
# - Commit mesajlarını reword et
# - Mantıksal sırayla düzenle
# - Gereksizleri drop et

# Güvenli force push (başkası kullanmıyorsa)
git push --force-with-lease origin feature/my-feature
```

### Autosquash Workflow

```bash
# Initial commit
git commit -m "feat: add CV upload validation"

# Düzeltme commit'i
git add .
git commit --fixup HEAD  # veya: git commit --fixup abc123

# Otomatik squash ile rebase
git rebase -i --autosquash main
# Git fixup commit'lerini otomatik işaretler
```

---

## 3. Cherry-Pick — Seçici Commit Uygulama

```bash
# Tek commit
git cherry-pick abc123

# Commit aralığı (exclusive start)
git cherry-pick abc123..def456

# Commit etmeden sadece stage et
git cherry-pick -n abc123

# Mesajı düzenleyerek cherry-pick
git cherry-pick -e abc123
```

### Hotfix Birden Fazla Branch'e Uygulama

```bash
# main'de fix oluştur
git checkout main
git commit -m "fix: critical security patch"

# Release branch'lerine uygula
git checkout release/2.0
git cherry-pick abc123

git checkout release/1.9
git cherry-pick abc123

# Conflict varsa
git cherry-pick --continue
# veya
git cherry-pick --abort
```

---

## 4. Git Bisect — Bug'ı Bulma

```bash
# Bisect başlat
git bisect start
git bisect bad HEAD           # Şu an bozuk
git bisect good v2.1.0        # Bilinen iyi versiyon

# Git ortaya commit'e gider — test et
npm test
git bisect good  # veya: git bisect bad

# Git bir sonraki commit'e geçer, devam et
# Bug bulunana kadar tekrar et

# Bitince temizle
git bisect reset
```

### Otomatik Bisect

```bash
git bisect start HEAD v2.1.0
git bisect run npm test
# Script exit 0 = good, exit 1-127 = bad
```

---

## 5. Worktree — Paralel Çalışma

```bash
# Mevcut worktree'leri listele
git worktree list

# Yeni worktree ekle (var olan branch)
git worktree add ../proje-hotfix hotfix/critical-bug

# Yeni worktree + yeni branch
git worktree add -b bugfix/urgent ../proje-bugfix main

# Worktree'yi kaldır
git worktree remove ../proje-hotfix

# Stale worktree'leri temizle
git worktree prune
```

### Paralel Geliştirme Workflow

```bash
# Ana proje dizini
cd ~/projects/talent-architect

# Urgent hotfix için ayrı dizin
git worktree add ../ta-hotfix hotfix/auth-bypass
cd ../ta-hotfix
# Fix'i yap ve commit et
git push origin hotfix/auth-bypass

# Ana çalışmaya kesintisiz dön
cd ~/projects/talent-architect
git fetch origin
git cherry-pick hotfix/auth-bypass

# Temizle
git worktree remove ../ta-hotfix
```

---

## 6. Reflog — Kurtarma Ağı

```bash
# Reflog'u gör
git reflog
# Örnek çıktı:
# abc123 HEAD@{0}: reset: moving to HEAD~5  ← Hata burada
# def456 HEAD@{1}: commit: my important work

# Kayıp commit'leri kurtar
git reset --hard def456

# Veya yeni branch oluştur
git branch kurtarilan-branch def456

# Silinen branch'i geri getir (90 gün içinde)
git reflog
git branch silinen-branch abc123
```

---

## 7. Önemli Kurallar

```bash
# Güvenli force push — başkasının çalışmasını ezmez
git push --force-with-lease origin feature/branch

# Riskli operasyon öncesi backup
git branch backup-branch
git rebase -i main
# Sorun çıkarsa:
git reset --hard backup-branch
```

### Rebase vs Merge Kararı

| Durum                             | Tercih              |
| --------------------------------- | ------------------- |
| Push edilmemiş local commit'ler   | Rebase              |
| Feature branch'i güncel tutma     | Rebase              |
| Tamamlanmış feature'ı main'e alma | Merge               |
| Public/paylaşılan branch          | Merge (asla rebase) |

### Kurtarma Komutları

```bash
# Operasyonu iptal et
git rebase --abort
git merge --abort
git cherry-pick --abort
git bisect reset

# Son commit'i geri al (değişiklikleri koru)
git reset --soft HEAD^

# Son commit'i geri al (değişiklikleri sil)
git reset --hard HEAD^

# Dosyayı belirli commit'ten geri yükle
git restore --source=abc123 path/to/file
```

---

## 8. Anti-Pattern'lar

```bash
# ❌ Public branch'i rebase etme
git checkout main
git rebase feature/branch  # ASLA

# ❌ --force-with-lease olmadan force push
git push --force  # TEHLİKELİ

# ❌ Bisect testi temiz olmayan working directory ile
# Bisect öncesi commit veya stash yap

# ❌ Birden fazla şeyi tek commit'te
git commit -m "fix bug, add feature, update styles, refactor code"
```

---

## 8. Conventional Commits Formatı

Proje commit'lerinde tutarlılık için Conventional Commits standardı:

### Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer]
```

### Type Listesi

| Type       | Kullanım                                          |
| ---------- | ------------------------------------------------- |
| `feat`     | Yeni özellik                                      |
| `fix`      | Bug düzeltme                                      |
| `chore`    | Bakım, tool değişikliği                           |
| `docs`     | Yalnızca dokümantasyon                            |
| `style`    | Anlam değiştirmeyen format (whitespace, prettier) |
| `refactor` | Bug fix veya feature değil, kod düzenleme         |
| `perf`     | Performans iyileştirme                            |
| `test`     | Test ekleme veya düzeltme                         |

### Kurallar

- Header **100 karakteri geçmemeli**
- Description nokta/tam durma ile **bitmemeli**
- Imperative present tense: "add" ✅ "added" ❌ "adds" ❌
- Description küçük harfle başlasın
- Body satırları 72 karakterde wrap

### Talent Architect Örnekleri

```bash
# Feature
git commit -m "feat(cv): add PDF export with custom template selection"

# Bug fix
git commit -m "fix(ats): correct score calculation when job description is empty"

# Refactoring
git commit -m "refactor(auth): move session validation to shared lib/auth/session.ts"

# i18n
git commit -m "feat(i18n): add TR/EN translations for new ATS analysis section"

# Breaking change (footer ile)
git commit -m "feat(api): redesign cv upload endpoint response structure

BREAKING CHANGE: Response shape changed from { cvId } to { cv: { id, status } }"

# Chore
git commit -m "chore: update anthropic SDK to 0.78.0"

# Test
git commit -m "test(cv): add unit tests for PDF generation edge cases"
```

### Scope Önerileri (Talent Architect)

```
feat(cv):         CV generation/upload/download
feat(ats):        ATS analysis
feat(chat):        AI chatbot
feat(cover-letter): Ön yazı
feat(calculator): Maaş/kıdem hesaplama
feat(auth):       Kimlik doğrulama
feat(profile):    Profil yönetimi
feat(i18n):       Çeviriler
feat(admin):      Admin paneli
fix(monitoring):  Monitoring sistemi
chore(deps):      Bağımlılık güncellemeleri
```

---

## 9. Changelog Otomasyonu

### Keep a Changelog Formatı

```markdown
# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- Yeni özellik X

## [1.2.0] - 2024-01-15

### Added

- Kullanıcı profili avatar desteği
- Dark mode

### Changed

- Checkout performansı %40 iyileştirildi

### Deprecated

- Eski auth API'si (v2 kullanın)

### Removed

- Legacy ödeme gateway

### Fixed

- Login timeout sorunu (#123)

### Security

- CVE-2024-1234 için bağımlılık güncellemesi

[Unreleased]: https://github.com/user/repo/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/user/repo/compare/v1.1.0...v1.2.0
```

### Conventional Commits → Changelog Eşlemesi

| Commit Tipi                    | CHANGELOG Bölümü | Versiyon Etkisi |
| ------------------------------ | ---------------- | --------------- |
| `feat`                         | Added            | MINOR           |
| `fix`                          | Fixed            | PATCH           |
| `perf`                         | Changed          | PATCH           |
| `refactor`                     | Changed          | (dahil edilmez) |
| `feat!` veya `BREAKING CHANGE` | —                | MAJOR           |
| `docs`, `test`, `chore`, `ci`  | —                | (dahil edilmez) |

### standard-version Kurulumu (Node.js)

```bash
npm install -D standard-version

# package.json
{
  "scripts": {
    "release": "standard-version",
    "release:minor": "standard-version --release-as minor",
    "release:major": "standard-version --release-as major",
    "release:dry": "standard-version --dry-run"
  }
}
```

### semantic-release (Tam Otomasyon)

```javascript
// release.config.js
module.exports = {
  branches: ['main', { name: 'beta', prerelease: true }],
  plugins: [
    '@semantic-release/commit-analyzer',
    '@semantic-release/release-notes-generator',
    ['@semantic-release/changelog', { changelogFile: 'CHANGELOG.md' }],
    [
      '@semantic-release/git',
      {
        assets: ['CHANGELOG.md', 'package.json'],
        message: 'chore(release): ${nextRelease.version} [skip ci]',
      },
    ],
    '@semantic-release/github',
  ],
}
```

### git-cliff (Rust tabanlı, En Hızlı)

```toml
# cliff.toml
[git]
conventional_commits = true
commit_parsers = [
  { message = "^feat", group = "Features" },
  { message = "^fix", group = "Bug Fixes" },
  { message = "^perf", group = "Performance" },
  { message = "^chore\\(release\\)", skip = true },
]
tag_pattern = "v[0-9]*"
```

```bash
git cliff -o CHANGELOG.md              # Tüm geçmişten üret
git cliff v1.0.0..HEAD --unreleased    # Yayımlanmamış değişiklikler
git cliff --dry-run                    # Önizleme
```

### GitHub Actions Release Workflow

```yaml
# .github/workflows/release.yml
name: Release
on:
  push:
    branches: [main]

permissions:
  contents: write

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
          token: ${{ secrets.GITHUB_TOKEN }}

      - uses: actions/setup-node@v4
        with:
          node-version: '22'

      - run: npm ci

      - name: Configure Git
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"

      - name: Run semantic-release
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: npx semantic-release
```

### Best Practices

```
✅ Her commit'te Conventional Commits kuralına uy
✅ BREAKING CHANGE'leri ! ile işaretle (feat!: ...)
✅ Issue numaralarını referans göster (Closes #123)
✅ Release tag'lerini v prefix ile oluştur (v1.2.0)
✅ CHANGELOG.md'yi version control'de tut

❌ CHANGELOG'u manuel düzenleme
❌ Vague commit mesajları ("fix stuff", "update")
❌ Breaking change'i işaretlemeyi atlamak
❌ Release'i CI/CD dışında tetiklemek
```
