from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, DeleteView, UpdateView
from django.db.models import Q
from django.utils.http import urlencode
# Create your views here.

from webapp.models import Item, CATEGORIES_CHOICES
from webapp.forms import ItemForm, SearchForm, AddToBasketForm


class IndexView(ListView):
    model = Item
    template_name = "items/index.html"
    context_object_name = "items"
    ordering = 'name'
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        self.answer_form = self.get_answer_form()
        self.answer_value = self.get_answer_value()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if self.search_value:
            return Item.objects.filter(
                Q(name__icontains=self.search_value) | Q(description__icontains=self.search_value))
        return Item.objects.filter(balance__gt=0).order_by(('category'), ('name').lower())

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["form"] = self.form
        context['form2'] = AddToBasketForm

        if self.search_value:
            query = urlencode({'search': self.search_value})
            context['query'] = query
            context['search'] = self.search_value
        return context

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get("search")

    def get_answer_form(self):
        return AddToBasketForm(self.request.GET)

    def get_answer_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get("answer")


class ItemView(TemplateView):
    template_name = "items/item_view.html"

    def get_context_data(self, **kwargs):
        pk = kwargs.get("pk")
        item = get_object_or_404(Item, pk=pk)
        kwargs["item"] = item
        kwargs['form2'] = AddToBasketForm
        return super().get_context_data(**kwargs)


class CreateItem(CreateView):
    template_name = 'items/create_item.html'
    model = Item
    form_class = ItemForm

    def get_success_url(self):
        return reverse('item_view', kwargs={'pk': self.object.pk})


class UpdateItem(UpdateView):
    model = Item
    form_class = ItemForm
    context_object_name = 'item'
    template_name = 'items/update.html'

    def get_success_url(self):
        return reverse('item_view', kwargs={'pk': self.object.pk})


class DeleteItem(DeleteView):
    model = Item
    context_object_name = 'item'
    success_url = reverse_lazy('index')