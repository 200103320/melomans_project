from django.contrib import admin
from django.urls import path, include
from main import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.staticfiles.urls import static
from django.conf import settings
from main.views import (
    registration_view,
    logout_view,
    login_view,
    account_view
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('register/', registration_view, name="register"),
    path('logout/', logout_view, name="logout"),
    path('login/', login_view, name="login"),
    path('account/', account_view, name="account"),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('accounts/', include('allauth.urls')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
