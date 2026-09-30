---
trigger: always_on
---

# Project Overview & Context
- **Project Name**: Nusa Property Back-end
- **Description**: REST API yang menangani integrasi untuk android app.
- **Primary Tech Stack**: Python, FastAPI, Pydantic v2, SQLAlchemy/Prisma, Uvicorn, PostgreSQL.

## Architecture & Folder Structure
- `src/nusa_property_backend/` : Rote app.
  - `main.py` : Entry point FastAPI (`app = FastAPI(...)`).
  - `config.py` : Konfigurasi app (base URL, upload directory, database path).
  - `database.py` : PostgreSQL helper, inisialisasi tabel otomatis.
  - `models/` : Model ORM / Prisma schema mapping.
  - `routers/` : Endpoint-endpoint.
  - `services/` : Business logic.
  - `uploads/` : Direktori penyimpanan file upload (KTP, slip gaji, dokumen SP3K).

## Coding & Style Conventions
- Class (Pydantic schema, ORM model, service): `PascalCase`.
- Function, variable, module file: `snake_case`.
- Konstanta: `UPPER_SNAKE_CASE`.
- Nama file: `snake_case.py` (`user_service.py`, bukan `UserService.py`).
- Path URL: `kebab-case`.
- Gunakan **Pydantic v2** untuk semua validasi request & response.
- Gunakan `Depends()` untuk DI (DB session, current user, dsb).
- Environment variable via `pydantic-settings` (`BaseSettings`), **bukan** `os.getenv` langsung.

## Hard Guardrails (Dilarang Keras)
1. **DILARANG** mengubah file `.env`, konfigurasi database production, atau kredensial rahasia.
2. **DILARANG** menjalankan migration destruktif (seperti drop table/drop column) tanpa peringatan eksplisit.
3. **DILARANG** menambahkan dependensi baru tanpa meminta izin terlebih dahulu.
4. **DILARANG** menghapus file existing secara permanen jika tidak diinstruksikan eksplisit.
5. **DILARANG** melakukan git commit atau push otomatis ke remote repository.