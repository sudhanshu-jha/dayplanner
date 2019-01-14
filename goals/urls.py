from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r"^$", views.index, name="index"),
    url(r"^add", views.add, name="add"),
    url(r"^edit/(?P<pk>\d+)/", views.edit, name="edit"),
    url(r"^delete/(?P<pk>\d+)/", views.delete, name="delete"),
    url(r"^login", views.login_user, name="login"),
    url(r"^logout", views.logout_user, name="logout"),
    url(r"^signup", views.signup, name="signup"),
    url(
        r"^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        views.activate,
        name="activate",
    ),
    url(r"^password_reset/$", auth_views.password_reset, name="password_reset"),
    url(
        r"^password_reset/done/$",
        auth_views.password_reset_done,
        name="password_reset_done",
    ),
    url(
        r"^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        auth_views.password_reset_confirm,
        name="password_reset_confirm",
    ),
    url(
        r"^reset/done/$",
        auth_views.password_reset_complete,
        name="password_reset_complete",
    ),
]
