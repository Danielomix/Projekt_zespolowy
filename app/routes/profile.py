from flask import Blueprint, render_template, request, session, redirect, flash
import firebase_admin
from firebase_admin import auth, firestore, db

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')

# Połączenie z Firestore i Realtime Database
firestore_db = firestore.client()
realtime_db = db.reference("/")

@profile_bp.route("/", methods=["GET", "POST"])
def profile():
    if 'user_id' not in session:
        return redirect("/auth?action=login")  # Przekierowanie do logowania, jeśli użytkownik nie jest zalogowany

    try:
        user = auth.get_user(session['user_id'])  # Pobranie użytkownika na podstawie ID z sesji
        user_data = firestore_db.collection("users").document(user.uid).get().to_dict()  # Pobranie danych z Firestore
        
        if request.method == "POST":
            new_email = request.form["email"]
            new_role = request.form.get("role", "user")
            
            # Aktualizacja w Firebase Authentication
            auth.update_user(user.uid, email=new_email)
            
            # Aktualizacja w Firestore
            firestore_db.collection("users").document(user.uid).update({
                "email": new_email,
                "role": new_role
            })
            
            # Aktualizacja w Realtime Database
            realtime_db.child("users").child(user.uid).update({
                "email": new_email,
                "role": new_role
            })
            return redirect("/profile")  # Po zapisaniu zmian wróć na stronę profilu

        return render_template("profile.html", user=user_data)
    except Exception as e:
        return f"Error: {str(e)}"

@profile_bp.route("/edit", methods=["POST"])
def edit_profile():
    if 'user_id' not in session:
        return redirect("/auth?action=login")  # Przekierowanie do logowania, jeśli użytkownik nie jest zalogowany

    try:
        user = auth.get_user(session['user_id'])  # Pobranie użytkownika na podstawie ID z sesji
        user_data = firestore_db.collection("users").document(user.uid).get().to_dict()  # Pobranie danych z Firestore

        # Pobierz dane z formularza
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        phone_number = request.form.get("phone_number")
        email_notifications = request.form.get("email_notifications") == "on"

        # Aktualizacja danych w Firestore
        firestore_db.collection("users").document(user.uid).update({
            "first_name": first_name,
            "last_name": last_name,
            "phone_number": phone_number,
            "email_notifications": email_notifications
        })

        # Aktualizacja w Realtime Database
        realtime_db.child("users").child(user.uid).update({
            "first_name": first_name,
            "last_name": last_name,
            "phone_number": phone_number,
            "email_notifications": email_notifications
        })

        flash("Profil został zaktualizowany!", "success")
        return redirect("/profile")
    except Exception as e:
        return f"Error: {str(e)}"