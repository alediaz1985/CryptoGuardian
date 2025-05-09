from django.db import models

class HistorialPrediccion(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    precio_actual = models.FloatField()
    prediccion = models.FloatField()
    diferencia = models.FloatField()
    tendencia = models.CharField(max_length=50)
    modelo_usado = models.CharField(max_length=50, default="modelo_online")

    def __str__(self):
        return f"{self.fecha} - {self.tendencia} - ${self.prediccion:.2f}"
