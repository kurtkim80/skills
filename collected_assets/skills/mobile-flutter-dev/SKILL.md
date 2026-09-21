---
name: mobile-flutter-dev
description: Build, debug, refactor, or test Flutter and Dart applications for iOS and Android. Use for widgets, state, navigation, networking, persistence, animation, performance, platform behavior, or Flutter-specific tooling; inspect the project's current architecture and package versions before choosing patterns.
allowed-tools: Read, Glob, Grep
---

# Flutter Mobile Development

Implement Flutter features that fit the existing application architecture and behave correctly on every supported platform.

## Inspect First

Read `pubspec.yaml`, analysis options, routing, state management, dependency injection, theme, localization, platform targets, and nearby feature code. Do not introduce a second state, routing, serialization, or dependency-injection approach without a demonstrated need.

Verify current Flutter, Dart, and package APIs before making version-sensitive changes.

## Implementation Principles

- Keep widgets focused on composition and interaction; move business rules to the project's established domain or service layer.
- Model loading, empty, error, success, offline, permission, and partial states explicitly.
- Preserve immutable state and predictable ownership.
- Use keys intentionally for identity and state preservation.
- Avoid unnecessary rebuilds, synchronous work on the UI isolate, and unbounded lists.
- Dispose controllers, subscriptions, focus nodes, and platform resources.
- Respect safe areas, text scaling, localization, keyboard navigation, semantics, and platform conventions.
- Use adaptive behavior where iOS and Android expectations differ materially.

## Data and Navigation

Keep transport models separate from durable domain meaning where that distinction exists. Validate external data, handle cancellation and retry boundaries, and avoid hiding failures behind empty results. Define deep links, restoration, authentication redirects, and back-stack behavior for navigation changes.

## Native Integration

Use existing plugins before writing platform channels. When native code is necessary, define typed channel contracts, thread and lifecycle behavior, error mapping, permission handling, and tests on real target platforms. Use the ios-flutter-interop skill for substantial iOS-specific integration.

## Verification

Run formatting, static analysis, relevant tests, and a build or device check proportionate to the change. Exercise narrow screens, large text, dark mode, slow or offline networks, lifecycle transitions, denied permissions, and platform-specific behavior when relevant. Inspect runtime logs and performance evidence before claiming improvement.

Report changed behavior, checks performed, and platform limitations or unverified assumptions.
