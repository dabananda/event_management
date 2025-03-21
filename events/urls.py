from django.urls import path
from events import views

app_name = 'events'

urlpatterns = [
    path('', views.index, name='index'),
    path('organizer_dashboard/', views.organizer_dashboard,
         name='organizer_dashboard'),
    path('create_event/', views.create_event,
         name='create_event'),
    path('create_category/', views.create_category,
         name='create_category'),
    path('all_categories/', views.all_categories,
         name='all_categories'),
    path('create_participant/', views.create_participant,
         name='create_participant'),
]
