---
name: bug-triage-investigate
description: Analyzes crash logs, stack traces, compile failures, runtime exceptions, and framework diagnostics for FastAPI & Python backend (including Uvicorn/Gunicorn startup/lifespan errors, Pydantic ValidationError/schema mismatches, SQLAlchemy/ORM database errors, async/await coroutine issues, HTTPException, route/dependency injection errors), Kotlin & Jetpack Compose (including Android Logcat, Compose recomposition/layout errors, state/Modifier issues, and errors in Kotlin .kt files), Flutter (including RenderFlex overflow, RenderBox constraints, infinite height/width errors, Flutter widget build/layout errors, assertion failures, red/blue debug console output), Gradle/Xcode build issues, React/Next.js, and React Native whenever the user pastes any error log, console output, stack trace, or asks to investigate/fix errors in FastAPI, Python, or frontend/mobile code.
---

# Procedural Steps for Bug Investigation

1. **Log Parsing**:
   - Ekstrak baris file dan nomor baris spesifik tempat exception terjadi dari stack trace (termasuk Python/Uvicorn traceback, Logcat, atau console browser).
2. **Root Cause Analysis**:
   - Periksa apakah error disebabkan oleh: null/None/undefined value, Pydantic validation failure, masalah async/await/unawaited coroutine, masalah permission/CORS, database/ORM session leak, tipe data tidak cocok, atau dependensi network/service.
3. **Impact Scope**:
   - Tentukan apakah bug memengaruhi fungsionalitas atau endpoint lain di sekitarnya.
4. **Actionable Fix**:
   - Tampilkan potongan kode sebelum dan sesudah perbaikan tanpa mengubah arsitektur modul yang tidak terkait.