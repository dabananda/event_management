from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from events import views as event_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', event_views.IndexView.as_view(), name='index'),
    path('events/', include('events.urls')),
    path('register/', user_views.register, name='register'),
    path('login/', user_views.custom_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('activate/<int:user_id>/<str:token>/',
         user_views.activate_user, name='activate'),
    path('admin_dashboard/', user_views.admin_dashboard, name='admin_dashboard'),
    path('admin_dashboard/assign_role/<int:id>/',
         user_views.assign_role, name='assign_role'),
    path('admin_dashboard/create_group/',
         user_views.create_group, name='create_group'),
    path('admin_dashboard/group_list/', user_views.group_list, name='group_list'),
    path('no_permission', user_views.no_permission, name='no_permission'),
    path('organizer_dashboard/', event_views.OrganizerDashboardView.as_view(),
         name='organizer_dashboard'),
    path('participant_dashboard/', event_views.ParticipantDashboardView.as_view(),
         name='participant_dashboard'),
    path('dashboard/', event_views.dashboard, name="dashboard"),
    path('profile/', user_views.profile, name='profile'),
    path('edit_profile/', user_views.edit_profile, name='edit_profile'),
    path('profile/change-password/', auth_views.PasswordChangeView.as_view(
        template_name='users/change_password.html', success_url='/profile/'), name='change_password'),
    path('profile/password-reset/', auth_views.PasswordResetView.as_view(
        template_name='users/password_reset.html'), name='password_reset'),
    path('profile/password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('profile/password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('profile/password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'), name='password_reset_complete'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
