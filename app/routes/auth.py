from flask import Blueprint, render_template, request, redirect, jsonify, session, url_for
from firebase_admin import auth, firestore, db
from app.firebase_config import firestore_db, realtime_db
from datetime import datetime

auth_bp = Blueprint("auth", __name__)

# Rejestracja i logowanie użytkownika
@auth_bp.route("/auth", methods=["GET", "POST"])
def auth_user():
    action = request.args.get("action", "login")  # Domyślnie login
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        try:
            if action == "register":
                # Tworzenie użytkownika w Firebase Auth
                user = auth.create_user(email=email, password=password)
                # Zapisanie użytkownika w Firestore
                firestore_db.collection("users").document(user.uid).set({
                    "email": email,
                    "uid": user.uid,
                    "role": "user",  # Domyślnie przypisujemy rolę "user"
                    "created_at": firestore.SERVER_TIMESTAMP
                })
                # Zapisanie użytkownika w Firebase Realtime Database
                realtime_db.child("users").child(user.uid).set({
                    "email": email,
                    "role": "user"
                })
                # Po rejestracji logujemy użytkownika automatycznie
                session['user_id'] = user.uid  # Przechowywanie UID w sesji
                print(f"Logged in user_id: {session.get('user_id')}")
                return redirect(url_for('auth.home'))  # Po rejestracji przekierowujemy na stronę główną
            elif action == "login":
                # Logowanie użytkownika
                user = auth.get_user_by_email(email)
                session['user_id'] = user.uid  # Przechowywanie UID w sesji
                return redirect(url_for('auth.home'))  # Przekierowanie na stronę główną po zalogowaniu
        except Exception as e:
            return jsonify({"success": False, "message": str(e)})
    return render_template("auth.html", action=action)

# Wylogowanie użytkownika
@auth_bp.route("/auth/logout")
def logout():
    session.pop('user_id', None)  # Usuwamy dane użytkownika z sesji
    return redirect(url_for('auth.home'))  # Przekierowanie na stronę główną po wylogowaniu

# Strona główna (index)
@auth_bp.route("/")
def home():
    if 'user_id' not in session:
        # Jeśli użytkownik nie jest zalogowany, przekierowujemy do logowania
        return render_template('index.html', user=None, current_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # Pobieramy dane użytkownika z Firestore
    user_id = session['user_id']
    user_ref = firestore_db.collection('users').document(user_id)
    user = user_ref.get()

    if user.exists:
        user_data = user.to_dict()
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Pobieramy aktualną datę i godzinę
        return render_template('index.html', user=user_data, current_date=current_date)
    else:
        return jsonify({"success": False, "message": "User not found"}), 404
