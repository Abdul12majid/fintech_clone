from django.db import models
import uuid
from django.contrib.auth.models import User

# Create your models here.


class WalletType(models.Model):
    type = models.CharField(max_length=50)

    def __str__(self):
    	return self.type

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wallet_type = models.ForeignKey(WalletType, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
    	return f'{self.user.username} wallet'


class Transaction(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
	amount = models.DecimalField(max_digits=10, decimal_places=2)
	description = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.wallet.user.username
