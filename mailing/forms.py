from django.forms import BooleanField, ModelForm
from django import forms
from mailing.models import Message, Client, Mailing


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class MailingForm(StyleFormMixin, ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['message'].queryset = Message.objects.filter(owner=self.instance.owner)
        self.fields['clients'].queryset = Client.objects.filter(owner=self.instance.owner)

    class Meta:
        model = Mailing
        fields = ['name', 'first_send_datetime',
                  'last_send_datetime', 'period', 'status', 'message',
                  'clients']
        widgets = {
            'first_send_datetime': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}),
            'last_send_datetime': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}),
            # multiple select for many-to-many relation
            'clients': forms.SelectMultiple(
                attrs={'multiple': True}),
        }


