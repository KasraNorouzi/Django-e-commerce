from django.views.generic import (TemplateView, ListView,
                                  DetailView, View)
from django.db.models import Q

from review.models import ReviewModel, ReviewStatusTypeModel
from .models import ProductModel, ProductStatusType, ProductCategoryModel, WishlistModel
from django.core.exceptions import FieldError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse


class ProductGridView(ListView):
    model = ProductModel
    paginate_by = 10
    template_name = 'shop/product-grid.html'

    def get_queryset(self):
        queryset = ProductModel.objects.filter(status=ProductStatusType.publish.value)
        if search_q := self.request.GET.get("q"):
            queryset = queryset.filter(title__icontains=search_q)
        if category_id := self.request.GET.get("category_id"):
            queryset = queryset.filter(category__id=category_id)
        if min_price := self.request.GET.get("min_price"):
            queryset = queryset.filter(price__gte=min_price)
        if max_price := self.request.GET.get("max_price"):
            queryset = queryset.filter(price__lte=max_price)
        if order_by := self.request.GET.get("order_by"):
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_items"] = self.get_queryset().count()
        context["wishlist_items"] = WishlistModel.objects.filter(user=self.request.user).values_list(
            "product__id", flat=True) if self.request.user.is_authenticated else []
        context["categories"] = ProductCategoryModel.objects.all()
        return context


class ProductDetailView(DetailView):
    template_name = 'shop/product-detail.html'
    queryset = ProductModel.objects.filter(status=ProductStatusType.publish.value)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context['is_wished'] = WishlistModel.objects.filter(user=self.request.user,
                                                            product__id=product.id).exists() if self.request.user.is_authenticated else False
        reviews = ReviewModel.objects.filter(product=product, status=ReviewStatusTypeModel.accepted.value)
        context['reviews'] = reviews
        total_reviews_count = reviews.count()
        context["reviews_count"] = {
            f"rate_{rate}": reviews.filter(rate=rate).count() for rate in range(1, 6)
        }
        if total_reviews_count != 0:
            context["reviews_avg"] = {
                f"rate_{rate}": round((reviews.filter(rate=rate).count() / total_reviews_count) * 100, 2) for rate in
                range(1, 6)
            }
        else:
            context["reviews_avg"] = {f"rate_{rate}": 0 for rate in range(1, 6)}
        return context

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.product_images.prefetch_related()
        return obj


class AddOrRemoveWishListView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        product_id = request.POST.get("product_id")
        message = ''
        if product_id:
            try:
                wishlist_item = WishlistModel.objects.get(user=request.user,
                                                          product_id=product_id)
                wishlist_item.delete()
                message = 'محصول از لیست علایق حذف شد'
            except WishlistModel.DoesNotExist:
                WishlistModel.objects.create(
                    user=request.user, product_id=product_id
                )
                message = 'محصول به لیست علایق اضافه شد'

        return JsonResponse({'message': message})
