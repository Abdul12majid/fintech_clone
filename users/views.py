from django.shortcuts import render, HttpResponse
from .models import Profile
from fintech_app.models import Wallet, Transaction, WalletType
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import AccountSerializer, ProfileSerializer, TransactionSerializer, ShowTransaction
from .serializers import LoginSerializer, SignUpSerializer
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from uuid import UUID

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
	if serializer.is_valid():
		receiver_id = request.data['receiver']
		amount = request.data['amount']
		description = request.data.get('description', '')
		pin = request.data['pin']
		get_sender_wallet = Wallet.objects.get(user=request.user, wallet_type=type_spending)
		sender_wallet_type = get_sender_wallet.wallet_type
		get_receiver_id = Wallet.objects.filter(id=receiver_id).exists()
		get_sender_pin = get_sender_wallet.pin
		if get_receiver_id:
			get_id = Wallet.objects.get(id=receiver_id)
			if get_id.wallet_type.type != "Bonus":
				if pin != "0000":
					if get_sender_pin == pin:
						Transaction.objects.create(
							wallet_type=sender_wallet_type,
							wallet=get_sender_wallet,
							receiver=get_id,
							amount=amount,
							description=description)

						#remove amount from sender wallet
						get_sender_wallet.total_balance -= int(amount)
						get_sender_wallet.save()

						#add amount to receiver wallet
						get_id.total_balance += int(amount)
						get_id.save()

						#display transaction made
						get_last = Transaction.objects.filter(wallet=get_sender_wallet).order_by('-created_at').first()
						show_trans = ShowTransaction(get_last, many=False)
						return Response({'info':show_trans.data})
					else:
						return Response({'info':"Wrong pin, try again"})
				else:
					return Response({'info':"Default pin can't be used, change pin."})
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

@api_view(['POST', 'GET'])	
def register(request):
	serializer = SignUpSerializer(data=request.data)
	if serializer.is_valid():
		username = request.data['username']
		password = request.data['password']

		#create user
		serializer.save()
		get_user = User.objects.get(username=username)

		#authenticate user
		user=authenticate(username=username, password=password)
		login(request, user)

		#create spending wallet for user
		type_spending = WalletType.objects.get(id=1)
		user_profile = request.user
		Wallet.objects.create(
			user=user_profile,
			wallet_type = type_spending)

		#add wallet type to profile
		profile = user_profile.profile
		profile.wallet.add(type_spending)
		profile.save()

		#add user to wallet
		type_spending.users.add(user_profile)
		type_spending.save()

		response = {
			"info":"Registeration successful",
			"data":serializer.data
		}
		return Response(data=response, status=status.HTTP_201_CREATED)
	return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def transactions(request):
	user = request.user
	type_spending = WalletType.objects.get(id=1)
	get_user_wallet = Wallet.objects.get(user=user, wallet_type=type_spending)
	get_trans = Transaction.objects.filter(wallet=get_user_wallet).all()
	show_trans = ShowTransaction(get_trans, many=True)
	return Response({'info':show_trans.data})


@api_view(['GET'])
def transaction(request, pk):
	get_trans = Transaction.objects.get(id=pk)
	if get_trans:
		show_trans = ShowTransaction(get_trans, many=False)
		return Response({'info':show_trans.data})
	else:
		return Response({'info':"Transaction"})
	
	
