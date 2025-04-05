from flask import session
from app.firebase_config import firestore_db

# Sprawdzanie, czy użytkownik jest zalogowany
def is_user_logged_in():
    return 'user_id' in session

# Pobieranie danych użytkownika z Firestore na podstawie user_id zapisanej w sesji
def get_user_from_session():
    if is_user_logged_in():
        user_id = session['user_id']
        user_doc = firestore_db.collection("users").document(user_id).get()
        if user_doc.exists:
            return user_doc.to_dict()
    return None
