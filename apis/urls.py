from django.urls import path
from .views import sample_page, create_client, admin_login,admin_home,add_site, premium,client_homepage,client_login, custom_403_view

urlpatterns = [
    path("test",sample_page,name='sample_page'),
    path('create_client',create_client,name='create_client'),
    path("admin_home",admin_home, name="admin_home"),
    path('admin_login',admin_login,name='admin_login'),
    path('add_site',add_site,name='add_site'),
    path('premium',premium,name='premium'),
    path('client_login',client_login,name='client_login'),
    path('client_homepage',client_homepage,name='client_homepage'),
    path('403',custom_403_view,name='403')

]
