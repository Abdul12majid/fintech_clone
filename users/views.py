from django.shortcuts import render, HttpResponse
from .models import Profile
from fintech_app.models import Wallet, Transaction, WalletType
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import AccountSerializer, ProfileSerializer, TransactionSerializer


# Create your views here.
@api_view(['GET'])
def index(request):
	user = request.user
	user_profile = Profile.objects.get(user=user)
	serializer = ProfileSerializer(user_profile, many=False)
	return Response({'info':serializer.data})


@api_view(['GET'])
def wallets(request):
	user = request.user
	user_wallets = Wallet.objects.filter(user=user).all()
	serializer = AccountSerializer(user_wallets, many=True)
	return Response({'info':serializer.data})


@api_view(['POST', 'GET'])
def send(request):
	serializer = TransactionSerializer(data=request.data)
	if serializer.is_valid():
		get_wallet_type = request.data['wallet_type']
		wallet_type = WalletType.objects.get(id=get_wallet_type)
		user_profile = request.user.profile
		if get_wallet_type in user_profile.wallet.all():
			get_wallet = Wallet.objects.get(
				wallet_type=get_wallet_type,
				user=request.user)
			user_wallet = get_wallet.id

			receiver = request.data['receiver']
			receiver_wallet = Wallet.objects.get(id=receiver)
			amount = request.data['amount']
			description = request.data['description']
			if receiver_wallet.wallet_type != "Bonus":
				Transaction.objects.create(
					wallet_type=wallet_type,
					wallet=user_wallet,
					receiver=receiver_wallet,
					amount=amount,
					description=description)
				return Response({'info':'Transaction made'})
			else:
				return Response({'info':'cant send to a bonus account'})
		return Response({'info':'user does not have this account'})
	return Response({'info':serializer.errors})

