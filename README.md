# Linux Security Audit Tool

Simple Linux security scanner with Flask API.

python3 pm venv venv
source /venv/bin/activate

## Install

pip install -r requirements.txt

## Run API

python app.py


## API Endpoints

- POST /api/scan
- GET /api/results

## Frontend Routes

- GET /scan
- GET /scan-results


### If port 5000 is busy, kill it by:

- sudo fuser -k 5000/tcp 