from django.http import JsonResponse, Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from productapp.models import Order, Customer, Product, Order_Item
from rest_framework import status

from productapp.serializers import CustomerSerializer, ProductSerializer, OrderSerializer


# Customer view
class Customer_view(APIView):
    def get_Customer_object(self, pk):
        try:
            return Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            raise Http404

    def get(self, request):
        try:
            all_data = Customer.objects.all()
            serialized = CustomerSerializer(all_data, many=True)
            res = {
                "code": status.HTTP_200_OK,
                "message": "data get successfully",
                "data": serialized.data
            }
            return Response(res, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"code": status.HTTP_400_BAD_REQUEST, "message": str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            res = {
                "code": status.HTTP_200_OK,
                "message": "Customer added successfully"
            }
            return Response(res, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        obj = self.get_Customer_object(pk)
        serializer = CustomerSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            res = {
                "code": status.HTTP_200_OK,
                "message": "Customer update successfully"
            }
            return Response(res, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Product view
class Product_view(APIView):
    def get(self, request):
        try:
            all_data = Product.objects.all()
            serialized = ProductSerializer(all_data, many=True)
            res = {
                "code": status.HTTP_200_OK,
                "message": "data get successfully",
                "data": serialized.data
            }
            return Response(res, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"code": status.HTTP_400_BAD_REQUEST, "message": str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            serialized = ProductSerializer(data=request.data)
            if serialized.is_valid():
                serialized.save()
                res = {
                    "code": status.HTTP_200_OK,
                    "message": "Product added successfully"
                }
                return Response(res)
            else:
                res = {
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": serialized.errors
                }
                return Response(res, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"code": status.HTTP_400_BAD_REQUEST, "message": e}, status=status.HTTP_400_BAD_REQUEST)


# order views
class Order_view(APIView):
    def get(self, request):
        try:
            all_data = Order.objects.all()
            serialized = OrderSerializer(all_data, many=True)
            res = {
                "code": status.HTTP_200_OK,
                "message": "data get successfully",
                "data": serialized.data
            }
            return Response(res, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"code": status.HTTP_400_BAD_REQUEST, "message": str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        try:
            serializer = OrderSerializer(data=request.data)
            if serializer.is_valid():
                order = serializer.save()
                order_items_data = request.data.get('order_item', [])

                for item_data in order_items_data:
                    product_id = item_data.get('product')
                    quantity = item_data.get('quantity')
                    product = Product.objects.get(pk=product_id)
                    Order_Item.objects.create(order=order, product=product, quantity=quantity)
                res = {
                    "code": status.HTTP_200_OK,
                    "message": "Order placed  successfully"
                }
                return Response(res, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"code": status.HTTP_400_BAD_REQUEST, "message": str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

    def get_obj(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        try:
            order_instance = self.get_obj(pk)
            serializer = OrderSerializer(order_instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                res = {
                    "message": "Order updated successfully",
                    "status_code": status.HTTP_200_OK,
                    "data": serializer.data
                }
                return Response(res, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"code": status.HTTP_400_BAD_REQUEST, "message": str(e)},
                            status=status.HTTP_400_BAD_REQUEST)


# oder list by product name
class OrderListByProducts(APIView):
    def get(self, request):
        try:
            product_names = request.GET.get('products', '').split(',')
            orders = Order.objects.filter(order_item__product__name__in=product_names).distinct()
            serializer = OrderSerializer(orders, many=True)
            res = {
                "message": "Orders filtered by products",
                "status_code": status.HTTP_200_OK,
                "data": serializer.data
            }
            return Response(res, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"code": status.HTTP_400_BAD_REQUEST, "message": str(e)},
                            status=status.HTTP_400_BAD_REQUEST)


# oder list by customer name
class OrderListByCustomer(APIView):
    def get(self, request):
        try:
            customer_name = request.GET.get('customer', '')
            orders = Order.objects.filter(customer__name=customer_name)
            serializer = OrderSerializer(orders, many=True)
            res = {
                "message": f"Orders filtered by customer '{customer_name}'",
                "status_code": status.HTTP_200_OK,
                "data": serializer.data
            }
            return Response(res, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"code": status.HTTP_400_BAD_REQUEST, "message": str(e)},
                            status=status.HTTP_400_BAD_REQUEST)
