from django.db import models
import uuid
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here

class WalletType(models.Model):
    type = models.CharField(max_length=50)
    users=models.ManyToManyField(User)

    def __str__(self):
    	return self.type

def get_default_wallet():
    try:
        return WalletType.objects.get(type="Bonus")
    except WalletType.DoesNotExist:
        return None

class Wallet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wallet_type = models.ForeignKey(WalletType, on_delete=models.CASCADE, default=get_default_wallet)
    total_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    pin = models.CharField(max_length=20, default="0000")

    def __str__(self):
    	return f'{self.user.username} - {self.wallet_type.type} wallet'


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    wallet_type = models.ForeignKey(WalletType, on_delete=models.CASCADE)
    receiver = models.ForeignKey(Wallet, related_name='sender', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.wallet.user.username} to {self.receiver.user.username}'

