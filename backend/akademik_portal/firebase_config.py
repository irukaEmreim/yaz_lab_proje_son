import firebase_admin
from firebase_admin import credentials, storage
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Firebase servis hesabı dosyasının yolu
cred = credentials.Certificate(os.path.join(BASE_DIR,"akademik_portal","firebase_service_account.json"))

# Projeyi başlat
firebase_admin.initialize_app(cred, {
    'storageBucket': 'akademik-portal.firebasestorage.app'  # Bunu kendi bucket adınla değiştir
})

bucket = storage.bucket()
