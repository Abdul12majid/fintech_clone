from django.shortcuts import render, HttpResponse
from .models import Wallet, Transaction, WalletType
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import ShowTransaction

# Create your views here.
def index(request):
	return HttpResponse("Holla")


@api_view(['GET'])
def transactions(request):
	get_trans = Transaction.objects.all()
	show_trans = ShowTransaction(get_trans, many=True)
	return Response({'info':show_trans.data})