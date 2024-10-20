from rest_framework import serializers
from .models import Profile
from fintech_app.models import Wallet, WalletType, Transaction
from django.contrib.auth.models import User

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')
    wallet = serializers.SerializerMethodField()

    def get_wallet(self, instance):
        wallets = instance.wallet.all()
        wallet_data = []
        for wallet in wallets:
            wallet_data.append({
                'id': wallet.id,
                'type': wallet.type,
            })
        return wallet_data

    class Meta:
        model = Profile
        fields = ('user', 'wallet', 'phone_no', 'profile_bio')


class AccountSerializer(serializers.ModelSerializer):
    wallet_type = serializers.CharField(source='wallet_type.type')

    class Meta:
        model = Wallet
        fields = ('wallet_type', 'total_balance')


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id', 'wallet_type', 'receiver', 'amount', 'description', 'created_at')