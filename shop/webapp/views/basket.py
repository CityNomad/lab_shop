from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404, HttpResponseRedirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView

from webapp.models import Item, ItemsOrders, Order
from webapp.forms import OrderForm


class AddToCart(View):

    def post(self, request, *args, **kwargs):
        quantity = int(request.POST.get('qty'))
        pk = self.kwargs.get('pk')
        item = get_object_or_404(Item, pk=pk)
        if not request.session.get('pk') or not request.session.get('qty'):
            request.session['pk'] = []
            request.session['qty'] = []
        id_list = request.session['pk']
        qty_list = request.session['qty']

        if pk not in id_list:
            id_list.append(pk)
            if item.balance >= quantity:
                qty = quantity
                qty_list.append(qty)
                messages.success(request, f'Item "{item.name}" added to a cart, {qty} pieces')
            else:
                messages.error(request, f'Item {item.name} balance is not enough to add to your cart')

        elif pk in id_list:
            if item.balance >= quantity:
                index = id_list.index(pk)
                qty = qty_list[index]
                qty = qty + quantity
                qty_list[index] = qty
                messages.success(request, f'Item "{item.name}" added to a cart, {qty} pieces')
            else:
                messages.error(request, f'Item {item.name} balance is not enough to add to your cart')

        request.session['pk'] = id_list
        request.session['qty'] = qty_list

        return redirect(reverse('webapp:index'))

    def get(self, request, *args, **kwargs):
        quantity = 0
        pk = self.kwargs.get('pk')
        item = get_object_or_404(Item, pk=pk)
        if not request.session.get('pk') or not request.session.get('qty'):
            request.session['pk'] = []
            request.session['qty'] = []
        id_list = request.session['pk']
        qty_list = request.session['qty']
        if pk not in id_list:
            id_list.append(pk)
            if item.balance > 0:
                qty = quantity + 1
                qty_list.append(qty)
                messages.success(request, f'Item "{item.name}" added to a cart, {qty} pieces')
            else:
                messages.error(request, f'Item {item.name} balance is not enough to add to your cart')

        elif pk in id_list:
            if item.balance > 0:
                index = id_list.index(pk)
                qty = qty_list[index]
                qty = qty + 1
                qty_list[index] = qty
                messages.success(request, f'Item "{item.name}" added to a cart, {qty} pieces')
            else:
                messages.error(request, f'Item {item.name} balance is not enough to add to your cart')

        request.session['pk'] = id_list
        request.session['qty'] = qty_list

        return redirect(reverse('webapp:index'))


class Cart(TemplateView):
    template_name = 'carts/cart.html'

    def get(self, request, *args, **kwargs):
        items = []
        total_sum = 0
        items_sum = []
        form = OrderForm
        if request.session.get('pk'):
            id_list = request.session['pk']
            qty_list = request.session['qty']
            i = 0

            for pk in id_list:
                product = dict()
                item = get_object_or_404(Item, pk=pk)
                product['name'] = item.name
                product['pk'] = item.pk
                product['price'] = item.price
                qty = qty_list[i]
                product['qty'] = qty
                p_sum = item.price * qty
                product['items_sum'] = p_sum
                items_sum.append(p_sum)
                items.append(product)
                i += 1
            for k in items_sum:
                total_sum += k
            request.session['pk'] = id_list
            request.session['qty'] = qty_list
        return render(request, 'carts/cart.html', {'items': items, 'total_sum': total_sum,
                                                   'form': form})


def delete_from_cart(request, pk):
    id_list = request.session.get('pk')
    item = get_object_or_404(Item, pk=pk)
    index = id_list.index(pk)
    id_list.remove(pk)
    qty_list = request.session.get('qty')
    quantity = qty_list[index]
    qty_list.remove(quantity)
    request.session['pk'] = id_list
    request.session['qty'] = qty_list
    messages.warning(request, f'Item {item.name} was successfully removed from the cart')

    return redirect('webapp:cart')


def delete_one_by_one(request, pk):
    item = get_object_or_404(Item, pk=pk)
    id_list = request.session.get('pk')
    index = id_list.index(pk)
    qty_list = request.session.get('qty')
    quantity = qty_list[index]
    if quantity > 1:
        new_quantity = quantity - 1
        qty_list[index] = new_quantity
        request.session['pk'] = id_list
        request.session['qty'] = qty_list
        messages.warning(request, f'1 piece of {item.name} was removed from the cart')
    else:
        id_list.remove(pk)
        qty_list.remove(quantity)
        request.session['pk'] = id_list
        request.session['qty'] = qty_list
        messages.warning(request, f'Item {item.name} was successfully removed from the cart')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class Checkout(CreateView):
    model = Order
    template_name = 'carts/cart.html'
    form_class = OrderForm

    def form_valid(self, form):
        self.object = form.save()
        if self.request.user.is_authenticated:
            self.object.user = self.request.user
        order = ItemsOrders
        for i in range(len(self.request.session['pk'])):
            order.objects.create(quantity=self.request.session['qty'][i], order_id=self.object.pk,
                                 item_id=self.request.session['pk'][i])
        id_list = self.request.session['pk']
        id_list.clear()
        self.request.session['pk'] = id_list
        qty_list = self.request.session['qty']
        qty_list.clear()
        self.request.session['pk'] = qty_list
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('webapp:index')


class OrderView(ListView):
    template_name = 'carts/orderview.html'
    model = ItemsOrders
    context_object_name = 'itemsorders'

    def get_queryset(self, *args, **kwargs):
        user = self.request.user.username
        return ItemsOrders.objects.filter(order__username=user)
