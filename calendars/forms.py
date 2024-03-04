from django import forms
from .models import Calendar, Event
import datetime

class CalendarForm(forms.ModelForm):
    name = forms.CharField(required=True, error_messages={
        "required": "This field is required"
    })

    start_date = forms.CharField(required=True, error_messages={"required": "This field is required"})

    end_date = forms.CharField(required=True, error_messages={"required": "This field is required"})
    
    class Meta:
        model = Calendar
        fields = ['name', 'description', 'start_date', 'end_date']

    def start_date(self):
        start_date = self.cleaned_data.get("start_date")
        try:
            datetime.datetime.strptime(start_date, '%Y-%m-%d')
        except ValueError:
            raise forms.ValidationError('Enter a valid date (YYYY-MM-DD)')

        return start_date
    
    def end_date(self):
        end_date = self.cleaned_data.get("end_date")
        try:
            datetime.datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            raise forms.ValidationError('Enter a valid date (YYYY-MM-DD)')

        return end_date


class EventForm(forms.ModelForm):
    name = forms.CharField(required=True, error_messages={
        "required": "This field is required"
    })

    date = forms.CharField(required=True, error_messages={"required": "This field is required"})

    start_time = forms.CharField(required=True, error_messages={"required": "This field is required"})
    
    duration = forms.CharField(required=True, error_messages={"required": "This field is required"})
    
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'start_time', 'duration']

    def clean_date(self):
        date = self.cleaned_data.get("date")
        try:
            datetime.datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            raise forms.ValidationError('Enter a valid date (YYYY-MM-DD)')

        return date
    
    def clean_start_time(self):
        start_time = self.cleaned_data.get("start_time")
        try:
            datetime.datetime.strptime(start_time, '%H:%M')
        except ValueError:
            raise forms.ValidationError("Enter a valid time (hh:mm)")
        
        return start_time