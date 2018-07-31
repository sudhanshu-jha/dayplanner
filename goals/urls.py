from django.conf.urls import url

from . import views

urlpatterns = [
    
    url(r'^$', views.index, name='index'),
    url(r'^add', views.add, name='add'),
    url(r'^edit/(?P<pk>\d+)/', views.edit, name='edit'),
    url(r'^delete/(?P<pk>\d+)/', views.delete, name='delete'),
    url(r'^login', views.login_user, name='login'),
    url(r'^logout', views.logout_user, name='logout'),
    url(r'^signup',views.signup_user, name='signup'),
]
