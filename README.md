# Coruscant Health Administration System

Django-based health administration platform covering five stakeholders:
**Patient, Doctor, Department, Administrator, Emergency Services.**

## Features implemented
- Custom user model with roles + Administrator approval workflow (`accounts`)
- Device data upload API + Patient dashboard (`patients`)
- Doctor dashboard: patient trend chart, report writing, service orders (`doctors`)
- Department order queue: execute orders, record results (`departments`)
- Emergency quick-intake form, minimal fields (`emergency`)
- Encrypted document storage (Fernet/AES) for scans, lab reports, prescriptions (`documents`)
- Bootstrap-based responsive UI (`templates/`)
- Unit tests for every app (`python manage.py test`)
- GitHub Actions CI (`.github/workflows/ci.yml`)

## Local setup
```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in secrets
export $(cat .env | xargs)
python manage.py migrate
python manage.py createsuperuser   # create the first Administrator
python manage.py runserver
```

Generate a document-encryption key once:
```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

## Running tests
```bash
python manage.py test
```

## Roles & flow
1. Patient/Doctor register at `/accounts/register/` → status pending.
2. Administrator logs into `/accounts/approve/` and approves them.
3. Patient's device calls `POST /api/patients/readings/` to upload readings.
4. Doctor views `/doctors/dashboard/`, opens a patient, sees the trend chart,
   writes a report, or raises an order (CT/PET/etc).
5. Department staff view `/departments/orders/`, execute an order, record a
   result summary, then upload the full result as an encrypted document.
6. Emergency Services use `/emergency/intake/` for fast, minimal-field
   patient registration during an emergency (auto-approved).

## Deployment
This project deploys to any platform that runs Django via `gunicorn`
(Render, Railway, Azure App Service, AWS Elastic Beanstalk, Heroku-style
buildpacks). Required environment variables are listed in `.env.example`.
Once deployed, put the live URL in `my_coruscant_health_administration_url.txt`
at the project root (URL only, nothing else).

## Security notes
- Documents are encrypted with Fernet (AES-128-CBC + HMAC) before storage;
  the key lives only in `DOCUMENT_ENCRYPTION_KEY`, never in source control.
- `DEBUG=False` in production enables HSTS, secure cookies, and SSL redirect.
- Switch `DATABASES` to Postgres via `DATABASE_URL` for production.
