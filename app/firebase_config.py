import firebase_admin
from firebase_admin import credentials, auth, firestore, db
import os

# Wczytanie konfiguracji Firebase
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
cred_path = os.path.join(BASE_DIR, "../firebase_credentials.json")  # Cofamy się o katalog

# Inicjalizacja Firebase (sprawdzamy, czy już nie jest zainicjalizowane)
if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://aplikacja-biznesowa-default-rtdb.europe-west1.firebasedatabase.app/'
    })

# Połączenie do baz danych
firestore_db = firestore.client()
realtime_db = db.reference("/")
