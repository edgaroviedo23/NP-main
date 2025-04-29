from django.contrib import admin
from django.urls import path, include
from nueva_app.views import home
from django.conf.urls.static import static
from django.conf import settings
from django.templatetags.static import static as static_url
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('nueva_app.urls')), 
    path('favicon.ico', RedirectView.as_view(url=static_url('img/favicon.ico'), permanent=True)),
     # Aquí se incluyen las rutas de nueva_app
]