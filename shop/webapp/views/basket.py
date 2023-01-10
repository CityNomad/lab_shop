from django.shortcuts import redirect, get_object_or_404, HttpResponseRedirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, ListView, DeleteView, CreateView

# Create your views here.

from webapp.models import Item, ItemsOrders, Order
from webapp.forms import ItemForm, SearchForm, OrderForm


class AddToCart(View):

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
        amount = 0
        total_sum = []
        form = OrderForm
        if request.session.get('pk'):
            id_list = request.session['pk']
            qty_list = request.session['qty']
            i = 0

            for pk in id_list:
                item = get_object_or_404(Item, pk=pk)
                items.append(item)
                p_sum = item.price * qty_list[i]
                total_sum.append(p_sum)
                i += 1

            for i in total_sum:
                amount += i
            request.session['pk'] = id_list
            request.session['qty'] = qty_list

        return render(request, 'carts/cart.html', {'items': items, 'amount': amount,
                                                   'form': form, 'total_sum': total_sum})


class DeleteFromCart(TemplateView):

    template_name = 'carts/delete.html'
    context_object_name = 'item'

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        id_list = request.session.get('pk')
        index = id_list.index(pk)
        id_list.remove(pk)
        qty_list = request.session.get('qty')
        q = qty_list[index]
        qty_list.remove(q)
        request.session['pk'] = id_list
        request.session['qty'] = qty_list

        return redirect('webapp:cart')


class CreateOrder(CreateView):
    model = Order
    template_name = 'carts/cart.html'
    form_class = OrderForm

    def form_valid(self, form):
        self.object = form.save()
        if self.request.user.is_authenticated:
            self.object.user = self.request.user
        ordercart = ItemsOrders
        for i in range(len(self.request.session['pk'])):
            ordercart.objects.create(quantity=self.request.session['qty'][i],
                                     order_id=self.object.pk, product_id=self.request.session['pk'][i])
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
    model = Order
    context_object_name = 'orders'

    def get_queryset(self):
        pk = self.request.user.pk
        return Order.objects.filter(user_id=pk)

