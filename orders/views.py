import csv

from django.http import HttpResponse
from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from stars_store.pagination import CustomPagination
from users.auth import JWTAuthentication
from users.permissions import ViewPermissions

from .models import Order, OrderItem
from .serializers import OrderSerializer


class OrderGenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated & ViewPermissions]
    permission_object = 'orders'
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = CustomPagination


    def get(self, request, pk=None):
        if pk:
            return Response({
                'data':self.retrieve(request, pk).data
            })
        
        return Response({
            'data':self.list(request).data
        })



class ExportAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated & ViewPermissions]
    permission_object = 'orders'

    def get(self, request):
        response = HttpResponse(content_type='text/csv')

        response['Content-Disposition'] = 'attachment; filename=orders.csv'

        orders = Order.objects.all()
        writer = csv.writer(response)

        writer.writerow(['ID', 'Product', 'Price', 'Quantity'])

        for order in orders:
            writer.writerow([order.id, '', '', ''])
            orderItems = OrderItem.objects.all().filter(order_id=order.id)
            
            for item in orderItems:
                writer.writerow(['', item.product, item.price, item.quantity])

        return response
