from uuid import UUID
from django.test import TestCase
from your_app.models import Wallet, WalletType, Transaction  # Adjust the import path

class TestModel(TestCase):
    def setUp(self):
        # Create Wallet and WalletType instances needed for the test
        self.w_id = UUID("5d71bcc8-db89-4dee-ad29-1b7eba9ab2a9")
        self.r_id = UUID("98d7f6ed-1544-442d-beb2-09f4f7a7b1cd")
        
        # Create the sender wallet
        self.wallet = Wallet.objects.create(id=self.w_id, balance=1000)  # Add any required fields here
        
        # Create the receiver wallet
        self.receiver = Wallet.objects.create(id=self.r_id, balance=500)  # Add any required fields here
        
        # Create the wallet type
        self.type_spending = WalletType.objects.create(id=1, name="Spending")  # Add any required fields here

    def test_model_transaction(self):
        amount = 300

        # Create the transaction
        transc_item = Transaction.objects.create(
            wallet=self.wallet,
            wallet_type=self.type_spending,
            receiver=self.receiver,
            amount=amount
        )

        # Verify that the transaction was created successfully
        self.assertTrue(isinstance(transc_item, Transaction))
