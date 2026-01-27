from .serializers import StoreSerializer, ProductSerializer
from .models import Store, Product
from rest_framework import generics, response, status

# Create your views here.


class StoreList(generics.ListCreateAPIView):
    # API view to retrieve list of stores or create a new store
    queryset = Store.objects.all()
    serializer_class = StoreSerializer


class StoreDetailUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    # API view to retrieve, update or delete a store instance
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    lookup_field = 'store_id'


class StoreDeleteAll(generics.DestroyAPIView):
    # API view to delete all stores
    def delete(self, request, *args, **kwargs):
        # Delete all Store objects
        Store.objects.all().delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class ProductList(generics.ListCreateAPIView):
    # API view to retrieve list of products or create a new product
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    # API view to retrieve, update or delete a product instance
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'


class ProductDeleteAll(generics.DestroyAPIView):
    # API view to delete all products
    def delete(self, request, *args, **kwargs):
        Product.objects.all().delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)


from rest_framework.decorators import api_view
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request, format=None):
    return response.Response({
        'stores': reverse('store-list', request=request, format=format),
        'products': reverse('product-list', request=request, format=format),
    })

