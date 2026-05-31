# CyberAudit

A cross-platform security auditing dashboard built using Python, Flask, React, and JavaScript.

CyberAudit performs automated security and configuration audits on both Linux and Windows systems, providing actionable findings through a modern web dashboard.

---

# Installation

## Clone Repository

```bash
git clone https://github.com/avish-attri/CyberAudit.git
cd CyberAudit
```

---

# Quick Setup

## Linux

```bash
chmod +x setup.sh
./setup.sh
```

## Windows

```cmd
setup.bat
```

---

# Manual Setup

## Create Virtual Environment

```bash
python -m venv venv
```

## Activate Environment

### Linux

```bash
source venv/bin/activate
```

### Windows

```cmd
venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

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

# How CyberAudit Works

```text
User clicks "Run Scan"
        ↓
React dashboard sends API request
        ↓
Flask backend receives request
        ↓
Platform detection occurs
        ↓
Linux or Windows scanners execute
        ↓
Results returned as JSON
        ↓
Dashboard updates dynamically
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

## Features

* Cross-platform security auditing
* Real-time scan dashboard
* Risk-level filtering
* Security score calculation
* Authentication audits
* Filesystem audits
* Network audits
* Service audits
* Logging audits
* PDF report export
  
---

# PDF Report Export

CyberAudit allows users to export scan results as a professional PDF report.

The generated report includes:

* Scan timestamp
* Security score
* Audit summary
* Detailed findings
* Risk levels
* Recommendations
* System information

This enables users to archive scan results, share reports, and track security improvements over time.

---

# Tech Stack

## Backend

* Python
* Flask
* Flask-CORS

## Frontend

* React
* JavaScript
* HTML
* CSS

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

* React
* ReactDOM
* Babel

This keeps the frontend lightweight without requiring a full React build setup.

---

# Project Structure

```bash
CyberAudit/
│
├── api/
│   └── routes.py
│
├── frontend/
│   ├── assets/
│   │   └── cyberaudit-logo.png
│   ├── index.html
│   ├── style.css
│   └── app.jsx
│
├── scanner/
│   ├── auth_checks.py
│   ├── filesystem_checks.py
│   ├── logging_checks.py
│   ├── network_checks.py
│   ├── service_checks.py
│   ├── system_checks.py
│   ├── windows_checks.py
│   ├── linux_checks.py
│   ├── scorer.py
│   ├── utils.py
│   └── main.py
│
├── app.py
├── requirements.txt
├── setup.sh
├── setup.bat
└── README.md
```

---

# Security Checks Implemented

## Authentication Checks

### Linux

* UID 0 user detection
* SSH root login audit
* SSH password authentication audit
* Empty password account detection
* Password expiry policy verification

### Windows

* Administrator account verification
* Guest account status
* Password policy audit
* Account lockout policy audit

---

## Filesystem Checks

### Linux

* World writable files
* SUID binary detection
* /etc/passwd permission audit
* /etc/shadow permission audit

### Windows

* Sensitive directory permission verification
* Startup folder inspection
* Writable system directory detection

---

## Network Checks

### Linux & Windows

* Open ports detection
* Firewall status verification
* Remote access exposure detection
* Listening service enumeration

---

## Logging Checks

### Linux

* Authentication log verification
* Failed login detection

### Windows

* Security Event Log verification
* Failed logon event detection

---

## System Checks

### Linux

* Pending security updates
* Running services audit
* Root disk usage verification
* Kernel version audit

### Windows

* Windows Update status
* Windows Defender status
* Running services audit
* Disk usage analysis

---

# Important Notes

* Some checks require administrative privileges.
* Certain checks may be unavailable depending on:

  * Operating system
  * Installed services
  * User permissions
  * System configuration

---

# Author

Avish Attri

GitHub:
https://github.com/avish-attri
