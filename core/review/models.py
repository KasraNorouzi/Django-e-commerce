from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.dispatch import receiver
from django.db.models import Avg
from django.db.models.signals import post_save


class ReviewStatusTypeModel(models.IntegerChoices):
    pending = 1, "در انتظار تایید"
    accepted = 2, "تایید شده"
    rejected = 3, "رد شده"


class ReviewModel(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    product = models.ForeignKey('shop.ProductModel', on_delete=models.CASCADE)
    review = models.TextField()
    rating = models.IntegerField(default=0, validators=[
        MinValueValidator(0), MaxValueValidator(5)
    ])
    status = models.IntegerField(choices=ReviewStatusTypeModel.choices,
                                 default=ReviewStatusTypeModel.pending.value)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return f'{self.user} - {self.product.id}'

    def get_status(self):
        return {
            'id': self.status,
            'title': ReviewStatusTypeModel(self.status).name,
            'label': ReviewStatusTypeModel(self.status).label,
        }


@receiver(post_save, sender=ReviewModel)
def calculate_avg_rating(sender, instance, created, **kwargs):
    if instance.status == ReviewStatusTypeModel.accepted.value:
        product = instance.product
        average_rating = ReviewModel.objects.filter(product=product,
                                                    status=ReviewStatusTypeModel.accepted).aggregate(Avg('rate'))['rate__avg']
        product.avg_rate = round(average_rating, 1)
        product.save()
