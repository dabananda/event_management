from django.urls import path
from events import views

app_name = 'events'

urlpatterns = [
    path('search/', views.SearchResultsView.as_view(), name='search_results'),

    # Event
    path('create_event/', views.CreateEventView.as_view(),
         name='create_event'),
    path('all_events/', views.AllEventsView.as_view(),
         name='all_events'),
    path('update_event/<int:id>/',
         views.UpdateEventView.as_view(), name='update_event'),
    path('delete_event/<int:id>/',
         views.DeleteEventView.as_view(), name='delete_event'),
    path('event/<int:id>/', views.EventDetailView.as_view(), name='event_detail'),

    # Category
    path('create_category/', views.CreateCategoryView.as_view(),
         name='create_category'),
    path('all_categories/', views.AllCategoriesView.as_view(),
         name='all_categories'),
    path('update_category/<int:id>', views.UpdateCategoryView.as_view(),
         name='update_category'),
    path('delete_category/<int:id>', views.DeleteCategoryView.as_view(),
         name='delete_category'),
    path('category/<int:id>/',
         views.EventsByCategoryView.as_view(), name='events_by_category'),

    # RSVP
    path('rsvp/<int:event_id>/', views.RSVPEventView.as_view(), name='rsvp_event'),
]
