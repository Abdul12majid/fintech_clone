from rest_framework import serializers
from .models import Profile
from rest_framework.validators import ValidationError
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
    receiver = serializers.UUIDField()

    class Meta:
        model = Transaction
        fields = ('id', 'receiver', 'amount', 'description')

    def validate(self, attrs):
        check_receiver = Wallet.objects.filter(id=attrs['receiver']).exists()
        if not check_receiver:
            raise ValidationError("invalid wallet")
        return check_receiver


class ShowTransaction(serializers.ModelSerializer):
    wallet = serializers.CharField(source='wallet.user.username')
    class Meta:
        model = Transaction
        fields = ('id', 'wallet', 'receiver', 'amount', 'description', 'created_at',)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=500)
    password = serializers.CharField(max_length=500, write_only=True)
    

class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=50)
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(min_length=8, write_only=True, max_length=50)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        check_username = User.objects.filter(username=attrs['username']).exists()
        check_email = User.objects.filter(email=attrs['email']).exists()
        if check_username:
            raise ValidationError("username taken, pick another")
        elif check_email:
            raise ValidationError('email exists, pick another')
        return super().validate(attrs)


    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user