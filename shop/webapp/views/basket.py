from django.shortcuts import redirect, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView, ListView, DeleteView

# Create your views here.

from webapp.models import Item, Basket, ItemsOrders
from webapp.forms import ItemForm, SearchForm, OrderForm


def add_item_basket(request, pk):
    item = get_object_or_404(Item, pk=pk)
    Basket.objects.all()

    if request.method == "POST":
        user_amount = request.POST.get('amount')
        if item.balance != 0:
            try:
                product = get_object_or_404(Basket, item_id=item.pk)
                old_amount = product.amount
                new_amount = int(old_amount) + int(user_amount)

                if item.balance > new_amount:
                    Basket.objects.filter(item_id=item.pk).update(amount=new_amount)
                else:
                    new_amount = item.balance
                    Basket.objects.filter(item_id=item.pk).update(amount=new_amount)
            except:
                Basket.objects.create(item_id=pk, amount=user_amount)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    elif request.method == "GET":
        item = get_object_or_404(Item, pk=pk)
        amount = 1
        if item.balance != 0:
            try:
                product = get_object_or_404(Basket, item_id=item.pk)
                new_amount = int(product.amount) + amount

                if item.balance > new_amount:
                    Basket.objects.filter(item_id=item.pk).update(amount=new_amount)
                else:
                    new_amount = item.balance
                    Basket.objects.filter(item_id=item.pk).update(amount=new_amount)
            except:
                Basket.objects.create(item_id=pk, amount=amount)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class BasketView(ListView):
    model = Basket
    template_name = "baskets/basket_view.html"
    context_object_name = "baskets"

    def get_total(self):
        baskets = Basket.objects.all()
        for product in baskets:
            total = product.amount * product.item.price
            product.total = total
            product.save()
        return baskets

    def get_overall(self):
        overall = 0
        baskets = Basket.objects.all()
        for product in baskets:
            total = product.amount * product.item.price
            overall += total
        return overall

    def get_queryset(self):
        return Basket.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['baskets'] = self.get_total()
        context['overall'] = self.get_overall()
        context['form'] = OrderForm
        return context


class DeleteFromBasket(DeleteView):
    model = Basket

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('basket_view')


def delete_one_by_one(request, pk):
    product = get_object_or_404(Basket, pk=pk)
    if product.amount > 1:
        product.amount = product.amount - 1
        product.save()
    else:
        Basket.objects.filter(pk=pk).delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


