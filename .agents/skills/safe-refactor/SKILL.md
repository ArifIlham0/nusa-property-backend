---
name: safe-refactor
description: Triggers whenever the user asks to refactor, modularize, extract, or clean up code across any tech stack, including FastAPI / Python (e.g., separating APIRouter endpoints, service layer, repository pattern, dependency injection with Depends, Pydantic schemas/models, database session handling), Kotlin & Jetpack Compose (e.g., extracting @Composable functions, state hoisting, separating ViewModels/state holders, splitting large Compose/Kotlin .kt files), Flutter, Next.js/React, React Native, Django/Python, etc. (e.g., "refactor file ini", "pecah file ini", "pisahkan router/endpoint/service", "pisahkan widget/komponen/composable", "ekstrak composable/function/service/hook", "jadikan lebih modular", "clean up code"). Guides safe code restructuring and file splitting while strictly preserving 100% existing functionality with zero behavioral regressions.
---

# Procedural Steps for Safe Code Refactoring & Modularization

When this skill is triggered, perform the following steps sequentially to cleanly break down bloated files into modular, maintainable units without altering any application behavior:

1. **Pre-Refactor Audit & Dependency Mapping**:
   - Trace all variables, reactive states, hooks, ORM queries, methods, closures, and side effects within the target block.
   - Map exact interface boundaries:
     - **Inputs**: Props, constructor parameters, function arguments, context, FastAPI `Depends()` dependencies, path/query parameters, or request bodies.
     - **Outputs**: Callbacks, event emitters, return types, response models/schemas, mutations, or emitted state changes.
   - Understand the current behavior completely before moving or deleting any code.

2. **Atomic Extraction & Contract Preservation**:
   - Extract code cleanly with explicit type definitions (Kotlin types/data classes, Dart types, TypeScript interfaces/types, Python type hints & Pydantic schemas). Avoid fallback to `any` or `dynamic`.
   - Ensure imports and exports are properly linked; avoid circular imports (especially important in Python/FastAPI module splits).
   - Preserve existing naming conventions, docstrings, and comments unless explicitly instructed to update them.

3. **Zero-Regression Guardrails (Strict)**:
   - **Do NOT mutate business logic**: Keep conditional checks, calculation algorithms, error handling, status codes, and payload schemas identical.
   - **Do NOT introduce unapproved packages**: Do not add new external dependencies to `build.gradle.kts` / `build.gradle`, `pubspec.yaml`, `package.json`, or `requirements.txt` / `pyproject.toml` / `Pipfile` without explicit user permission.

4. **Integrity & Verification**:
   - Verify that all imports (both in the source file and the new module) resolve cleanly.
   - Clean up unused imports left behind in the caller file.
   - Check syntax and static types (e.g., `mypy`, `ruff`, `flake8`, `pytest`, `python manage.py check`, `./gradlew compileKotlin` / Android lint, `flutter analyze`, `tsc --noEmit`, or linter diagnostics where applicable).
   - Provide a concise summary of changes: what was extracted, destination paths, and confirmation that behavior remains identical.