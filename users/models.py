from django.db import models
from django.contrib.auth.models import User
from fintech_app.models import Transaction, WalletType, Wallet
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    wallet=models.ManyToManyField(WalletType)
    phone_no = models.CharField(max_length=255)
    date_of_birth=models.DateTimeField(auto_now=True)
    profile_image = models.ImageField(upload_to='profile_images', null=True, blank=True)
    profile_bio=models.TextField(null=True, blank=True, max_length=500)
    transactions = models.ManyToManyField(Transaction, symmetrical=False, blank=True)

    def __str__(self):
        return self.user.username

#@receiver(post_save, sender=Account)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile=Profile(user=instance)
        user_profile.save()
        #create wallet
        user_bonus_wallet=Wallet(user=instance)
        user_bonus_wallet.save()
        #add wallet type to profile
        get_bonus_wallet = WalletType.objects.get(type='Bonus')
        user_profile.wallet.add(get_bonus_wallet)
        user_profile.save()
post_save.connect(create_profile, sender=User)