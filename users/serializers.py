from rest_framework import serializers
from .models import Profile
from fintech_app.models import Wallet

class ProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = Profile
		fields = ('user', 'wallet', 'phone_no', 'profile_bio')


class AccountSerializer(serializers.ModelSerializer):
	class Meta:
		model = Wallet
		fields = ('user', 'total_balance')