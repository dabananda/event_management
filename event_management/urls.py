from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from events import views as event_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('events/', include('events.urls')),
    path('register/', user_views.register, name='register'),
    path('login/', user_views.custom_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('activate/<int:user_id>/<str:token>/',
         user_views.activate_user, name='activate'),

    # admin dashboard
    path('admin_dashboard/', user_views.admin_dashboard, name='admin_dashboard'),
    path('admin_dashboard/assign_role/<int:id>/',
         user_views.assign_role, name='assign_role'),
    path('admin_dashboard/create_group/',
         user_views.create_group, name='create_group'),
    path('admin_dashboard/group_list/',
         user_views.group_list, name='group_list'),
    path('no_permission', user_views.no_permission, name='no_permission'),

    # Dashboard redirecting url
    path('dashboard/', event_views.dashboard, name="dashboard")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
