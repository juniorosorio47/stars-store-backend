from rest_framework import serializers
from .models import Order, OrderItem
from products.models import Product

class OrderItemSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField('get_product_price')
    product = serializers.SerializerMethodField('get_product')


    def get_product_price(self, object):
        product = Product.objects.all().filter(id=object.product.id).first()

        return product.price

    def get_product(self, object):
        product = Product.objects.all().filter(id=object.product.id).first()

        product = {
            'id': product.id,
            'name': product.name,
            'description': product.description,
        }

        return product

    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    total = serializers.SerializerMethodField('get_total')
    
    def get_total(self, object):
        items = OrderItem.objects.all().filter(order_id=object.id)

        return sum((o.product.price * o.quantity) for o in items)

    class Meta:
        model = Order
        fields = '__all__'