from stars_store.pagination import CustomPagination
from rest_framework import generics, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.auth import JWTAuthentication

from .models import Client
from .serializers import ClientSerializer


class ClientGenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
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
