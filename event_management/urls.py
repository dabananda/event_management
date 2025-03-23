from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('events/', include('events.urls')),
    path('register/', user_views.register, name='register'),
    path('login/', user_views.custom_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('activate/<int:user_id>/<str:token>/',
         user_views.activate_user, name='activate'),

]
