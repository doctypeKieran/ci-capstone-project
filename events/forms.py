from django import forms
from .models import EventModel, BookEventModel, Review

class EventCreationForm(forms.ModelForm):
    class Meta:
        model = EventModel
        fields = [
            'title',
            'teaser',
            'event_image_url',
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
        self.fields['event_image_url'].widget.attrs.update({'class': 'form-input-field'})
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
            'event_image_url',
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
        self.fields['event_image_url'].widget.attrs.update({'class': 'form-input-field'})
        self.fields['description'].widget.attrs.update({'class': 'form-input-field'})
        self.fields['ticket_price'].widget.attrs.update({'class': 'form-input-field'})
        self.fields['event_date'].widget.attrs.update({'class': 'form-date-time-field'})
        self.fields['event_time'].widget.attrs.update({'class': 'form-date-time-field'})
        self.fields['city'].widget.attrs.update({'class': 'form-input-field'})
        self.fields['venue'].widget.attrs.update({'class': 'form-input-field'})


class BookingForm(forms.ModelForm):
    class Meta:
        model = BookEventModel
        fields = ['num_of_tickets']

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['num_of_tickets'].widget = forms.Select(choices=[(i, i) for i in range(1, 11)])
        self.fields['num_of_tickets'].widget.attrs.update({'class': 'form-input-field'})


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review_title', 'review_text', 'review_score']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['review_title'].widget.attrs.update({'class': 'form-input-field'})
        self.fields['review_text'].widget.attrs.update({'class': 'form-input-field'})
        self.fields['review_score'].widget.attrs.update({'class': 'form-input-field'})
