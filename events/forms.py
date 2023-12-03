from django import forms
from .models import EventModel

class EventCreationForm(forms.ModelForm):
    class Meta:
        model = EventModel
        fields = [
            'title',
            'teaser',
            'event_image',
            'description',
            'ticket_price',
            'event_date',
            'event_time',
            'city',
            'venue',
        ]
        widgets = {
            'event_date': forms.DateInput(attrs={'type': 'date'}),
            'event_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-input-field'})
        self.fields['teaser'].widget.attrs.update({'class': 'form-input-field'})
        self.fields['event_image'].widget.attrs.update({'class': 'form-input-field'})
        self.fields['description'].widget.attrs.update({'class': 'form-input-field'})
        self.fields['ticket_price'].widget.attrs.update({'class': 'form-input-field'})
        self.fields['event_date'].widget.attrs.update({'class': 'form-date-time-field'})
        self.fields['event_time'].widget.attrs.update({'class': 'form-date-time-field'})
        self.fields['city'].widget.attrs.update({'class': 'form-input-field'})
        self.fields['venue'].widget.attrs.update({'class': 'form-input-field'})


class EventEditForm(forms.ModelForm):
    class Meta:
        model = EventModel
        fields = [
            'title',
            'teaser',
            'event_image',
            'description',
            'ticket_price',
            'event_date',
            'event_time',
            'city',
            'venue',
        ]