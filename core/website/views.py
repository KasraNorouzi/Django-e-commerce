from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views.generic import CreateView
from website.forms import ContactForm, NewsLetterForm


class IndexView(TemplateView):
    template_name = 'website/index.html'


class ContactView(TemplateView):
    template_name = 'website/contact.html'


class AboutView(TemplateView):
    template_name = 'website/about.html'


class SendContactView(CreateView):
    http_method_names = ['post']
    form_class = ContactForm

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'تیکت شما با موفقیت ثبت شد.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, 'مشکلی در ارسال فرم شما پیش آمد لطفا ورودی ها رو بررسی کنین و مجدد ارسال نمایید'
        )
        return redirect(self.request.META.get('HTTP_REFERER'))

    def get_success_url(self):
        """
        This allows the user to be redirected back to the page they were on before submitting the form
        """
        return self.request.META.get('HTTP_REFERER')


class NewsletterView(CreateView):
    http_method_names = ['post']
    form_class = NewsLetterForm
    success_url = '/'

    def form_valid(self, form):
        messages.success(self.request, 'از ثبت نام شما ممنونم، اخبار جدید رو براتون ارسال می کنم')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'مشکلی در ارسال فرم شما وجود داشت')
        return redirect('website:index')
