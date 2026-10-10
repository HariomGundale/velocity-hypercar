# Velocity Hypercar Configurator — Audit & Debugging Report

## Overview
This document contains a comprehensive audit of all discovered issues, security considerations, state management bugs, 3D memory leaks, backend edge cases, and feature enhancements added to the **Velocity Hypercar Configurator** codebase.

---

## 1. Frontend Audit & Debugging Fixes

### 1.1 `getSharedBuild` Auth Header Leak & 401 Block on Public Builds
- **File**: [`frontend/src/services/configurationService.js`](file:///P:/p-66/velocity-hypercar/frontend/src/services/configurationService.js)
- **Issue**: `getSharedBuild(buildId)` called `request()` without setting `{ auth: false }`. When a user with an expired or stale token opened a public shared build link (`#/build/VX-XXXXX`), the browser sent `Authorization: Bearer <expired-token>`. The backend returned HTTP 401 Unauthorized, blocking public access.
- **Fix**: Updated `getSharedBuild` to explicitly pass `{ auth: false }`.

### 1.2 Option Incompatibility / State Corruption on Vehicle Switch
- **File**: [`frontend/src/catalog.js`](file:///P:/p-66/velocity-hypercar/frontend/src/catalog.js)
- **Issue**: `switchCar(prev, carId, o)` retained option IDs from the previous vehicle. Since options are vehicle-specific, switching to a car with different option IDs caused `byId()` to return `null`, breaking UI color swatches, pills, and 3D material mapping.
- **Fix**: Added option validation on vehicle switch — if the previously selected option ID is not valid for the new vehicle, it automatically falls back to that vehicle's default option.

### 1.3 `wheelStyle` Negative Index Fallback Bug
- **File**: [`frontend/src/catalog.js`](file:///P:/p-66/velocity-hypercar/frontend/src/catalog.js)
- **Issue**: When a wheel name didn't match style keywords, `(list||[]).findIndex(...)` returned `-1`. `Math.max(0, -1)` returned `0`, causing `0 % STYLES.length` to always pick `STYLES[0]` (`'aero'`) regardless of wheel position.
- **Fix**: Updated index calculation to verify `idx >= 0` before computing modulo.

### 1.4 WebGL / Three.js Context & Memory Leaks
- **File**: [`frontend/src/carStage.js`](file:///P:/p-66/velocity-hypercar/frontend/src/carStage.js)
- **Issue**: `PMREMGenerator` environment textures and shadow plane geometries/materials were not disposed when unmounting `<Car3D />`. Repeated navigation between views triggered WebGL context creation limits (`TOO_MANY_CONTEXTS`). Additionally, `SNAPS` snapshot map cached base64 image strings indefinitely.
- **Fix**: Added proper disposal for `PMREMGenerator`, `envTexture`, shadow geometries/textures, and capped the `SNAPS` cache size to 50 items with LRU eviction.

### 1.5 Carousel Visual State Leak
- **File**: [`frontend/src/App.jsx`](file:///P:/p-66/velocity-hypercar/frontend/src/App.jsx)
- **Issue**: In the Models carousel, `<CarVisual>` slots for non-active vehicles were passed the active vehicle's `look` object, displaying incorrect paints/wheels on other models.
- **Fix**: Updated carousel rendering so each vehicle slot uses its own default `makeLook` configuration.

---

## 2. Backend Audit & Security Improvements

### 2.1 Case-Insensitive Build ID Validation
- **File**: [`app/utils/build_id.py`](file:///P:/p-66/velocity-hypercar/app/utils/build_id.py)
- **Issue**: `BUILD_ID_PATTERN` regex was strictly uppercase. `is_valid_build_id` failed if passed un-normalized lowercase inputs like `vx-8f29a`.
- **Fix**: Added `re.IGNORECASE` flag to `BUILD_ID_PATTERN` and normalized string handling in `is_valid_build_id()`.

### 2.2 SQLite Foreign Key Enforcement
- **File**: [`app/db/database.py`](file:///P:/p-66/velocity-hypercar/app/db/database.py)
- **Issue**: SQLite disables foreign key constraints by default unless explicitly enabled per connection.
- **Fix**: Added SQLAlchemy event listener `@event.listens_for(engine, "connect")` executing `PRAGMA foreign_keys=ON` for SQLite database connections.

### 2.3 Null-Safe Section Response Building
- **File**: [`app/services/configuration_service.py`](file:///P:/p-66/velocity-hypercar/app/services/configuration_service.py)
- **Issue**: `_sections()` directly accessed properties on related models (`c.paint.id`, `c.wheel.id`). If any referenced option was deleted, querying the build raised an unhandled `AttributeError`, resulting in HTTP 500 Internal Server Error.
- **Fix**: Implemented `_ref()` and `_color_ref()` null-safety helper functions to provide fallback values (`"Unknown"` / `"#000000"`) if a related entity is missing.

### 2.4 Login Password Length Boundary Check
- **File**: [`app/schemas/auth.py`](file:///P:/p-66/velocity-hypercar/app/schemas/auth.py)
- **Issue**: `LoginRequest` lacked `max_length=72` validation on passwords. Unbounded password strings could be used to perform CPU DoS attacks against bcrypt verification.
- **Fix**: Added `max_length=72` validation to `LoginRequest.password`.

---

## 3. New Features & Vehicle Expansion

### 3.1 Seat Customization Visual Component (`<SeatVisual />`)
- **Files**: [`frontend/src/SeatVisual.jsx`](file:///P:/p-66/velocity-hypercar/frontend/src/SeatVisual.jsx), [`frontend/src/App.jsx`](file:///P:/p-66/velocity-hypercar/frontend/src/App.jsx), [`frontend/src/styles.css`](file:///P:/p-66/velocity-hypercar/frontend/src/styles.css)
- **Features**:
  - Displays a high-detail interactive seat visual element right alongside the hypercar in the configurator showcase stage across **all vehicle models**.
  - Dynamically updates seat geometry, carbon weave backing, harness slots, quilting patterns, and cushion colors when customizing **Seat Type** (`Sport`, `Racing`, `Luxury`), **Interior Material** (`Leather`, `Alcantara`, `Carbon`), and **Interior Color** (`Black`, `White`, `Red`, `Tan`).
  - Clicking the seat showcase opens/focuses the Interior customization tab.

### 3.2 New Hypercar Model: Ferrari 296 GTB
- **Files**: [`app/db/seed.py`](file:///P:/p-66/velocity-hypercar/app/db/seed.py), [`frontend/src/vehicleVisuals.js`](file:///P:/p-66/velocity-hypercar/frontend/src/vehicleVisuals.js), [`frontend/src/VehicleArt.jsx`](file:///P:/p-66/velocity-hypercar/frontend/src/VehicleArt.jsx), [`tests/test_cars.py`](file:///P:/p-66/velocity-hypercar/tests/test_cars.py)
- **Features**:
  - Added **Ferrari 296 GTB** (`ferrari-296-gtb`) to the backend database with 830 hp V6 hybrid powertrain, Assetto Fiorano track calibration packages, active tea-tray spoiler aero, and custom 2D vector artwork (`FerrariArt`).

---

## 4. Verification & Test Results
- **Pytest Test Suite**: Executed test suite — **77 / 77 tests passed**.
- **Frontend Production Build**: Executed `npm run build` — completed successfully with 0 errors.
- **Runtime Verification**: Both backend API ([http://127.0.0.1:8000](http://127.0.0.1:8000)) and frontend dev server ([http://localhost:5173](http://localhost:5173)) verified active and healthy.
