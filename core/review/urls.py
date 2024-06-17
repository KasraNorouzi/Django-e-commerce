from django.urls import path
from review import views

app_name = "review"

urlpatterns = [
    path("submit-review/", views.SubmitReviewView.as_view(), name="submit-review")
]
