from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('categories/new/', views.CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/edit/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),
    
    path('events/', views.EventListView.as_view(), name='event_list'),
    path('events/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('events/new/', views.EventCreateView.as_view(), name='event_create'),
    path('events/<int:pk>/edit/', views.EventUpdateView.as_view(), name='event_update'),
    path('events/<int:pk>/delete/', views.EventDeleteView.as_view(), name='event_delete'),
    
    path('participants/', views.ParticipantListView.as_view(), name='participant_list'),
    path('participants/<int:pk>/', views.ParticipantDetailView.as_view(), name='participant_detail'),
    path('participants/new/', views.ParticipantCreateView.as_view(), name='participant_create'),
    path('participants/<int:pk>/edit/', views.ParticipantUpdateView.as_view(), name='participant_update'),
    path('participants/<int:pk>/delete/', views.ParticipantDeleteView.as_view(), name='participant_delete'),
]