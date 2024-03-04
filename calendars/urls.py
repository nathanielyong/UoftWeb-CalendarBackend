from django.urls import path
from .views import CalendarCreateView, CreateEventView, event_details, EventListView, CalendarDetailView, EventUpdateView

urlpatterns = [
    path('add/', CalendarCreateView.as_view(), name="calendar_create"),
    path('<int:calendar_id>/events/add/', CreateEventView.as_view(), name="event_create"),
    path('event/<int:event_id>/details/', event_details, name="event_details"),
    path('<int:calendar_id>/events/all/', EventListView.as_view(), name="event_list"),
    path('<int:pk>/details/', CalendarDetailView.as_view(), name="calendar_details"),
    path('event/<int:pk>/edit/', EventUpdateView.as_view(), name="edit_event")
]