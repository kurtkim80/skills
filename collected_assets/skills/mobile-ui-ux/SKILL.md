---
name: mobile-ui-ux
description: >
  iOS-first mobile UI/UX design and implementation guide. Covers 50+ design
  styles, color palette standards, typography system, iOS Human Interface
  Guidelines, touch psychology, performance-conscious layouts, accessibility,
  and a Flutter-specific design system. Use when designing mobile screens,
  iOS/Android UI components, design systems, color palettes, typography,
  dark mode, animations, layouts, spacing, touch targets, glassmorphism,
  neumorphism, minimalism, gestures, or safe area handling.
version: 2.0.0
allowed-tools: Read, Glob, Grep
---

# Mobile UI/UX — iOS-First Design System

> 10 years of mobile UI/UX expertise. Full compliance with iOS Human Interface
> Guidelines, touch-first design philosophy, and production-grade Flutter implementation.

---

## Questions to Ask Before Designing

Never assume. Ask for clarification when any of the following are undefined:

| Question                            | Why It Matters                                        |
| ----------------------------------- | ----------------------------------------------------- |
| Platform: iOS, Android, or both?    | Affects navigation, gestures, and typography          |
| Target audience?                    | Age and technical proficiency determine UI complexity |
| Is there an existing design system? | Colour, font, and spacing standards                   |
| Accessibility requirements?         | Contrast ratios, font sizes, VoiceOver support        |
| Is dark mode mandatory?             | Drives token architecture decisions                   |
| Which Flutter state management?     | Influences widget structure                           |

---

## Design Style Selection

### Style Categories

**1. Modern iOS Native (Default Recommendation)**
SF Pro typography, system colours, native blur effects, Dynamic Island compatibility, iOS 17+ aesthetics. Recommended for most consumer apps targeting iOS users.

**2. Glassmorphism / Frosted Glass**
Translucent layers, blur effects, subtle borders, light reflections, depth perception. Implemented with `BackdropFilter + ClipRRect + BoxDecoration`. Ideal for premium apps, music players, weather, and finance.

**3. Neumorphism (Soft UI)**
Single background colour, inner and outer shadows, tactile "pressable" feel. Uses monochromatic palettes. Important: validate accessibility — low contrast is a known risk.

**4. Material You (Android-first, cross-platform)**
Dynamic colour, M3 tokens, expressive motion. Colour scheme derived from the user's wallpaper via `MaterialScheme.fromSeed()`.

**5. Minimal / Editorial**
Generous white space, strong typography, limited colour. Used by Notion, Bear, and Things 3.

**6. Dark Native (Premium Dark)**
Pure black (`#000000`) for iOS OLED displays, subtle glow effects, elevated surfaces. Used by Dark Sky, Halide, and VSCO.

---

## Colour System (Flutter Token Architecture)

```dart
// ✅ CORRECT: Semantic token system
abstract class AppColors {
  // === PRIMARY PALETTE ===
  static const primary      = Color(0xFF007AFF); // iOS System Blue
  static const primaryLight = Color(0xFF409CFF);
  static const primaryDark  = Color(0xFF0055D4);

  // === LIGHT MODE ===
  static const lightBackground      = Color(0xFFF2F2F7);   // iOS Gray 6
  static const lightSurface         = Color(0xFFFFFFFF);
  static const lightSurfaceElevated = Color(0xFFFFFFFF);
  static const lightLabel           = Color(0xFF000000);
  static const lightLabelSecondary  = Color(0x993C3C43);   // 60% opacity
  static const lightLabelTertiary   = Color(0x4C3C3C43);   // 30% opacity
  static const lightSeparator       = Color(0x493C3C43);
  static const lightFill            = Color(0x33787880);

  // === DARK MODE ===
  static const darkBackground      = Color(0xFF000000);
  static const darkSurface         = Color(0xFF1C1C1E);
  static const darkSurfaceElevated = Color(0xFF2C2C2E);
  static const darkLabel           = Color(0xFFFFFFFF);
  static const darkLabelSecondary  = Color(0x99EBEBF5);
  static const darkLabelTertiary   = Color(0x4CEBEBF5);
  static const darkSeparator       = Color(0x59545458);
  static const darkFill            = Color(0x33787880);

  // === iOS SYSTEM COLOURS ===
  static const systemBlue   = Color(0xFF007AFF);
  static const systemGreen  = Color(0xFF34C759);
  static const systemRed    = Color(0xFFFF3B30);
  static const systemOrange = Color(0xFFFF9500);
  static const systemYellow = Color(0xFFFFCC00);
  static const systemPurple = Color(0xFFAF52DE);
  static const systemTeal   = Color(0xFF5AC8FA);
  static const systemIndigo = Color(0xFF5856D6);

  // === FUNCTIONAL ===
  static const success = systemGreen;
  static const error   = systemRed;
  static const warning = systemOrange;
  static const info    = systemBlue;
}

class AppTheme {
  static ThemeData light() => ThemeData(
    useMaterial3: true,
    colorScheme: ColorScheme.light(
      primary:      AppColors.primary,
      surface:      AppColors.lightSurface,
      background:   AppColors.lightBackground,
      error:        AppColors.error,
      onPrimary:    Colors.white,
      onSurface:    AppColors.lightLabel,
      onBackground: AppColors.lightLabel,
    ),
    fontFamily: 'SF Pro Display',
  );

  static ThemeData dark() => ThemeData(
    useMaterial3: true,
    colorScheme: ColorScheme.dark(
      primary:      AppColors.primary,
      surface:      AppColors.darkSurface,
      background:   AppColors.darkBackground,
      error:        AppColors.error,
      onPrimary:    Colors.white,
      onSurface:    AppColors.darkLabel,
      onBackground: AppColors.darkLabel,
    ),
    scaffoldBackgroundColor: AppColors.darkBackground,
  );
}
```

---

## Typography System

```dart
// iOS SF Pro — Android Roboto/Product Sans
abstract class AppTypography {
  static const largeTitle  = TextStyle(fontSize: 34, fontWeight: FontWeight.w700, letterSpacing: 0.37, height: 1.21);
  static const title1      = TextStyle(fontSize: 28, fontWeight: FontWeight.w700, letterSpacing: 0.36);
  static const title2      = TextStyle(fontSize: 22, fontWeight: FontWeight.w700, letterSpacing: 0.35);
  static const title3      = TextStyle(fontSize: 20, fontWeight: FontWeight.w600, letterSpacing: 0.38);
  static const headline    = TextStyle(fontSize: 17, fontWeight: FontWeight.w600, letterSpacing: -0.43);
  static const body        = TextStyle(fontSize: 17, fontWeight: FontWeight.w400, letterSpacing: -0.43, height: 1.47);
  static const callout     = TextStyle(fontSize: 16, fontWeight: FontWeight.w400, letterSpacing: -0.32);
  static const subheadline = TextStyle(fontSize: 15, fontWeight: FontWeight.w400, letterSpacing: -0.23);
  static const footnote    = TextStyle(fontSize: 13, fontWeight: FontWeight.w400, letterSpacing: -0.08);
  static const caption1    = TextStyle(fontSize: 12, fontWeight: FontWeight.w400, letterSpacing: 0);
  static const caption2    = TextStyle(fontSize: 11, fontWeight: FontWeight.w400, letterSpacing: 0.06);
}
```

---

## Spacing System (8pt Grid)

```dart
abstract class AppSpacing {
  static const double xs  = 4.0;
  static const double sm  = 8.0;
  static const double md  = 12.0;
  static const double lg  = 16.0;   // Primary unit
  static const double xl  = 20.0;
  static const double xl2 = 24.0;
  static const double xl3 = 32.0;
  static const double xl4 = 40.0;
  static const double xl5 = 48.0;
  static const double xl6 = 64.0;

  // Semantic aliases
  static const double screenPadding  = lg;     // 16
  static const double sectionGap     = xl3;    // 32
  static const double cardPadding    = lg;     // 16
  static const double tabBarHeight   = 49.0;   // iOS standard
  static const double navBarHeight   = 44.0;   // iOS standard
  static const double bottomSafeArea = 34.0;   // iPhone X+
}

abstract class AppRadius {
  static const double xs   = 6.0;
  static const double sm   = 10.0;
  static const double md   = 12.0;   // iOS card standard
  static const double lg   = 16.0;
  static const double xl   = 20.0;
  static const double full = 100.0;  // Fully circular
}
```

---

## Touch Psychology & Target Sizes

```
FITTS' LAW: Small target = More missed taps = User frustration

iOS HIG Minimum: 44 × 44 pt  (MANDATORY)
Recommended:     48 × 48 pt
Ideal (comfort): 52 × 52 pt+

THUMB REACH MAP (iPhone 14 Pro):
┌─────────────────────────┐
│ ████████████████░░░░░░░ │ ← Requires stretch (5%)
│ ████████████████░░░░░░░ │
│ ██████████████████████░ │ ← Comfortable (15%)
│ ████████████████████████│ ← Easy (40%)
│ ████████████████████████│
│ ████████████████████████│ ← Very easy — PRIMARY (40%)
│ [   Home   ][   ][   ]  │ ← Tab bar
└─────────────────────────┘
```

```dart
// ✅ CORRECT: Guaranteed minimum touch target
class AppTouchTarget extends StatelessWidget {
  const AppTouchTarget({
    super.key,
    required this.child,
    required this.onTap,
    this.minSize = 44.0,
  });

  final Widget child;
  final VoidCallback onTap;
  final double minSize;

  @override
  Widget build(BuildContext context) => GestureDetector(
    onTap: onTap,
    behavior: HitTestBehavior.opaque,
    child: ConstrainedBox(
      constraints: BoxConstraints(minWidth: minSize, minHeight: minSize),
      child: Center(child: child),
    ),
  );
}
```

---

## iOS Layout Patterns

### Safe Area Management

```dart
class AppScaffold extends StatelessWidget {
  const AppScaffold({
    super.key,
    required this.body,
    this.appBar,
    this.bottomNav,
    this.backgroundColor,
  });

  final Widget body;
  final PreferredSizeWidget? appBar;
  final Widget? bottomNav;
  final Color? backgroundColor;

  @override
  Widget build(BuildContext context) {
    final bottomPadding = MediaQuery.of(context).padding.bottom;

    return Scaffold(
      backgroundColor: backgroundColor,
      appBar: appBar,
      body: body,
      bottomNavigationBar: bottomNav != null
          ? Padding(
              padding: EdgeInsets.only(bottom: bottomPadding),
              child: bottomNav,
            )
          : null,
    );
  }
}
```

### Glassmorphism Card

```dart
class GlassCard extends StatelessWidget {
  const GlassCard({
    super.key,
    required this.child,
    this.blur = 10.0,
    this.opacity = 0.15,
    this.borderRadius,
  });

  final Widget child;
  final double blur;
  final double opacity;
  final BorderRadius? borderRadius;

  @override
  Widget build(BuildContext context) {
    final isDark  = Theme.of(context).brightness == Brightness.dark;
    final radius  = borderRadius ?? BorderRadius.circular(AppRadius.md);

    return ClipRRect(
      borderRadius: radius,
      child: BackdropFilter(
        filter: ImageFilter.blur(sigmaX: blur, sigmaY: blur),
        child: Container(
          decoration: BoxDecoration(
            borderRadius: radius,
            color: isDark
                ? Colors.white.withOpacity(opacity)
                : Colors.white.withOpacity(opacity + 0.1),
            border: Border.all(
              color: isDark
                  ? Colors.white.withOpacity(0.2)
                  : Colors.white.withOpacity(0.6),
              width: 0.5,
            ),
            boxShadow: [
              BoxShadow(
                color: Colors.black.withOpacity(isDark ? 0.3 : 0.1),
                blurRadius: 20,
                offset: const Offset(0, 4),
              ),
            ],
          ),
          child: child,
        ),
      ),
    );
  }
}
```

### iOS Bottom Sheet

```dart
void showAppBottomSheet({
  required BuildContext context,
  required Widget child,
  bool isDismissible = true,
}) {
  showModalBottomSheet(
    context: context,
    isDismissible: isDismissible,
    isScrollControlled: true,
    backgroundColor: Colors.transparent,
    builder: (context) => Container(
      decoration: BoxDecoration(
        color: Theme.of(context).colorScheme.surface,
        borderRadius: const BorderRadius.vertical(top: Radius.circular(20)),
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          // iOS drag handle
          Padding(
            padding: const EdgeInsets.only(top: 12, bottom: 8),
            child: Container(
              width: 36,
              height: 5,
              decoration: BoxDecoration(
                color: AppColors.lightLabelTertiary,
                borderRadius: BorderRadius.circular(2.5),
              ),
            ),
          ),
          child,
          SizedBox(height: MediaQuery.of(context).padding.bottom),
        ],
      ),
    ),
  );
}
```

---

## Design Token Generation

When the design system changes, use the following template to translate colour, typography, and spacing tokens into Dart code without manual copying.

```dart
// This file is generated from the design token source.
// Do not edit manually — update the source file instead.

abstract class DesignTokens {
  // === COLOUR TOKENS ===
  static const Color brandPrimary   = Color(0xFF______); // Primary-500
  static const Color brandSecondary = Color(0xFF______); // Secondary-500
  static const Color brandAccent    = Color(0xFF______); // Accent-500

  // Greyscale
  static const Color gray50  = Color(0xFFF9FAFB);
  static const Color gray100 = Color(0xFFF3F4F6);
  static const Color gray200 = Color(0xFFE5E7EB);
  static const Color gray500 = Color(0xFF6B7280);
  static const Color gray900 = Color(0xFF111827);

  // === SHADOW TOKENS ===
  static const List<BoxShadow> shadowSm = [
    BoxShadow(color: Color(0x0A000000), blurRadius: 4,  offset: Offset(0, 1)),
  ];
  static const List<BoxShadow> shadowMd = [
    BoxShadow(color: Color(0x0F000000), blurRadius: 8,  offset: Offset(0, 2)),
    BoxShadow(color: Color(0x0A000000), blurRadius: 4,  offset: Offset(0, 1)),
  ];
  static const List<BoxShadow> shadowLg = [
    BoxShadow(color: Color(0x14000000), blurRadius: 16, offset: Offset(0, 4)),
    BoxShadow(color: Color(0x0A000000), blurRadius: 8,  offset: Offset(0, 2)),
  ];
}
```

---

## Accessibility

Never hardcode colours. Always retrieve them from the theme:

```dart
// ❌ WRONG
color: Colors.white,

// ✅ CORRECT
color: Theme.of(context).colorScheme.onSurface,
```

All images must have a `semanticLabel`. The label should describe meaning, not the object itself:

```dart
// ❌ Wrong
Image(semanticLabel: 'heart icon'),

// ✅ Correct
Image(semanticLabel: 'Add to favourites'),
```

Colour must never be the sole carrier of information. Error states should use an icon, text, or shape change in addition to colour.

WCAG AA minimum contrast ratio: **4.5:1** for body text.

---

## Pre-Delivery Checklist

**Visual Quality**

- [ ] No emojis used as icons (SVG/Icon used instead)
- [ ] All colours sourced from semantic tokens
- [ ] Typography scale consistent (AppTypography used)
- [ ] Spacing aligns with 8pt grid
- [ ] Dark mode tested with no visual issues
- [ ] Corner radius consistent (AppRadius used)

**Touch & Interaction**

- [ ] All interactive elements are at least 44 × 44 pt
- [ ] Primary CTA is in the thumb zone (bottom 40% of screen)
- [ ] All interactive elements have press-state feedback
- [ ] Transitions are between 200–350 ms

**iOS Specific**

- [ ] Safe areas handled (top and bottom)
- [ ] Navigation follows iOS standard (centred title, back gesture)
- [ ] Bottom sheet has drag handle
- [ ] Keyboard handled with `resizeToAvoidBottomInset`
- [ ] No interference with Dynamic Island or notch

**Dark Mode Contrast**

- [ ] Light mode text contrast is at least 4.5:1
- [ ] Glass/transparent elements are visible in light mode
- [ ] Borders are visible in both modes
