from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('predictor/', include('predictor.urls')),  # 👈 esto está bien
]
