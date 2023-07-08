from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from rest_framework import serializers
from rest_framework import status

@api_view(['GET'])
def ApiView(request):
    json = {
        'category': 'Electronics',
        'subcatgeory': 'Mobile',
        'name': 'Realme',
        'amount': '10,000',
    }
  
    return Response(json)

@api_view(['POST'])
def ApiAdd(request):
    
    response={}
    if 'amount' not in request.data or request.data['amount'] == "" or request.data['amount'] is None:
        response['message']= "invalid amount field"
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
        print(request.data)


    product=ProductSerializer(data=request.data)
    if Product.objects.filter(**request.data).exists():
        raise serializers.ValidationError("This data already exists")
    if product.is_valid():
        product.save()
        return Response(product.data,status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
        


# @api_view(['GET'])
# def ApiAll(request):
#     if request.query_params:
#         product=Product.objects.filter(**request.query_param.dict())
#     else:
#         product=Product.objects.all()
    


#     if product:
#         data=ProductSerializer(product,many=True)
#         return Response(data.data)
#     else:
#         return Response(status=status.HTTP_404_NOT_FOUND)



@api_view(['PUT'])
def Apiupdate(request,pk):
    try:
        # product=Product.objects.get(pk=pk)
        product_obj=Product.objects.get(pk=pk)
        data=ProductSerializer(instance=product_obj,data=request.data)

        if data.is_valid():
            data.save()
            return Response(data.data,status=status.HTTP_200_OK)
        else:
            response={}
            response['message']= "please choose different http method i.e., patch and add partial=True"
            return Response(response,status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(e)
        return Response({'status':403,'message':'invalid id'})



        


@api_view(['DELETE'])
def ApiDelete(request,pk):
    product=Product.objects.get(pk=pk)
    if product:
        product.delete()
        return Response(status=status.HTTP_202_ACCEPTED)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def ApiAll(request):
    response={}
     
    if request.data == {}:
        product =Product.objects.all()
        data1 = ProductSerializer(product, many=True)
        response['message']='Request GET Succesfully'
        return Response(data1.data)

        
    else:
        product =Product.objects.all()
        if request.data['subcatgeory'] !="":
            product = Product.filter(subcatgeory = request.data['subcatgeory'])  
        elif request.data['category'] !="":
            product = product.filter(category=request.data['category'])
        if product:
            data1 = ProductSerializer(product, many=True)
            response['message']='Request GET Succesfully'
            return Response(data1.data)
        else:
            response['message']='No Item Found'
            return Response(response,status=status.HTTP_404_NOT_FOUND)

