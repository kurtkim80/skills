---
name: ios-developer
description: Build, debug, refactor, or review native iOS applications with Swift, SwiftUI, and platform frameworks. Use for iOS-specific UI, data, networking, concurrency, lifecycle, permissions, performance, testing, or App Store delivery; verify the deployment target and current Apple APIs.
---

# iOS Developer

Implement native iOS behavior that fits the application's existing architecture, supported OS range, privacy model, and Apple platform conventions.

## Inspect First

Review the Xcode project, deployment target, Swift language mode, package dependencies, signing, entitlements, app lifecycle, navigation, state ownership, persistence, networking, localization, and test setup. Do not introduce a second architecture or dependency mechanism without a demonstrated need.

Apple APIs and review requirements change; consult current official documentation for version-sensitive work.

## Implementation Principles

- Keep SwiftUI view bodies focused on composition; move business logic to testable types using the project's established pattern.
- Use structured concurrency with clear task ownership, cancellation, actor isolation, and main-thread UI updates.
- Model loading, empty, error, offline, permission, and partial states.
- Respect Dynamic Type, VoiceOver, contrast, Reduce Motion, safe areas, localization, and platform navigation behavior.
- Avoid force unwraps and hidden global state in production paths.
- Use platform storage appropriate to data sensitivity and lifecycle; protect secrets with Keychain or the project's secure abstraction.
- Request permissions in context and explain denied or restricted states.

## Integration

Validate server data and map transport errors into domain behavior. Define background execution, deep links, notifications, widgets, extensions, and shared containers explicitly when relevant. Keep extension targets within their memory, lifecycle, and API constraints.

## Performance

Measure launch, scrolling, memory, energy, networking, and persistence before optimizing. Avoid blocking the main actor, repeated expensive view work, oversized assets, and unbounded caches. Use Instruments or available metrics for consequential claims.

## Verification

Run formatting or linting, builds, and relevant unit or UI tests. Exercise supported OS versions and devices, dark mode, large text, VoiceOver, denied permissions, offline behavior, lifecycle transitions, deep links, and release configuration as appropriate.

For distribution, verify signing, privacy manifests or disclosures, entitlements, export compliance, store metadata, and current review requirements.
