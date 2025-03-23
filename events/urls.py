from django.urls import path
from events import views

app_name = 'events'

urlpatterns = [
    path('', views.index, name='index'),
    path('organizer_dashboard/', views.organizer_dashboard,
         name='organizer_dashboard'),
    path('search/', views.search_results, name='search_results'),

    # Event
    path('create_event/', views.create_event,
         name='create_event'),
    path('all_events/', views.all_events,
         name='all_events'),
    path('update_event/<int:id>/', views.update_event, name='update_event'),
    path('delete_event/<int:id>/', views.delete_event, name='delete_event'),
    path('event/<int:id>/', views.event_detail, name='event_detail'),

    # Category
    path('create_category/', views.create_category,
         name='create_category'),
    path('all_categories/', views.all_categories,
         name='all_categories'),
    path('update_category/<int:id>', views.update_category,
         name='update_category'),
    path('delete_category/<int:id>', views.delete_category,
         name='delete_category'),
    path('category/<int:id>/',
         views.events_by_category, name='events_by_category'),

#     # Participant
#     path('create_participant/', views.create_participant,
#          name='create_participant'),
#     path('all_participants/', views.all_participants,
#          name='all_participants'),
#     path('update_participant/<int:id>/', views.update_participant,
#          name='update_participant'),
#     path('delete_participant/<int:id>', views.delete_participant,
#          name='delete_participant'),
]
