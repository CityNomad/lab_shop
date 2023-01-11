from django.shortcuts import redirect, get_object_or_404, HttpResponseRedirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView

from webapp.models import Item, ItemsOrders, Order
from webapp.forms import OrderForm


class AddToCart(View):

    def post(self, request, *args, **kwargs):
        quantity = 0
        pk = self.kwargs.get('pk')
        if not request.session.get('pk') or not request.session.get('qty'):
            request.session['pk'] = []
            request.session['qty'] = []
        id_list = request.session['pk']
        qty_list = request.session['qty']
        if pk not in request.session['pk']:
            id_list.append(pk)
            item = get_object_or_404(Item, pk=pk)
            if item.balance != 0:
                qty = quantity + 1
                qty_list.append(qty)

        elif pk in id_list:
            product = get_object_or_404(Item, pk=pk)
            if product.balance != 0:
                index = id_list.index(pk)
                qty = qty_list[index]
                qty = qty + 1
                qty_list[index] = qty

        request.session['pk'] = id_list
        request.session['qty'] = qty_list

        return redirect(reverse('webapp:index'))

    def get(self, request, *args, **kwargs):
        quantity = 0
        pk = self.kwargs.get('pk')
        if not request.session.get('pk') or not request.session.get('qty'):
            request.session['pk'] = []
            request.session['qty'] = []
        id_list = request.session['pk']
        qty_list = request.session['qty']
        if pk not in request.session['pk']:
            id_list.append(pk)
            product = get_object_or_404(Item, pk=pk)
            if product.balance != 0:
                qty = quantity + 1
                qty_list.append(qty)

        elif pk in id_list:
            product = get_object_or_404(Item, pk=pk)
            if product.balance != 0:
                index = id_list.index(pk)
                qty = qty_list[index]
                qty = qty + 1
                qty_list[index] = qty

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
                # item['qty'] = qty_list[i]
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
                print(product)
            for k in items_sum:
                total_sum += k
            request.session['pk'] = id_list
            request.session['qty'] = qty_list
        print(items)
        return render(request, 'carts/cart.html', {'items': items, 'total_sum': total_sum,
                                                   'form': form})


def delete_from_cart(request, pk):
    id_list = request.session.get('pk')
    index = id_list.index(pk)
    id_list.remove(pk)
    qty_list = request.session.get('qty')
    quantity = qty_list[index]
    qty_list.remove(quantity)
    request.session['pk'] = id_list
    request.session['qty'] = qty_list

    return redirect('webapp:cart')


def delete_one_by_one(request, pk):
    id_list = request.session.get('pk')
    index = id_list.index(pk)
    qty_list = request.session.get('qty')
    quantity = qty_list[index]
    if quantity > 1:
        new_quantity = quantity - 1
        qty_list[index] = new_quantity
        request.session['pk'] = id_list
        request.session['qty'] = qty_list
    else:
        id_list.remove(pk)
        qty_list.remove(quantity)
        request.session['pk'] = id_list
        request.session['qty'] = qty_list

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
