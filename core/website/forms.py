from django import forms
from .models import ContactModel, NewsLetterModel


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactModel
        fields = ['full_name', 'email', 'phone_number', 'subject', 'message']

        error_messages = {
            'full_name': {
                'required': 'فیلد نام و نام خانوادگی نمی تواند خالی باشد'
            },
            'email': {
                'required': 'فیلد ایمیل نمی تواند خالی باشد'
            },
            'subject': {
                'required': 'فیلد  عنوان نمی تواند خالی باشد'
            },
            'message': {
                'required': 'فیلد نام و نام خانوادگی نمی تواند خالی باشد'
            }
        }


class NewsLetterForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, required=False)

    class Meta:
        model = NewsLetterModel
        fields = ['first_name', 'email']

    def clean_first_name(self):
        if len(self.cleaned_data['first_name']) > 0:
            return forms.ValidationError('Please leave this field blank.')
        return self.cleaned_data['first_name']

    def save(self, commit=True):
        newsletter, created = NewsletterModel.objects.get_or_create(email=self.cleaned_data.get('email'))
        return newsletter
