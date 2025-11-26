# tmp_reptest_db.py
from database.firebase_config import init_firebase
from firebase_admin import db
import traceback

init_firebase()
try:
    root = db.reference('/')
    print("Intentando lectura de la raíz (podría tardar):")
    print(root.get())  # imprime None o estructura si la conexión funciona
except Exception:
    traceback.print_exc()