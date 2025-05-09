from predictor.lstm_predictor import entrenar_desde_csv, entrenar_desde_internet
import os
from pathlib import Path

# Obtener ruta base del proyecto
BASE_DIR = Path(__file__).resolve().parent

# Menú de opciones
print("🧠 ¿Cómo querés entrenar el modelo de predicción?")
print("1️⃣  Desde archivo CSV (modo local)")
print("2️⃣  Desde datos reales online (Yahoo Finance)")

opcion = input("Elegí una opción (1 o 2): ").strip()

# Ejecutar según opción elegida
if opcion == "1":
    ruta_csv = os.path.abspath(os.path.join(BASE_DIR, "..", "data", "bitcoin.csv"))
    if os.path.exists(ruta_csv):
        entrenar_desde_csv(ruta_csv)
    else:
        print(f"❌ Archivo no encontrado: {ruta_csv}")
elif opcion == "2":
    entrenar_desde_internet()
else:
    print("⚠️ Opción inválida. Por favor, ejecutá de nuevo y elegí 1 o 2.")
