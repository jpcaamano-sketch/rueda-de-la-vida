import os

SUPABASE_URL  = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY  = os.environ.get("SUPABASE_KEY", "")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")

SMTP_SERVER   = "smtp.gmail.com"
SMTP_PORT     = 587
SMTP_USER     = "jpcaamano@gmail.com"
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "")

# URL base de la app pública (app_public.py)
BASE_URL      = os.environ.get("BASE_URL", "http://localhost:8532")

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "rueda2024")
