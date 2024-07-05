from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from .views import home
from users.views import Login, Registration

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('login/', Login.as_view(), name='login'),
    path('registration', Registration.as_view(), name='registration'),
    # path('api/', include)
]
