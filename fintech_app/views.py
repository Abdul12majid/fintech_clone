from django.shortcuts import render, HttpResponse
from .models import Wallet, Transaction, WalletType
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import ShowTransaction
from rest_framework.generics import ListCreateAPIView

# Create your views here.
def index(request):
	return HttpResponse("Holla")


class transactions(ListCreateAPIView):
	queryset = Transaction.objects.all()
	serializer_class = ShowTransaction
