import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
import yfinance as yf
import os
from datetime import datetime

# 🚀 Entrenamiento desde un archivo CSV local
def entrenar_desde_csv(csv_path, output_model='modelo_csv.h5'):
    df = pd.read_csv(csv_path, sep=';')

    # Normalizar nombres de columnas
    df.columns = [col.lower().strip() for col in df.columns]
    print("🧪 Columnas disponibles:", df.columns.tolist())

    # Verificar columna 'close'
    if 'close' not in df.columns:
        raise ValueError("❌ El archivo CSV debe tener una columna llamada 'close' (minúscula).")

    # Filtrar y continuar entrenamiento
    df = df[['close']].dropna()
    return entrenar(df, output_model)

# 🌐 Entrenamiento desde datos reales en línea
def entrenar_desde_internet(output_model='modelo_online.h5'):
    df = yf.download('BTC-USD', start='2013-01-01', end=datetime.today().strftime('%Y-%m-%d'))

    # Usar solo precios de cierre
    df = df[['Close']].dropna()
    df.columns = ['close']

    return entrenar(df, output_model)

# 🧠 Función compartida de entrenamiento (usada por CSV o por internet)
def entrenar(df, output_model):
    # Escalar los datos
    scaler = MinMaxScaler()
    data = scaler.fit_transform(df)

    # Preparar secuencias para LSTM
    x_train, y_train = [], []
    for i in range(60, len(data)):
        x_train.append(data[i-60:i, 0])
        y_train.append(data[i, 0])

    x_train, y_train = np.array(x_train), np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    # Definir modelo LSTM
    model = tf.keras.Sequential([
        tf.keras.layers.LSTM(50, return_sequences=True, input_shape=(x_train.shape[1], 1)),
        tf.keras.layers.LSTM(50),
        tf.keras.layers.Dense(1)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')

    # Entrenar
    model.fit(x_train, y_train, epochs=10, batch_size=32)

    # Guardar modelo y escalador
    os.makedirs('ml_models', exist_ok=True)
    model.save(os.path.join('ml_models', output_model))
    np.save(os.path.join('ml_models', f'{output_model}_scaler_max.npy'), scaler.data_max_)

    print(f"✅ Modelo '{output_model}' entrenado y guardado.")
