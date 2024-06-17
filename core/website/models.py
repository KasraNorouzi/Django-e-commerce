from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ContactModel(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(default='<EMAIL>')
    phone_number = models.CharField(max_length=100)
    subject = models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField()
    is_seen = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_date']

    def __str__(self):
        return f'name: {self.full_name} email: {self.email}'


class NewsLetterModel(models.Model):
    email = models.EmailField(default='<EMAIL>')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email
