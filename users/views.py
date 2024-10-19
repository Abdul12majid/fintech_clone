from django.shortcuts import render, HttpResponse
from .models import Profile
from fintech_app.models import Wallet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import AccountSerializer, ProfileSerializer


# Create your views here.
@api_view(['GET'])
def index(request):
	user = request.user
	user_profile = Profile.objects.get(user=user)
	serializer = ProfileSerializer(user_profile, many=False)
	return Response({'info':serializer.data})




	