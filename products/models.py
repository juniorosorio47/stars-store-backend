from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(max_length=1000)
    image = models.CharField(max_length=200)
    price = models.DecimalField(default=0.00, decimal_places=2, max_digits=20)
    inventory = models.IntegerField(default=0)
    multiple = models.IntegerField(default=1, blank=True, null=True)

    def has_inventory(self, quantity):
        if quantity > self.inventory:
            return False
        else:
            return True

    def decrease_inventory(self, quantity):
        if self.is_multiple(quantity) and quantity <= self.inventory:
            self.inventory -= quantity
            return True
        else:
            return False
    
    def increase_inventory(self, quantity):
        self.inventory += quantity
        return True

    def is_multiple(self, quantity):
        if self.multiple:
            return quantity%self.multiple == 0
        else:
            return False