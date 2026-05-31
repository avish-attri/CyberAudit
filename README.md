# CyberAuditTool

A modular security auditing dashboard built using Python, Flask, React, and JavaScript.

The tool performs automated Linux security checks and displays findings through a modern web dashboard.

---

## Features

- security auditing
- Real-time scan dashboard
- Modular scanner architecture
- Risk-level filtering
- Security score calculation
- Authentication checks
- Filesystem checks
- Network checks
- Logging checks
- Service checks
- Human-readable recommendations
- Scan metadata display
- Local web dashboard

---

# Tech Stack

## Backend
- Python
- Flask
- Flask-CORS

## Frontend
- React
- JavaScript
- HTML
- CSS

## Security & System
- Linux system commands
- Filesystem analysis
- SSH configuration auditing
- Service inspection

---

# React Frontend

The frontend dashboard is built using React and rendered through:

```text
frontend/app.jsx
```

React is loaded through CDN inside:

```text
frontend/index.html
```

using:
- React
- ReactDOM
- Babel

This keeps the frontend lightweight without requiring a full React build setup.

---

# Project Structure

```bash
linux-security-audit-tool/
│
├── api/
│   └── routes.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   ├── script.js
│   └── app.jsx
│
├── scanner/
│   ├── auth_checks.py
│   ├── file_checks.py
│   ├── logging_checks.py
│   ├── network_checks.py
│   ├── service_checks.py
│   ├── system_checks.py
│   ├── scorer.py
│   ├── utils.py
│   └── main.py
│
├── app.py
├── requirements.txt
├── setup.sh
└── README.md
```

---

# Security Checks Implemented

## Authentication Checks
- UID 0 user detection
- SSH root login check
- SSH password authentication check
- Guest account detection
- Empty password account detection
- Password expiry policy audit

## Filesystem Checks
- World writable files
- SUID binary detection
- /etc/passwd permission checks
- /etc/shadow permission checks

## Network Checks
- Open ports detection
- Firewall status
- SSH service exposure

## Logging Checks
- Authentication log verification
- Failed login detection

## System Checks
- Pending security updates
- Running services count
- Root disk usage
- Kernel version audit

---

# Installation

## Clone Repository

```bash
git clone https://github.com/avish-attri/sec-audit-linux.git
cd sec-audit-linux
```

---

# Quick Setup

Run:

```bash
chmod +x setup.sh
./setup.sh
```

This script:
- creates virtual environment
- installs dependencies
- starts the Flask server

---

# Manual Setup

## Create Virtual Environment

```bash
python3 -m venv venv
```

## Activate Virtual Environment

```bash
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Application

```bash
python app.py
```

---

# Open Dashboard

Visit:

```text
http://127.0.0.1:5000/scan
```

---

# How React Frontend Works

## Frontend Flow

```text
User clicks "Run Scan"
        ↓
React frontend sends API request
        ↓
Flask backend receives request
        ↓
Python scanner executes Linux checks
        ↓
Results returned as JSON
        ↓
React dashboard updates dynamically
```

---

# API Endpoints

## Run Security Scan

```http
POST /api/scan
```

## Fetch Latest Results

```http
GET /api/scan-results
```

---

# Dashboard Features

- Security score visualization
- Risk-level filtering
- Pass / Warning / Fail / Unavailable statistics
- Detailed recommendations
- Scan metadata
- Responsive dark-mode UI

---

# Sample Workflow

1. Launch application
2. Open dashboard in browser
3. Click "Run Scan"
4. Scanner performs security audit
5. Results displayed in dashboard

---

# Important Notes

- Some checks require elevated permissions
- Recommended to run on Linux systems
- Certain checks may be unavailable depending on:
  - Linux distribution
  - installed services
  - user permissions

---


<!-- # Screenshots

## Dashboard

Add screenshots here.

--- -->

# Author

Avish Attri

GitHub:
https://github.com/avish-attri

---