from django import forms
from .models import EventModel, BookEventModel, Review


class EventCreationForm(forms.ModelForm):
    """
    Form for users to create events which works off the `EventModel`.
    Uses widgets to assign input types to `event_date` and `event_time`.
    Also assigns classes to input fields.
    """
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
        self.fields['teaser'].widget.attrs.update({'class': 'form-input-field'})  # noqa
        self.fields['event_image_url'].widget.attrs.update({'class': 'form-input-field'})  # noqa
        self.fields['description'].widget.attrs.update({'class': 'form-input-field'})  # noqa
        self.fields['ticket_price'].widget.attrs.update({'class': 'form-input-field'})  # noqa
        self.fields['event_date'].widget.attrs.update({'class': 'form-date-time-field'})  # noqa
        self.fields['event_time'].widget.attrs.update({'class': 'form-date-time-field'})  # noqa
        self.fields['city'].widget.attrs.update({'class': 'form-input-field'})
        self.fields['venue'].widget.attrs.update({'class': 'form-input-field'})


class EventEditForm(forms.ModelForm):
    """
    Form for users to edit their created events. This form contains
    the exact same functionality as the `EventCreationForm`.
    """
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
        self.fields['teaser'].widget.attrs.update({'class': 'form-input-field'})  # noqa
        self.fields['event_image_url'].widget.attrs.update({'class': 'form-input-field'})  # noqa
        self.fields['description'].widget.attrs.update({'class': 'form-input-field'})  # noqa
        self.fields['ticket_price'].widget.attrs.update({'class': 'form-input-field'})  # noqa
        self.fields['event_date'].widget.attrs.update({'class': 'form-date-time-field'})  # noqa
        self.fields['event_time'].widget.attrs.update({'class': 'form-date-time-field'})  # noqa
        self.fields['city'].widget.attrs.update({'class': 'form-input-field'})
        self.fields['venue'].widget.attrs.update({'class': 'form-input-field'})


class BookingForm(forms.ModelForm):
    """
    Form for users to book an event using the `BookEventModel`. Uses
    widgets in the `__init__` method to assign a select input field
    type to the `num_of_tickets` field.
    """
    class Meta:
        model = BookEventModel
        fields = ['num_of_tickets']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['num_of_tickets'].widget = forms.Select(choices=[(i, i) for i in range(1, 11)])  # noqa
        self.fields['num_of_tickets'].widget.attrs.update({'class': 'form-input-field'})  # noqa


class ReviewForm(forms.ModelForm):
    """
    Form for users to leave reviews on events using the `Review`
    model. Uses widgets to add class attributes and values to
    each input field.
    """
    class Meta:
        model = Review
        fields = ['review_title', 'review_text', 'review_score']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['review_title'].widget.attrs.update({'class': 'form-input-field'})  # noqa
        self.fields['review_text'].widget.attrs.update({'class': 'form-input-field'})  # noqa
        self.fields['review_score'].widget.attrs.update({'class': 'form-input-field'})  # noqa


class EditReviewForm(forms.ModelForm):
    """
    Form for users to edit their events. This form uses the exact
    same functionality as `ReviewForm`.
    """
    class Meta:
        model = Review
        fields = ['review_title', 'review_text', 'review_score']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['review_title'].widget.attrs.update({'class': 'form-input-field'})  # noqa
        self.fields['review_text'].widget.attrs.update({'class': 'form-input-field'})  # noqa
        self.fields['review_score'].widget.attrs.update({'class': 'form-input-field'})  # noqa
