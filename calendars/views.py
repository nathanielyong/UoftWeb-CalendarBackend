from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ValidationError
from django.views.generic.edit import FormView
from django.views.generic import ListView, DetailView, UpdateView
from .forms import CalendarForm, EventForm
from .models import Calendar, Event
from django.views.decorators.http import require_GET
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator


class CalendarCreateView(FormView): 
    template_name = 'calendars/create.html'
    form_class = CalendarForm

    def dispatch(self, request, *a, **k):
        if not request.user.is_authenticated:
            return HttpResponse(status=401)
        return super().dispatch(request, *a, **k)

    def form_valid(self, form):
        calendar = form.save(commit=False)
        calendar.owner = self.request.user
        calendar.save()
        self.calendar_id = calendar.pk
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('calendar_details', args=[self.calendar_id])


class CreateEventView(FormView):
    template_name = 'calendars/create_event.html'
    form_class = EventForm

    def dispatch(self, request, *a, **k):
        if not request.user.is_authenticated:
            return HttpResponse(status=401)

        self.calendar = get_object_or_404(Calendar, pk=k['calendar_id'])
        if self.calendar.owner != self.request.user:
            return HttpResponse(status=403)
        return super().dispatch(request, *a, **k)

    def form_valid(self, form):
        form.instance.calendar = self.calendar
        self.event = form.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('event_details', kwargs={'event_id': self.event.pk})
    

@require_GET
def event_details(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    response_data = {
        "id": event.id,
        "name": event.name,
        "description": event.description,
        "date": event.date,
        "start_time": event.start_time,
        "duration": event.duration,
        "last_modified": event.last_modified
    }

    return JsonResponse(response_data)


class EventListView(ListView):
    template_name = 'calendars/event_list.html' 
    context_object_name = 'event_list'  

    def get_queryset(self):
        calendar_id = self.kwargs['calendar_id']
        return Event.objects.filter(calendar__id=calendar_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        authenticated = self.request.user.is_authenticated
        if not authenticated:
            for event in context['event_list']:
                event.name = ''
        return context
    

@method_decorator(require_GET, name='dispatch')
class CalendarDetailView(DetailView):
    model = Calendar
    template_name = 'calendars/detail.html'
    context_object_name = 'calendar'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class EventUpdateView(UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'calendars/edit_event.html'

    def dispatch(self, request, *a, **k):
        if not request.user.is_authenticated:
            return HttpResponse(status=401)
        if request.user != self.get_object().calendar.owner:
            return HttpResponse(status=403)
        return super().dispatch(request, *a, **k)
    
    def form_valid(self, form):
        event = form.save(commit=False)
        event.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event_id'] = self.kwargs['pk']
        return context
    
    def get_success_url(self):
        return reverse_lazy('event_details', kwargs={'event_id': self.object.id})
    