from django.contrib import admin
from django.urls import path,include 


urlpatterns = [
    path('api/auth/', include('users.urls')),
    path('admin/', admin.site.urls),
]
