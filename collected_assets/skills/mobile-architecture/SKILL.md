---
name: mobile-architecture
description: >
  Mobile-first Clean Architecture and Domain Driven Design for Flutter apps.
  Repository pattern, use case layer, dependency injection (GetIt/Injectable),
  error handling (Either/Failure), feature-sliced project structure, and test
  strategy. Use when making architecture decisions, setting up Clean Architecture,
  implementing repository pattern, choosing dependency injection, defining domain
  entities, structuring use cases, writing Either/Failure error handling, or
  establishing a test strategy.
version: 2.0.0
allowed-tools: Read, Glob, Grep
---

# Mobile Architecture — Clean Architecture for Flutter

> Testable, maintainable Flutter applications built on SOLID principles,
> DDD, and a mobile-first mindset.

---

## Layered Architecture

```
┌─────────────────────────────────────────────────────┐
│                  PRESENTATION LAYER                  │
│  Screens → Widgets → BLoC/Cubit/Provider            │
│  (UI state management, user interactions)            │
├─────────────────────────────────────────────────────┤
│                   DOMAIN LAYER                       │
│  Entities → Use Cases → Repository Interfaces       │
│  (Business logic — platform independent)             │
├─────────────────────────────────────────────────────┤
│                    DATA LAYER                        │
│  Models → Repository Implementations → Data Sources │
│  (API, local DB, cache)                              │
└─────────────────────────────────────────────────────┘

DEPENDENCY DIRECTION: Presentation → Domain ← Data
The Domain layer depends on nothing.
```

---

## Feature-Sliced Project Structure

```
lib/
├── core/
│   ├── di/
│   │   └── injection.dart
│   ├── error/
│   │   ├── exceptions.dart
│   │   └── failures.dart
│   ├── network/
│   │   ├── api_client.dart
│   │   └── network_info.dart
│   ├── constants/
│   ├── extensions/
│   ├── theme/
│   ├── router/
│   └── utils/
│
├── features/
│   └── auth/
│       ├── data/
│       │   ├── datasources/
│       │   │   ├── auth_remote_datasource.dart
│       │   │   └── auth_local_datasource.dart
│       │   ├── models/
│       │   │   └── user_model.dart
│       │   └── repositories/
│       │       └── auth_repository_impl.dart
│       ├── domain/
│       │   ├── entities/
│       │   │   └── user.dart
│       │   ├── repositories/
│       │   │   └── auth_repository.dart    # Abstract
│       │   └── usecases/
│       │       ├── login_usecase.dart
│       │       └── logout_usecase.dart
│       └── presentation/
│           ├── bloc/
│           ├── screens/
│           └── widgets/
│
├── shared/
│   ├── widgets/
│   └── services/
│
└── main.dart
```

---

## Domain Layer

### Entity (Pure Dart — no external dependencies)

```dart
// ✅ CORRECT: Immutable entity with Equatable
class User extends Equatable {
  const User({
    required this.id,
    required this.email,
    required this.displayName,
    this.avatarUrl,
    required this.createdAt,
  });

  final String id;
  final String email;
  final String displayName;
  final String? avatarUrl;
  final DateTime createdAt;

  @override
  List<Object?> get props => [id, email, displayName, avatarUrl, createdAt];

  // Domain logic lives here
  bool get hasAvatar => avatarUrl != null && avatarUrl!.isNotEmpty;
  String get initials => displayName.split(' ')
      .take(2)
      .map((n) => n[0].toUpperCase())
      .join();
}
```

### Use Case Pattern

```dart
// Base use case — type-safe parameters
abstract class UseCase<Type, Params> {
  Future<Either<Failure, Type>> call(Params params);
}

class NoParams extends Equatable {
  @override
  List<Object?> get props => [];
}

// Concrete use case
class LoginUseCase extends UseCase<User, LoginParams> {
  const LoginUseCase(this._repository);
  final AuthRepository _repository;

  @override
  Future<Either<Failure, User>> call(LoginParams params) async {
    if (params.email.isEmpty) {
      return const Left(ValidationFailure('Email cannot be empty'));
    }
    if (params.password.length < 8) {
      return const Left(ValidationFailure('Password must be at least 8 characters'));
    }

    return _repository.login(email: params.email, password: params.password);
  }
}

class LoginParams extends Equatable {
  const LoginParams({required this.email, required this.password});
  final String email;
  final String password;

  @override
  List<Object?> get props => [email, password];
}

// Repository interface (lives in the domain layer)
abstract class AuthRepository {
  Future<Either<Failure, User>> login({
    required String email,
    required String password,
  });
  Future<Either<Failure, void>> logout();
  Future<Either<Failure, User>> getCurrentUser();
  Stream<User?> get authStateChanges;
}
```

---

## Data Layer

### Failure Hierarchy

```dart
// Sealed class enables exhaustive error handling
sealed class Failure extends Equatable {
  const Failure(this.message);
  final String message;

  @override
  List<Object?> get props => [message];
}

class NetworkFailure     extends Failure { const NetworkFailure([super.message = 'No internet connection']); }
class TimeoutFailure     extends Failure { const TimeoutFailure([super.message = 'Connection timed out']); }
class UnauthorizedFailure extends Failure { const UnauthorizedFailure([super.message = 'Session expired']); }
class CacheFailure       extends Failure { const CacheFailure([super.message = 'Cache error']); }
class NotFoundFailure    extends Failure { const NotFoundFailure([super.message = 'Resource not found']); }
class ValidationFailure  extends Failure { const ValidationFailure(super.message); }

class ServerFailure extends Failure {
  const ServerFailure(super.message, {this.statusCode});
  final int? statusCode;

  @override
  List<Object?> get props => [message, statusCode];
}

extension DioExceptionToFailure on DioException {
  Failure toFailure() => switch (type) {
    DioExceptionType.connectionTimeout ||
    DioExceptionType.receiveTimeout    => const TimeoutFailure(),
    DioExceptionType.connectionError   => const NetworkFailure(),
    _ => switch (response?.statusCode) {
      401      => const UnauthorizedFailure(),
      404      => const NotFoundFailure(),
      >= 500   => ServerFailure(
                    response?.data?['message'] ?? 'Server error',
                    statusCode: response?.statusCode,
                  ),
      _        => ServerFailure(message),
    },
  };
}
```

### Repository Implementation

```dart
class AuthRepositoryImpl implements AuthRepository {
  const AuthRepositoryImpl({
    required AuthRemoteDataSource remoteDataSource,
    required AuthLocalDataSource localDataSource,
    required NetworkInfo networkInfo,
  })  : _remote  = remoteDataSource,
        _local   = localDataSource,
        _network = networkInfo;

  final AuthRemoteDataSource _remote;
  final AuthLocalDataSource  _local;
  final NetworkInfo          _network;

  @override
  Future<Either<Failure, User>> login({
    required String email,
    required String password,
  }) async {
    if (!await _network.isConnected) return const Left(NetworkFailure());

    try {
      final userModel = await _remote.login(email: email, password: password);
      await _local.cacheUser(userModel);
      return Right(userModel.toEntity());
    } on UnauthorizedException {
      return const Left(UnauthorizedFailure('Incorrect email or password'));
    } on ServerException catch (e) {
      return Left(ServerFailure(e.message, statusCode: e.statusCode));
    } on Exception {
      return const Left(ServerFailure('An unexpected error occurred'));
    }
  }
}
```

### Data Model (JSON Serialisable)

```dart
@JsonSerializable(fieldRename: FieldRename.snake)
class UserModel {
  const UserModel({
    required this.id,
    required this.email,
    required this.displayName,
    this.avatarUrl,
    required this.createdAt,
  });

  final String  id;
  final String  email;
  final String  displayName;
  final String? avatarUrl;
  final DateTime createdAt;

  factory UserModel.fromJson(Map<String, dynamic> json) => _$UserModelFromJson(json);
  Map<String, dynamic> toJson() => _$UserModelToJson(this);

  User toEntity() => User(
    id:          id,
    email:       email,
    displayName: displayName,
    avatarUrl:   avatarUrl,
    createdAt:   createdAt,
  );
}
```

---

## Dependency Injection (GetIt + Injectable)

```dart
final sl = GetIt.instance;

@InjectableInit(initializerName: 'init', preferRelativeImports: true, asExtension: true)
Future<void> configureDependencies() async => sl.init();

@singleton
class NetworkInfo {
  const NetworkInfo(this._connectivity);
  final Connectivity _connectivity;
  Future<bool> get isConnected async {
    final result = await _connectivity.checkConnectivity();
    return result != ConnectivityResult.none;
  }
}

@lazySingleton
class ApiClient {
  ApiClient(this._networkInfo);
  final NetworkInfo _networkInfo;
}

@LazySingleton(as: AuthRepository)
class AuthRepositoryImpl implements AuthRepository {
  const AuthRepositoryImpl(this._remote, this._local, this._network);
}

// Use cases are always factory-scoped
@injectable
class LoginUseCase {
  const LoginUseCase(this._repository);
  final AuthRepository _repository;
}

// In main.dart
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await configureDependencies();
  runApp(const App());
}
```

---

## Test Strategy

### Folder Structure

```
test/
├── core/
├── features/
│   └── auth/
│       ├── data/
│       │   ├── datasources/
│       │   └── repositories/
│       ├── domain/
│       │   └── usecases/
│       └── presentation/
│           └── bloc/
└── shared/
    └── widgets/
```

### Unit Test (Use Case)

```dart
void main() {
  late LoginUseCase loginUseCase;
  late MockAuthRepository mockRepository;

  setUp(() {
    mockRepository = MockAuthRepository();
    loginUseCase   = LoginUseCase(mockRepository);
  });

  group('LoginUseCase', () {
    const testUser = User(
      id: '123', email: 'test@test.com', displayName: 'Test User', createdAt: ...,
    );

    test('should return user with valid credentials', () async {
      when(() => mockRepository.login(email: 'test@test.com', password: 'password123'))
          .thenAnswer((_) async => const Right(testUser));

      final result = await loginUseCase(
        const LoginParams(email: 'test@test.com', password: 'password123'),
      );

      expect(result, const Right(testUser));
      verify(() => mockRepository.login(email: 'test@test.com', password: 'password123'))
          .called(1);
    });

    test('should return ValidationFailure for short password', () async {
      final result = await loginUseCase(
        const LoginParams(email: 'test@test.com', password: '123'),
      );

      expect(result.isLeft(), true);
      expect(result.fold(id, id), isA<ValidationFailure>());
      verifyNever(() => mockRepository.login(
        email: any(named: 'email'),
        password: any(named: 'password'),
      ));
    });
  });
}
```

---

## Architecture Decision Rules

**State management selection**
Simple (1–2 states, minimal business logic) → Provider/ValueNotifier. Medium (async, multiple states) → Riverpod AsyncNotifier. Complex (event-driven, heavy testing) → BLoC/Cubit.

**Repository pattern always applies.** It enables mock repositories in tests, decouples presentation from data sources, and centralises caching strategy. Never make direct API calls from the presentation layer. Use cases must not call other use cases.

**Code quality rules.** DRY: extract logic used in more than three places. YAGNI: do not add what is not needed today. File size limits: widgets and screens max 200 lines, repository implementations max 150 lines, use cases max 50 lines.

---

## Pre-Delivery Checklist

**Layer Isolation**

- [ ] Domain layer imports no Flutter or external packages
- [ ] Data layer does not import presentation
- [ ] Each use case calls a single repository method
- [ ] Entities are immutable and Equatable

**Error Handling**

- [ ] All async operations return `Either<Failure, T>`
- [ ] Try-catch blocks exist only in the data layer
- [ ] Each Failure type is specific and descriptive

**Dependency Injection**

- [ ] All dependencies resolved from the DI container
- [ ] Mock injection used in tests
- [ ] Singleton vs factory decisions are intentional

**Test Coverage**

- [ ] Use cases have unit tests
- [ ] Repositories tested with mock data sources
- [ ] Critical widgets have widget tests
- [ ] BLoC/Cubit state transitions tested
