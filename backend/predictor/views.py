from django.http import JsonResponse
from django.shortcuts import render
from keras.models import load_model
import numpy as np
import pandas as pd
import yfinance as yf
import os
from .models import HistorialPrediccion
from django.utils.timezone import get_current_timezone

"""def predecir(request):
    try:
        modelo_path = 'ml_models/modelo_online.h5'
        scaler_path = 'ml_models/modelo_online.h5_scaler_max.npy'

        model = load_model(modelo_path)
        scaler_max = np.load(scaler_path)

        # Obtener datos recientes
        df = yf.download('BTC-USD', period='90d', interval='1d')
        df = df[['Close']].dropna()
        df.columns = ['close']
        data = df['close'].values.reshape(-1, 1)

        # Normalizar
        data = data / scaler_max

        # Secuencia para predecir
        ultimo_valor = data[-60:]
        ultimo_valor = np.reshape(ultimo_valor, (1, 60, 1))

        # Predicción
        prediccion_normalizada = model.predict(ultimo_valor)
        prediccion = float(prediccion_normalizada * scaler_max)

        # Precio real actual
        precio_actual = float(df['close'].iloc[-1])
        diferencia = prediccion - precio_actual
        tendencia = "📈 Subirá" if diferencia > 0 else "📉 Bajará" if diferencia < 0 else "➡️ Se mantendrá"

        HistorialPrediccion.objects.create(
            precio_actual=precio_actual,
            prediccion=prediccion,
            diferencia=diferencia,
            tendencia=tendencia,
            modelo_usado="modelo_online"
        )

        return JsonResponse({
            "prediccion": round(prediccion, 2),
            "precio_actual": round(precio_actual, 2),
            "diferencia": round(diferencia, 2),
            "tendencia": tendencia
        })

    except Exception as e:
        return JsonResponse({"error": f"❌ Error al predecir: {str(e)}"})"""

def predecir(request):
    try:
        modelo = request.GET.get("modelo", "modelo_online")
        modelo_path = f'ml_models/{modelo}.h5'
        scaler_path = f'ml_models/{modelo}.h5_scaler_max.npy'

        # Cargar modelo entrenado y escalador
        model = load_model(modelo_path)
        scaler_max = np.load(scaler_path)

        # Obtener datos de entrada (CSV local o datos en línea)
        if modelo == "modelo_csv":
            df = pd.read_csv("C:/proyectos/CryptoGuardian/data/bitcoin.csv", sep=";")
            df.columns = [col.lower().strip() for col in df.columns]
            df = df[['close']].dropna()
        else:
            df = yf.download('BTC-USD', period='90d', interval='1d')[['Close']].dropna()
            df.columns = ['close']

        data = df['close'].values.reshape(-1, 1)
        data = data / scaler_max

        # Preparar secuencia de entrada
        secuencia = data[-60:]
        secuencia = np.reshape(secuencia, (1, 60, 1))

        # Realizar predicción
        prediccion_normalizada = model.predict(secuencia)
        prediccion = float(prediccion_normalizada * scaler_max)
        precio_actual = float(df['close'].iloc[-1])
        diferencia = prediccion - precio_actual
        tendencia = "📈 Subirá" if diferencia > 0 else "📉 Bajará" if diferencia < 0 else "➡️ Se mantendrá"

        # Guardar en historial
        HistorialPrediccion.objects.create(
            precio_actual=precio_actual,
            prediccion=prediccion,
            diferencia=diferencia,
            tendencia=tendencia,
            modelo_usado=modelo
        )

        # Obtener últimos 5 del historial (orden cronológico)
        ultimos = HistorialPrediccion.objects.order_by("-fecha")[:5][::-1]
        tz = get_current_timezone()
        labels = [p.fecha.astimezone(tz).strftime("%Y-%m-%d %H:%M") for p in ultimos]
        precios_reales = [round(p.precio_actual, 2) for p in ultimos]
        precios_predichos = [round(p.prediccion, 2) for p in ultimos]

        return JsonResponse({
            "prediccion": round(prediccion, 2),
            "precio_actual": round(precio_actual, 2),
            "diferencia": round(diferencia, 2),
            "tendencia": tendencia,
            "labels": labels,
            "precio_real": precios_reales,
            "precio_predicho": precios_predichos
        })

    except Exception as e:
        return JsonResponse({"error": f"❌ Error al predecir: {str(e)}"})


# Vista para el frontend interactivo
def vista_prediccion(request):
    return render(request, "predictor/predecir.html")



"""
anterior funcionando solo para listar el historial de predicciones
def historial_predicciones(request):
    predicciones = HistorialPrediccion.objects.order_by('-fecha')[:50]  # las últimas 50
    return render(request, "predictor/historial.html", {"predicciones": predicciones})
"""
from django.utils.timezone import make_aware, get_current_timezone
from datetime import datetime, time

def historial_predicciones(request):
    fecha_inicio = request.GET.get("inicio")
    fecha_fin = request.GET.get("fin")

    print("📅 Fecha inicio (raw):", fecha_inicio)
    print("📅 Fecha fin (raw):", fecha_fin)

    predicciones = HistorialPrediccion.objects.all()
    tz = get_current_timezone()

    if fecha_inicio and fecha_fin:
        try:
            inicio_dt = make_aware(datetime.combine(datetime.strptime(fecha_inicio, "%Y-%m-%d"), time.min), tz)
            fin_dt = make_aware(datetime.combine(datetime.strptime(fecha_fin, "%Y-%m-%d"), time.max), tz)

            print("🕒 Rango filtrado:", inicio_dt, "→", fin_dt)

            predicciones = predicciones.filter(
                fecha__range=(inicio_dt, fin_dt)
            ).order_by("-fecha")

            print(f"🔎 Coincidencias encontradas: {predicciones.count()}")

        except Exception as e:
            print("⚠️ Error al parsear fechas:", e)
            predicciones = HistorialPrediccion.objects.order_by("-fecha")[:3]
    else:
        predicciones = HistorialPrediccion.objects.order_by("-fecha")[:3]
        print("ℹ️ No se ingresaron fechas. Mostrando últimas 3.")

    return render(request, "predictor/historial.html", {
        "predicciones": predicciones,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
    })

