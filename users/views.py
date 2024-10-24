from django.shortcuts import render, HttpResponse
from .models import Profile
from fintech_app.models import Wallet, Transaction, WalletType
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import AccountSerializer, ProfileSerializer, TransactionSerializer, ShowTransaction


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
	type_spending = WalletType.objects.get(id=1)
	user_profile = request.user.profile
	serializer = TransactionSerializer(data=request.data)
	#print(get_user.user.username)
	if serializer.is_valid():
		receiver_id = request.data['receiver']
		amount = request.data['amount']
		description = request.data.get('description', '')
		get_sender_wallet = Wallet.objects.get(user=request.user, wallet_type=type_spending)
		sender_wallet_type = get_sender_wallet.wallet_type
		get_receiver_id = Wallet.objects.filter(id=receiver_id).exists()
		if get_receiver_id:
			get_id = Wallet.objects.get(id=receiver_id)
			if get_id.wallet_type.type != "Bonus":
				Transaction.objects.create(
					wallet_type=sender_wallet_type,
					wallet=get_sender_wallet,
					receiver=get_id,
					amount=amount,
					description=description)
				get_last = Transaction.objects.filter(wallet=get_sender_wallet).last()
				show_trans = ShowTransaction(get_last, many=False)
				return Response({'info':show_trans.data})
			else:
				return Response({'info':"can't send to a bonus account"})
		else:
			return Response({'info':'account does not exist'})
	return Response({'info':serializer.errors})


@api_view(['POST', "GET"])
def login_user(request):
	serializer = LoginSerializer(data=request.data)
	if serializer.is_valid():
		username = request.data['username']
		password = request.data['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return Response({'Info': 'Login Successful'})
		else:
			return Response({'Info': 'Incorrect username or password'})

	return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

