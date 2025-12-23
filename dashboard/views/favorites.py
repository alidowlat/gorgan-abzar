from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from product.models import Favorite


class FavoriteProductsView(LoginRequiredMixin, ListView):
    model = Favorite
    template_name = 'dashboard/favorites/main.html'
    context_object_name = 'favorites'

    def get_queryset(self):
        return Favorite.objects.select_related('product').filter(user=self.request.user)
