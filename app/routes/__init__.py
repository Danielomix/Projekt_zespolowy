# app/routes/__init__.py

# Importowanie tras do użycia w głównym pliku aplikacji (np. app.py)
from .auth import auth_bp  # Blueprint dla autentykacji (logowanie, rejestracja)
from .profile import profile_bp  # Blueprint dla profilu użytkownika
