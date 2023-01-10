from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView
from webapp.forms import OrderForm
from webapp.models import ItemsOrders, Order, Item
# Create your views here.


class CreateOrder(CreateView):
    model = Order
    template_name = 'baskets/basket_view.html'
    form_class = OrderForm

    # def form_valid(self, form):
    #     self.object = form.save()
    #     items = Basket.objects.all()
    #     order = self.object.pk
    #     for i in items:
    #         ItemsOrders.objects.create(order_id=order, item_id=i.item.pk, quantity=i.amount)
    #         product = get_object_or_404(Item, pk=i.item.pk)
    #         remain = product.balance - i.amount
    #         product.balance = remain
    #         product.save()
    #     Basket.objects.all().delete()
    #     return super().form_valid(form)

    def get_success_url(self):
        return reverse('index')