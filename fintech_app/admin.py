from django.contrib import admin
from .models import WalletType, Wallet, Transaction

# Register your models here.
admin.site.register(WalletType)
admin.site.register(Wallet)
admin.site.register(Transaction)