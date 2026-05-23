# Linux Security Audit Tool

Simple Linux security scanner with Flask API.

## Setup

python3 -m venv venv
source venv/bin/activate

## Install

pip install -r requirements.txt

## Run

python app.py

Then open:

- http://127.0.0.1:5000/scan

## API Endpoints

- POST /api/scan
- GET /api/results

## Frontend Routes

- GET /scan
- GET /scan-results

### If port 5000 is busy, kill it by:

- sudo fuser -k 5000/tcp 