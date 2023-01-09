from django.db import models

# Create your models here.

CATEGORIES_CHOICES = [('other', 'Other'), ('fishing', 'Fishing'), ('hunting', 'Hunting'), ('skiing', 'Skiing'),
                      ('diving', 'Diving')]


class Item(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name="Name")
    description = models.TextField(max_length=2000, null=True, blank=True, verbose_name="Description")
    category = models.CharField(max_length=50, null=False, blank=False, choices=CATEGORIES_CHOICES,
                                verbose_name="Category", default=CATEGORIES_CHOICES[0][0])
    balance = models.PositiveIntegerField(verbose_name="Balance")
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Price")
    orders = models.ManyToManyField('webapp.Order', related_name='items', blank=True)

    def __str__(self):
        return f"{self.id}. {self.name}: {self.category}"

    class Meta:
        db_table = "items"
        verbose_name = "Item"
        verbose_name_plural = "Items"


class Basket(models.Model):
    item = models.ForeignKey('webapp.Item', on_delete=models.CASCADE,
                             related_name='baskets', verbose_name="Item")
    amount = models.PositiveIntegerField(verbose_name="Amount")

    def __str__(self):
        return f"{self.id}. {self.item}: {self.amount}"

    class Meta:
        db_table = "basket"
        verbose_name = "Basket"
        verbose_name_plural = "Baskets"


class Order(models.Model):
    username = models.CharField(max_length=50, null=False, blank=False, verbose_name="Username")
    phonenumber = models.CharField(max_length=50, null=False, blank=False, verbose_name="Phone number")
    address = models.CharField(max_length=1000, null=False, blank=False, verbose_name="Address")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")

    def __str__(self):
        return f"{self.id}. {self.username}: {self.phonenumber}"

    class Meta:
        db_table = "order"
        verbose_name = "Order"
        verbose_name_plural = "Orders"


class ItemsOrders(models.Model):
    item = models.ForeignKey("webapp.Item", on_delete=models.CASCADE,
                             related_name='itemsorders', verbose_name="Item")
    order = models.ForeignKey("webapp.Order", on_delete=models.CASCADE, related_name='itemsorders',
                              verbose_name="Order")
    quantity = models.PositiveIntegerField(verbose_name="Amount")

    def __str__(self):
        return f"{self.id}. {self.item}: {self.order}: {self.quantity}"

    class Meta:
        verbose_name = "Confirmed order"
        verbose_name_plural = "Confirmed orders"
