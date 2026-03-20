# OCPI 2.2.1 EMSP Simulator

**Current Version**: 1.0.0  
**Environment**: Internal Testing Tool  

## Overview
This project is a lightweight, internal **OCPI 2.2.1 EMSP Simulator** designed to validate the correctness of Savekar's CPO implementation. It allows you to simulate a roaming partner that adheres strictly to the OCPI standard.

### ⚠️ Scope & Limitations
- **Not a Production EMSP**: This tool is for testing only. It does not handle real payments, user management, or complex business logic.
- **OCPI 2.2.1 Only**: Supports strictly OCPI 2.2.1.
- **No Commands**: Does not implement the Commands module (Session Start/Stop is done via standard Session lifecycle).
- **Schema Validation**: Uses official OCPI 2.2.1 JSON schemas for validation. Note that while schemas are OCPI-aligned, they are intended for integration validation and may not cover every edge case of the full specification.

### 👥 Intended Audience
This simulator is intended for backend engineers and platform developers working on OCPI CPO implementations who need to validate protocol correctness before integrating with real EMSP roaming partners.

### ✅ What This Simulator Validates
- OCPI endpoint direction and usage
- Credentials handshake and token exchange
- Schema correctness for Locations, Sessions, and CDRs
- OCPI response envelope and status code semantics

### ❌ What This Simulator Does NOT Validate
- Commercial settlement or billing rules
- Partner-specific extensions or quirks
- Certification-level compliance
- Real-world EMSP operational behavior

### ⚠️ Error Handling
Authentication and authorization errors follow OCPI semantics (HTTP 200 with OCPI status codes), while schema validation errors can be configured to return HTTP 200 or HTTP 400 depending on testing needs.

### 📝 Logs & Debugging
The simulator writes structured, context-rich logs to stdout and optionally to a file (configured in `config.yaml`).
- **Format**: `[Direction][Module] Message {Context}`
- **Example**: `[CPO->EMSP][credentials] Invalid Token {Token=...}`
- **Test Summary**: Use `python verify_cpo.py` to run a validation flow and see a high-level PASS/FAIL summary.

## Features
- **Strict Validation**: Configurable HTTP status (default 400) when incoming data violates OCPI schemas.
- **Credentials Handshake**: Implements the CREDENTIALS module (Receiver & Sender).
- **Location Updates**: Accepts `PATCH` updates for EVSE status.
- **CDR Ingestion**: Accepts and validates Charge Detail Records.
- **CPO Client**: Includes a utility client to actively call your CPO endpoints.

## Setup & Installation

### 1. Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configuration
The application uses a `config.yaml` file for all settings. A sample file `config.example.yaml` is provided.

1. Copy the example configuration:
   ```bash
   cp config.example.yaml config.yaml
   # or manually copy/rename if on Windows without cp
   ```

2. Edit `config.yaml` to set your target CPO URL and auth tokens.

| Setting | Description |
| :--- | :--- |
| **Server Settings** | |
| `host` | Interface to bind to (default `127.0.0.1`). |
| `port` | Port to listen on (default `8000`). |
| `log_level` | Logging verbosity (e.g., `info`, `debug`). |
| **Validation** | |
| `validation_error_http_status` | Status code for schema errors. `200` for strict OCPI, `400` for clearer debugging. |
| **Authentication** | |
| `bootstrap_token` | Token expected from CPO for the initial CREDENTIALS handshake (Token A). |
| `emsp_token_to_cpo` | Token the Simulator will send to the CPO in requests (Token C). |
| `cpo_token_to_emsp` | Token the Simulator expects from the CPO after the handshake (Token B). |
| **CPO Endpoints** | |
| `cpo_url` | The base URL of your CPO implementation's OCPI API. |

## Running the Simulator

### Start the Server
```bash
python run.py
```
The server will start listening on `http://127.0.0.1:8000` (or your configured host/port).

### Access Web UI
Open your browser and navigate to:
```
http://localhost:8000
```
This simple UI allows you to view basic status or initiate flows if implemented in the UI.

## Usage Guide

### As an EMSP Simulator
Once running, the simulator listens for incoming OCPI requests. It currently supports:
- **Versions**: `/ocpi/versions`
- **Credentials**: `/ocpi/emsp/2.2.1/credentials`
- **Locations**: `/ocpi/emsp/2.2.1/locations` (PUT, PATCH, GET)
- **Sessions**: `/ocpi/emsp/2.2.1/sessions` (PUT, PATCH, GET)
- **CDRs**: `/ocpi/emsp/2.2.1/cdrs` (POST, GET)

Monitor the logs to see incoming requests and validation results.

### Testing Your CPO Implementation

To validate your CPO implementation against this simulator, follow these steps:

#### Step 1: Credentials Handshake
You (the CPO) must initiate the connection.
1. Ensure `bootstrap_token` in `config.yaml` matches what your CPO uses.
2. Send a `POST` request from your CPO to:
   `http://localhost:8000/ocpi/emsp/2.2.1/credentials`
   with the Authorization header `Token <bootstrap_token>`.
3. The simulator will validate your request, save your credentials, and return its own credentials (including `emsp_token_to_cpo`).

#### Step 2: Verification Script
We provide a script `verify_cpo.py` that acts as an active client to test *your* CPO endpoints (Simulating EMSP -> CPO calls).
```bash
python verify_cpo.py
```
This script will:
- Check if the CPO is reachable.
- Attempt to fetch locations/tariffs if implemented.
- Provide a PASS/FAIL summary.

## Project Structure
- `app/routes/`: Server-side OCPI endpoints.
- `app/client/`: Client-side logic to call CPO.
- `app/validators/json_schemas/`: Official OCPI 2.2.1 schemas.
- `tests/`: Automated verification scripts.
- `ui/`: Simple HTML/JS frontend for the simulator.

## 🤝 Test Your OCPI Integration With Us

Are you building a **production-grade CPO** and want to validate your OCPI implementation against a real EMSP before going live with a roaming partner?

We offer connectivity testing against our hosted EMSP simulator. Reach out to us and we'll help you verify your OCPI handshake, Location pushes, Session updates, and CDR submissions are spec-compliant.

- 📧 **Email**: [savekarev@gmail.com](mailto:savekarev@gmail.com)
- 💬 **GitHub**: [Open an issue or discussion](../../issues) on this repository
- 🌐 **More details**: [https://savekar.com/ocpi-simulator](https://savekar.com/ocpi-simulator)

---