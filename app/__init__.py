from flask import Flask, render_template, session
from datetime import datetime
import os
from app.routes.auth import auth_bp
from app.session_manager import is_user_logged_in, get_user_from_session  # Importujemy funkcje do obsługi sesji
from app.routes import profile_bp  # Importowanie blueprintów

def create_app():
    # Wskazujemy pełną ścieżkę do katalogu 'templates' i 'static' w katalogu głównym projektu
    app = Flask(__name__, 
                template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'),  # Folder z szablonami
                static_folder=os.path.join(os.path.dirname(__file__), '..', 'static'))  # Folder z plikami statycznymi (CSS, JS)

    app.secret_key = "your_secret_key"  # Konieczne do używania sesji

    # Rejestracja blueprintów
    app.register_blueprint(auth_bp)

    @app.route("/")
    def home():
        user = None  # Zakładamy, że użytkownik jest niezalogowany na początku
        if is_user_logged_in():  # Sprawdzamy, czy użytkownik jest zalogowany
            user = get_user_from_session()  # Pobieramy dane użytkownika z sesji

        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Pobieramy bieżącą datę i godzinę
        return render_template("index.html", user=user, current_date=current_date)

    return app
