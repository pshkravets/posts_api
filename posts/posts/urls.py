from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from .views import home
from users.views import Login, Registration, log_out

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('login/', Login.as_view(), name='login'),
    path('registration/', Registration.as_view(), name='registration'),
    path('logout/', log_out, name='logout'),
    path('api/', include('api.urls'))
]
