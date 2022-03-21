from stars_store.pagination import CustomPagination
from django.core.files.storage import default_storage
from rest_framework import exceptions, generics, mixins, status, viewsets
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from users.auth import JWTAuthentication
from users.permissions import ViewPermissions

from .models import Product
from .serializers import ProductSerializer


class ProductGenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated & ViewPermissions]
    # permission_object = 'products'
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = CustomPagination


    def get(self, request, pk=None):
        if pk:
            return Response({
                'data':self.retrieve(request, pk).data
            })
        
        return Response({
            'data':self.list(request).data
        })


    def post(self, request):

        return Response({
            'data': self.create(request).data
        })


    def put(self, request, pk=None):

        return Response({
            'data': self.partial_update(request, pk).data
        })


    def delete(self, request, pk=None):

        self.destroy(request, pk).data

        return Response(status=status.HTTP_204_NO_CONTENT)

class FileUploadView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,)

    def post(self, request):
        file = request.FILES['image']
        file_name = default_storage.save(file.name, file)
        url = default_storage.url(file_name)

        return Response({
            'url':f'http://localhost:8000/api{url}'
        })
