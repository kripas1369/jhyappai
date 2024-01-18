from pickle import TRUE
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from ecomapp.views import home, login_user, logout_user, notfound_404, register_user

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('about-us/', aboutus, name="About"),
    path("", include('ecomapp.urls', namespace="ecomapp")),
    path('login/', login_user, name="login"),
    path('register/', register_user, name="register"),
    path('logout/', logout_user, name="logout"),
    path('not-found/', notfound_404, name="error404"),
    path('accounts/', include("allauth.urls"))
]
