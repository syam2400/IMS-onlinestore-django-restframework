from django.shortcuts import render
from stocks.models import *
from stocks.serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError, DatabaseError
import logging

logger = logging.getLogger(__name__)

class Product_createView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = Product_Serilizer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                logger.info("Product created successfully.")
                return Response({"status":"1","message":"Product added successfully","data":serializer.data}, status=status.HTTP_201_CREATED)
            
            except IntegrityError as e:
                logger.error(f"Database integrity error: {e}")
                return Response({'error': 'Database integrity error.'}, status=status.HTTP_400_BAD_REQUEST)
           
            except DatabaseError as e:
                logger.error(f"Database error: {e}")
                return Response({'error': 'Database error.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        logger.warning("Invalid product data.")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Product_listView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            products = Products.objects.prefetch_related('variants__subvariants').all()
            paginator = PageNumberPagination()
            paginator.page_size = 3
            result_page = paginator.paginate_queryset(products, request)
            
            serializer = Product_Serilizer(result_page, many=True)
            logger.info("Product list retrieved successfully.")
            return paginator.get_paginated_response(serializer.data)
       
        except DatabaseError as e:
            logger.error(f"Database error: {e}")
            return Response({'error': 'Database error.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class Add_stock_view(APIView):
    def post(self, request, *args, **kwargs):
        add_serializer = StockUpdateSerializer(data=request.data)
        if add_serializer.is_valid():
            try:
                Product_obj = get_object_or_404(Products, ProductName=add_serializer.validated_data.get('product_name'),
                                                ProductCode=add_serializer.validated_data.get('ProductCode'))
                try:
                    variant_type = Variant.objects.get(variant_name=add_serializer.validated_data.get('variant_typ'), product=Product_obj)
                    try:
                        subvariant_obj = SubVariant.objects.filter(option=add_serializer.validated_data.get('option'))
                        print(subvariant_obj)

                        for variants in subvariant_obj:
                            varaiant_obj = Variant.objects.get(variant_name=variants.variant.variant_name, product=Product_obj)

                        varaiant_obj.product.TotalStock += add_serializer.validated_data.get('quantity')
                        varaiant_obj.product.save()
                        logger.info("Stock added/updated successfully.")
                        return Response({'status': '1', 'message': 'Product added/updated successfully.'}, status=status.HTTP_202_ACCEPTED)
                  
                    except Exception as e:
                        logger.error(f"Error adding subvariant: {e}")
                        SubVariant.objects.create(variant=variant_type, option=add_serializer.validated_data.get('option'))
                        print(variant_type.product.TotalStock, add_serializer.validated_data.get('quantity'))
                        
                        variant_type.product.TotalStock = add_serializer.validated_data.get('quantity')
                        variant_type.product.save()
                        
                        logger.info("New subvariant successfully created.")
                        return Response({'status': '1', 'message': 'New subvariant successfully created.'}, status=status.HTTP_201_CREATED)    
                except Exception as e:

                    logger.error(f"Error adding variant: {e}")
                    varaiant_obj = Variant.objects.create(variant_name=add_serializer.validated_data.get('variant_typ'), product=Product_obj)
                    subvariant_obj = SubVariant.objects.create(option=add_serializer.validated_data.get('option'), variant=varaiant_obj)
                    
                    varaiant_obj.product.TotalStock = add_serializer.validated_data.get('quantity')
                    varaiant_obj.product.save()
                    logger.info("New Product variant added successfully.")
                    return Response({'status': '1', 'message': 'New Product variant added successfully.'}, status=status.HTTP_201_CREATED)

            except IntegrityError as e:
                logger.error(f"Database integrity error: {e}")
                return Response({'error': 'Database integrity error.'}, status=status.HTTP_400_BAD_REQUEST)
            except DatabaseError as e:
                logger.error(f"Database error: {e}")
                return Response({'error': 'Database error.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        logger.warning("Invalid stock data.")
        return Response(add_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Remove_stock_view(APIView):
    def delete(self, request, *args, **kwargs):
        serializer = StockUpdateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                Product_obj = get_object_or_404(Products, ProductName=serializer.validated_data.get('product_name'),
                                                ProductCode=serializer.validated_data.get('ProductCode'))

                subvariant_obj = SubVariant.objects.filter(option=serializer.validated_data.get('option'))
                print(subvariant_obj)
                for variants in subvariant_obj:
                    varaiant_obj = Variant.objects.get(variant_name=variants.variant.variant_name, product=Product_obj)
                if varaiant_obj:
                    varaiant_obj.product.delete()
                    varaiant_obj.delete()

                    logger.info("Stock removed successfully.")
                    return Response({'status': '1', 'message': 'removed'}, status=status.HTTP_301_MOVED_PERMANENTLY)
                else:
                    logger.warning("Variant not found for removal.")
                    return Response({'status': '0', 'message': 'error'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

            except IntegrityError as e:
                logger.error(f"Database integrity error: {e}")
                return Response({'error': 'Database integrity error.'}, status=status.HTTP_400_BAD_REQUEST)
            except DatabaseError as e:
                logger.error(f"Database error: {e}")
                return Response({'error': 'Database error.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        logger.warning("Invalid stock data for removal.")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
