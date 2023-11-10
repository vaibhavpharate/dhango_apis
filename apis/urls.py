from django.urls import path
from .views import sample_page, create_client, admin_login,admin_home,add_site

urlpatterns = [
    path("test",sample_page,name='sample_page'),
    path('create_client',create_client,name='create_client'),
    path("admin_home",admin_home, name="admin_home"),
    path('admin_login',admin_login,name='admin_login'),
    path('add_site',add_site,name='add_site')
]
