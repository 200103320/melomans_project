from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import path, include
from main.views import index, premium, download, help, player, SearchResultsView, songadd

urlpatterns = [
    path("", index, name='/index'),
    url(r'^index/', index, name='/index'),
    url(r'^premium/', premium, name='premium'),
    url(r'^download/', download, name='download'),
    url(r'^help/', help, name='help'),
    url(r'^player/', player, name='player'),
    url(r'^songadd/', songadd, name='songadd'),
    url(r'^search/', SearchResultsView.as_view(), name='search'),
    path('accounts/', include('django.contrib.auth.urls')),

    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),
         name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'),
         name='password_change'),

    path('password_reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),
]
