from rest_framework import serializers
from rest_framework.validators import ValidationError
from .models import Transaction



class ShowTransaction(serializers.ModelSerializer):
    wallet = serializers.CharField(source='wallet.user.username')
    class Meta:
        model = Transaction
        fields = ('id', 'wallet', 'receiver', 'amount', 'description', 'created_at',)