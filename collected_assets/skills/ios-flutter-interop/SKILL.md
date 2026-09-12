---
name: ios-flutter-interop
description: >
  iOS platform integration and native interop for Flutter applications.
  MethodChannel, EventChannel, platform-specific UI behaviour, iOS App
  Extensions (widget, share, notification), Keychain, HealthKit, Face ID /
  Touch ID, and App Store submission guide. Use when: writing iOS platform
  code, integrating native features, platform channel, Swift-Dart bridge,
  iOS notifications, deep link, Universal Link, app extension, TestFlight,
  App Store review, iOS permissions.
version: 1.0.0
allowed-tools: Read, Glob, Grep
---

# iOS–Flutter Interop

> Bridging the Flutter application to the iOS native layer:
> platform channels, native UI, extensions, and the App Store submission process.

---

## When Is Native iOS Code Required?

Flutter's widget layer handles a great deal, but certain iOS capabilities mandate Swift code:

| Requires native code           | Flutter package is sufficient                       |
| ------------------------------ | --------------------------------------------------- |
| Keychain / Secure Enclave      | Core UI components                                  |
| Face ID / Touch ID (LocalAuth) | HTTP requests                                       |
| HealthKit, CoreMotion          | Push notification permission (`firebase_messaging`) |
| HomeKit, ARKit                 | Camera (`camera` package)                           |
| App Extensions (widget, share) | Maps (`google_maps_flutter`)                        |
| BackgroundFetch, silent push   | SQLite, Hive                                        |
| Custom URL scheme registration | File management                                     |

---

## Platform Channel Fundamentals

### MethodChannel — Single invocation

**Dart side:**

```dart
class BiometricService {
  static const _channel = MethodChannel('com.company.app/biometric');

  Future<bool> authenticate({required String reason}) async {
    try {
      final result = await _channel.invokeMethod<bool>(
        'authenticate',
        {'reason': reason},
      );
      return result ?? false;
    } on PlatformException catch (e) {
      throw BiometricFailure(e.message ?? 'Authentication failed');
    }
  }
}
```

**Swift side (AppDelegate.swift or a dedicated handler file):**

```swift
import Flutter
import LocalAuthentication

class BiometricChannelHandler {
  static func register(with controller: FlutterViewController) {
    let channel = FlutterMethodChannel(
      name: "com.company.app/biometric",
      binaryMessenger: controller.binaryMessenger
    )

    channel.setMethodCallHandler { call, result in
      guard call.method == "authenticate" else {
        result(FlutterMethodNotImplemented)
        return
      }

      let reason = (call.arguments as? [String: Any])?["reason"] as? String
                   ?? "Verify your identity"
      let context = LAContext()
      var error: NSError?

      guard context.canEvaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, error: &error) else {
        result(FlutterError(
          code: "BIOMETRIC_UNAVAILABLE",
          message: error?.localizedDescription,
          details: nil
        ))
        return
      }

      context.evaluatePolicy(
        .deviceOwnerAuthenticationWithBiometrics,
        localizedReason: reason
      ) { success, authError in
        DispatchQueue.main.async {
          if success {
            result(true)
          } else {
            result(FlutterError(
              code: "AUTH_FAILED",
              message: authError?.localizedDescription,
              details: nil
            ))
          }
        }
      }
    }
  }
}
```

### EventChannel — Continuous data stream

```dart
// Dart side: continuously updated data such as a step counter
class MotionService {
  static const _channel = EventChannel('com.company.app/motion');

  Stream<int> get stepCountStream =>
      _channel.receiveBroadcastStream().map((event) => event as int);
}

// Swift side
class MotionStreamHandler: NSObject, FlutterStreamHandler {
  private let pedometer = CMPedometer()

  func onListen(withArguments arguments: Any?,
                eventSink: @escaping FlutterEventSink) -> FlutterError? {
    pedometer.startUpdates(from: Date()) { data, error in
      if let steps = data?.numberOfSteps {
        eventSink(steps.intValue)
      }
    }
    return nil
  }

  func onCancel(withArguments arguments: Any?) -> FlutterError? {
    pedometer.stopUpdates()
    return nil
  }
}
```

---

## iOS Permissions (Info.plist)

Each permission requires two things: an `Info.plist` entry and a runtime request. The description string is shown directly to the user and must be concise and honest.

```xml
<!-- Camera -->
<key>NSCameraUsageDescription</key>
<string>Camera access is needed to take your profile photo.</string>

<!-- Location (while in use) -->
<key>NSLocationWhenInUseUsageDescription</key>
<string>We need your location to show nearby stores.</string>

<!-- Health -->
<key>NSHealthShareUsageDescription</key>
<string>HealthKit data is used to display your daily step count.</string>
<key>NSHealthUpdateUsageDescription</key>
<string>Permission is needed to save your workout data to Health.</string>

<!-- Face ID -->
<key>NSFaceIDUsageDescription</key>
<string>Face ID is available for quick, secure sign-in.</string>
```

---

## Deep Link and Universal Link

### URL Scheme (Simple, in-app routing)

```xml
<!-- Info.plist -->
<key>CFBundleURLTypes</key>
<array>
  <dict>
    <key>CFBundleURLSchemes</key>
    <array>
      <string>appname</string>
    </array>
  </dict>
</array>
```

```dart
// Flutter side — GoRouter handles deep links automatically
// appname://profile/123 → routes to /profile/123
GoRouter(routes: [...])
```

### Universal Link (Preferred — behaves like a standard web URL)

```json
// apple-app-site-association (must be served over HTTPS)
{
  "applinks": {
    "apps": [],
    "details": [
      {
        "appID": "TEAMID.com.company.app",
        "paths": ["/share/*", "/product/*", "/invite/*"]
      }
    ]
  }
}
```

```xml
<!-- Xcode → Signing & Capabilities → Associated Domains -->
<key>com.apple.developer.associated-domains</key>
<array>
  <string>applinks:company.com</string>
</array>
```

---

## iOS Home Screen Widget (App Extension)

Dart code cannot directly access a widget extension. Data sharing uses an **App Group**.

```swift
// iOS Extension
import WidgetKit
import SwiftUI

struct Provider: TimelineProvider {
  func getSnapshot(in context: Context,
                   completion: @escaping (SimpleEntry) -> Void) {
    // Read data written by Flutter via UserDefaults(suiteName:)
    let defaults = UserDefaults(suiteName: "group.com.company.app")
    let name = defaults?.string(forKey: "user_name") ?? "User"
    completion(SimpleEntry(date: Date(), userName: name))
  }

  func getTimeline(in context: Context,
                   completion: @escaping (Timeline<SimpleEntry>) -> Void) {
    let entry = SimpleEntry(date: Date(), userName: "User")
    completion(Timeline(entries: [entry], policy: .atEnd))
  }

  func placeholder(in context: Context) -> SimpleEntry {
    SimpleEntry(date: Date(), userName: "User")
  }
}
```

```dart
// Flutter side: write data to the shared App Group
class WidgetDataService {
  static const _channel = MethodChannel('com.company.app/widget');

  Future<void> updateWidget({required String userName}) async {
    await _channel.invokeMethod('updateWidget', {'user_name': userName});
    // Swift side writes to UserDefaults(suiteName:) and calls
    // WidgetCenter.shared.reloadAllTimelines()
  }
}
```

---

## App Store Submission Checklist

### Before Building

- [ ] Version number and build number updated in `pubspec.yaml`
- [ ] All debug `print()` calls and test code removed
- [ ] API keys hidden via `flutter_dotenv` or equivalent
- [ ] `NSAppTransportSecurity` configured restrictively for production
- [ ] `Info.plist` contains usage descriptions for every requested permission
- [ ] Splash screen and App Icon present in all required sizes

### TestFlight

- [ ] Internal testing (team) — approval typically takes 1–2 days
- [ ] External testing (beta users) — requires an Apple review
- [ ] At least one week of beta testing completed

### App Store Connect

- [ ] Screenshots: iPhone 6.9" (mandatory) + iPad (mandatory for universal apps)
- [ ] App Preview video (optional but improves conversion)
- [ ] App description complies with App Store Review Guidelines
- [ ] Privacy policy URL provided
- [ ] Privacy Nutrition Labels accurately completed
- [ ] Review notes include test account credentials

### Common Rejection Reasons

```
Guideline 2.1   → Crash or major bug (test thoroughly on TestFlight first)
Guideline 4.0   → Too similar to existing apps (demonstrate unique value)
Guideline 5.1.1 → Unnecessary permission requests (request only what is needed)
Guideline 3.1.1 → External payment used instead of in-app purchase
Guideline 2.3.3 → Placeholder content or "demo" / "test" text present
```

---

## Package Alternatives: Native vs Flutter

| Requirement               | Flutter Package          | Native Required?           |
| ------------------------- | ------------------------ | -------------------------- |
| Biometric authentication  | `local_auth`             | No                         |
| Keychain / secure storage | `flutter_secure_storage` | No                         |
| Push notifications        | `firebase_messaging`     | No                         |
| HealthKit                 | —                        | **Yes** (platform channel) |
| Home Screen Widget        | —                        | **Yes** (App Extension)    |
| Siri Shortcuts            | —                        | **Yes** (platform channel) |
| NFC                       | `nfc_manager`            | No                         |
| In-App Purchase           | `in_app_purchase`        | No                         |
| Sign in with Apple        | `sign_in_with_apple`     | No                         |
