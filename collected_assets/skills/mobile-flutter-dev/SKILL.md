---
name: flutter-mobile-dev
description: >
  Native Flutter & Dart development for iOS and Android. Covers widgets,
  state management (Provider, BLoC, Riverpod), navigation (GoRouter),
  API integration, local storage, animations, and platform-specific
  implementations. Use when building Flutter screens, components, features,
  or resolving Flutter/Dart-specific issues. Triggers: flutter, dart, widget,
  stateful, stateless, provider, bloc, riverpod, gorouter, pubspec, hot reload,
  flutter build, flutter run.
version: 2.0.0
allowed-tools: Read, Glob, Grep
---

# Flutter Mobile Development

> Production-grade iOS and Android apps built with 7+ years of Flutter & Dart expertise.
> iOS-first design, performance-conscious patterns, and full platform convention compliance.

---

## Activation Conditions

This skill applies when:

- Building Flutter widgets, screens, or features
- Selecting or implementing a state management solution
- Setting up navigation and routing
- Integrating APIs or local storage
- Writing platform-specific (iOS/Android) code
- Managing pubspec.yaml dependencies
- Optimising Flutter performance
- Implementing animations and transitions

---

## Project Structure (Flutter Template Standard)

```
lib/
├── core/
│   ├── constants/          # AppColors, AppSizes, AppStrings
│   ├── extensions/         # BuildContext, String, DateTime extensions
│   ├── theme/              # AppTheme, ThemeData
│   ├── router/             # GoRouter configuration
│   ├── network/            # Dio, interceptors, API client
│   └── utils/              # Helpers, validators
├── features/
│   └── [feature_name]/
│       ├── data/
│       │   ├── models/     # JSON serializable models
│       │   ├── repositories/
│       │   └── datasources/
│       ├── domain/
│       │   ├── entities/
│       │   ├── repositories/ (abstract)
│       │   └── usecases/
│       └── presentation/
│           ├── bloc/       # BLoC or Cubit
│           ├── screens/
│           └── widgets/
├── shared/
│   ├── widgets/            # Reusable UI components
│   └── services/           # Shared services
└── main.dart
```

---

## State Management

### 1. BLoC Pattern (Recommended for large features)

```dart
// ✅ CORRECT: Simple state management with Cubit
class AuthCubit extends Cubit<AuthState> {
  AuthCubit(this._authRepository) : super(const AuthState.initial());

  final AuthRepository _authRepository;

  Future<void> login(String email, String password) async {
    emit(const AuthState.loading());

    final result = await _authRepository.login(
      email: email,
      password: password,
    );

    result.fold(
      (failure) => emit(AuthState.error(failure.message)),
      (user) => emit(AuthState.success(user)),
    );
  }
}

// Type-safe state with sealed class
@freezed
sealed class AuthState with _$AuthState {
  const factory AuthState.initial() = _Initial;
  const factory AuthState.loading() = _Loading;
  const factory AuthState.success(User user) = _Success;
  const factory AuthState.error(String message) = _Error;
}
```

### 2. Riverpod (Recommended for medium features)

```dart
// ✅ CORRECT: Async state with AsyncNotifier
@riverpod
class ProductList extends _$ProductList {
  @override
  Future<List<Product>> build() async {
    return ref.watch(productRepositoryProvider).getProducts();
  }

  Future<void> refresh() async {
    state = const AsyncValue.loading();
    state = await AsyncValue.guard(
      () => ref.read(productRepositoryProvider).getProducts(),
    );
  }
}

// Widget usage
class ProductScreen extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final productsAsync = ref.watch(productListProvider);

    return productsAsync.when(
      data: (products) => ProductGridView(products: products),
      loading: () => const AppLoadingIndicator(),
      error: (error, _) => AppErrorWidget(message: error.toString()),
    );
  }
}
```

### 3. Provider (Suitable for simple, small features)

```dart
// ✅ CORRECT: Simple state with ChangeNotifier
class CartProvider extends ChangeNotifier {
  final List<CartItem> _items = [];

  List<CartItem> get items => List.unmodifiable(_items);
  int get itemCount => _items.length;
  double get total => _items.fold(0, (sum, item) => sum + item.price);

  void addItem(Product product) {
    final existingIndex = _items.indexWhere((i) => i.productId == product.id);

    if (existingIndex >= 0) {
      _items[existingIndex] = _items[existingIndex].copyWith(
        quantity: _items[existingIndex].quantity + 1,
      );
    } else {
      _items.add(CartItem.fromProduct(product));
    }
    notifyListeners();
  }

  void removeItem(String productId) {
    _items.removeWhere((item) => item.productId == productId);
    notifyListeners();
  }
}
```

---

## Navigation (GoRouter)

```dart
// ✅ CORRECT: Type-safe navigation with GoRouter
final router = GoRouter(
  initialLocation: AppRoutes.splash,
  redirect: (context, state) {
    final isAuthenticated = context.read<AuthCubit>().state is AuthSuccess;
    final isAuthRoute = state.matchedLocation.startsWith('/auth');

    if (!isAuthenticated && !isAuthRoute) return AppRoutes.login;
    if (isAuthenticated && isAuthRoute) return AppRoutes.home;
    return null;
  },
  routes: [
    GoRoute(
      path: AppRoutes.home,
      builder: (context, state) => const HomeScreen(),
      routes: [
        GoRoute(
          path: 'product/:id',
          builder: (context, state) => ProductDetailScreen(
            productId: state.pathParameters['id']!,
          ),
        ),
      ],
    ),
    ShellRoute(
      builder: (context, state, child) => MainShell(child: child),
      routes: [
        GoRoute(
          path: AppRoutes.discover,
          builder: (_, __) => const DiscoverScreen(),
        ),
        GoRoute(
          path: AppRoutes.profile,
          builder: (_, __) => const ProfileScreen(),
        ),
      ],
    ),
  ],
);

abstract class AppRoutes {
  static const splash   = '/splash';
  static const login    = '/auth/login';
  static const home     = '/home';
  static const discover = '/discover';
  static const profile  = '/profile';
}
```

---

## Network Layer (Dio)

```dart
// ✅ CORRECT: Dio setup with interceptors
class ApiClient {
  late final Dio _dio;

  ApiClient({required String baseUrl, required TokenService tokenService}) {
    _dio = Dio(
      BaseOptions(
        baseUrl: baseUrl,
        connectTimeout: const Duration(seconds: 30),
        receiveTimeout: const Duration(seconds: 30),
        headers: {'Content-Type': 'application/json'},
      ),
    );

    _dio.interceptors.addAll([
      AuthInterceptor(tokenService),
      RetryInterceptor(dio: _dio, retries: 3),
      LogInterceptor(requestBody: true, responseBody: kDebugMode),
    ]);
  }

  Future<Either<Failure, T>> get<T>(
    String path, {
    Map<String, dynamic>? queryParameters,
    T Function(Map<String, dynamic>)? fromJson,
  }) async {
    try {
      final response = await _dio.get(path, queryParameters: queryParameters);
      return Right(fromJson != null ? fromJson(response.data) : response.data);
    } on DioException catch (e) {
      return Left(e.toFailure());
    }
  }
}
```

---

## Local Storage

```dart
// ✅ CORRECT: Type-safe local storage with Hive
@HiveType(typeId: 0)
class UserPreferences extends HiveObject {
  @HiveField(0)
  late String theme;

  @HiveField(1)
  late String language;

  @HiveField(2)
  late bool notificationsEnabled;
}

// Secure storage — token management
class SecureStorageService {
  final FlutterSecureStorage _storage;

  SecureStorageService(this._storage);

  Future<void> saveToken(String token) async =>
      _storage.write(key: 'auth_token', value: token);

  Future<String?> getToken() async =>
      _storage.read(key: 'auth_token');

  Future<void> deleteToken() async =>
      _storage.delete(key: 'auth_token');
}
```

---

## Performance Rules

### Mandatory Optimisations

```dart
// 1. List rendering
class ProductList extends StatelessWidget {
  const ProductList({super.key, required this.products});
  final List<Product> products;

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      itemExtent: 80.0,               // ✅ Fixed height for better performance
      itemCount: products.length,
      addAutomaticKeepAlives: false,  // ✅ Performance
      addRepaintBoundaries: false,
      itemBuilder: (context, index) => ProductListTile(
        key: ValueKey(products[index].id), // ✅ Stable key
        product: products[index],
      ),
    );
  }
}

// 2. Const constructors — everywhere possible
class AppButton extends StatelessWidget {
  const AppButton({  // ✅ const constructor
    super.key,
    required this.label,
    required this.onPressed,
    this.isLoading = false,
  });

  final String label;
  final VoidCallback? onPressed;
  final bool isLoading;

  @override
  Widget build(BuildContext context) => ...;
}

// 3. RepaintBoundary — isolate heavy animations
RepaintBoundary(
  child: AnimatedProgressRing(progress: value),
)

// 4. Image caching
CachedNetworkImage(
  imageUrl: product.imageUrl,
  placeholder: (_, __) => const ShimmerBox(),
  errorWidget: (_, __, ___) => const ProductPlaceholder(),
  memCacheWidth: 400, // Limit decode size
)
```

### Common Anti-Patterns

```dart
// ❌ WRONG: Creating new objects inside build()
Widget build(BuildContext context) {
  final style = TextStyle(color: Colors.red); // New object on every build!
  return Text('Hello', style: style);
}

// ✅ CORRECT: Use static or const
static const _errorStyle = TextStyle(color: Colors.red);
// or
Text('Hello', style: const TextStyle(color: Colors.red));

// ❌ WRONG: Unnecessary setState
void _updateValue(int value) {
  setState(() { _count = value; }); // Rebuilds entire widget tree
}

// ✅ CORRECT: Minimal rebuild with ValueNotifier
final _count = ValueNotifier<int>(0);
ValueListenableBuilder<int>(
  valueListenable: _count,
  builder: (_, value, __) => Text('$value'),
)
```

---

## Animations

```dart
// ✅ CORRECT: Performant animation with native driver
class FadeSlideIn extends StatefulWidget {
  const FadeSlideIn({super.key, required this.child, this.delay = Duration.zero});
  final Widget child;
  final Duration delay;

  @override
  State<FadeSlideIn> createState() => _FadeSlideInState();
}

class _FadeSlideInState extends State<FadeSlideIn>
    with SingleTickerProviderStateMixin {
  late final AnimationController _controller;
  late final Animation<double> _opacity;
  late final Animation<Offset> _slide;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: const Duration(milliseconds: 400),
      vsync: this,
    );

    _opacity = Tween(begin: 0.0, end: 1.0).animate(
      CurvedAnimation(parent: _controller, curve: Curves.easeOut),
    );

    _slide = Tween(
      begin: const Offset(0, 0.1),
      end: Offset.zero,
    ).animate(CurvedAnimation(parent: _controller, curve: Curves.easeOutCubic));

    Future.delayed(widget.delay, () {
      if (mounted) _controller.forward();
    });
  }

  @override
  void dispose() {
    _controller.dispose(); // ✅ Prevent memory leak
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return FadeTransition(
      opacity: _opacity,
      child: SlideTransition(position: _slide, child: widget.child),
    );
  }
}
```

---

## Core pubspec.yaml Dependencies

```yaml
dependencies:
  flutter:
    sdk: flutter

  # State Management
  flutter_bloc: ^8.1.6
  riverpod: ^2.5.1
  flutter_riverpod: ^2.5.1

  # Navigation
  go_router: ^14.2.7

  # Network
  dio: ^5.7.0
  retrofit: ^4.4.1

  # Storage
  hive_flutter: ^1.1.0
  flutter_secure_storage: ^9.2.2
  shared_preferences: ^2.3.3

  # Serialisation
  freezed_annotation: ^2.4.4
  json_annotation: ^4.9.0

  # UI
  cached_network_image: ^3.4.1
  shimmer: ^3.0.0
  lottie: ^3.1.3
  gap: ^3.0.1

  # Utilities
  dartz: ^0.10.1
  equatable: ^2.0.7
  intl: ^0.19.0
  uuid: ^4.5.1

dev_dependencies:
  flutter_test:
    sdk: flutter
  build_runner: ^2.4.13
  freezed: ^2.5.7
  json_serializable: ^6.8.0
  retrofit_generator: ^9.1.4
  hive_generator: ^2.0.1
  flutter_lints: ^5.0.0
  mocktail: ^1.0.4
```

---

## Pre-Delivery Checklist

**Code Quality**

- [ ] All public APIs are documented
- [ ] `dispose()` methods present for controllers and subscriptions
- [ ] `const` constructors used throughout
- [ ] `ValueKey` added to long lists
- [ ] Error states handled

**Platform**

- [ ] iOS safe areas handled with `SafeArea` or `MediaQuery.padding`
- [ ] Android back button/gesture handled
- [ ] Keyboard handled with `resizeToAvoidBottomInset`
- [ ] Dark mode tested
- [ ] Accessibility font sizes tested

**Performance**

- [ ] `ListView.builder` used for large lists
- [ ] `RepaintBoundary` added for heavy animations
- [ ] Images cached
- [ ] `build()` method contains no side effects

**Testing**

- [ ] Unit tests: repositories and use cases
- [ ] Widget tests: critical UI components
- [ ] Integration tests: primary user flows
