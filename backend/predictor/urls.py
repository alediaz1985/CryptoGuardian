from django.urls import path
from .views import predecir, vista_prediccion, historial_predicciones

urlpatterns = [
    path('predecir/', predecir, name='predecir'),
    path('vista/', vista_prediccion, name='vista_prediccion'),
    path('historial/', historial_predicciones, name='historial_predicciones'),
]
