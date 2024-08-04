from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver
import random

class UsersTable(models.Model):
    FARMER = 'farmer'
    SUPPLIER = 'supplier'
    STOCKKEEPER = 'stockkeeper'
    ADMIN = 'admin'

    ROLE_CHOICES = [
        (FARMER, 'Farmer'),
        (SUPPLIER, 'Supplier'),
        (STOCKKEEPER, 'Stockkeeper'),
        (ADMIN, 'admin'),
    ]

    user_name = models.CharField(max_length=100, unique=True)
    pass_word = models.CharField(max_length=100)
    user_email = models.EmailField()
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=FARMER)
    user_id = models.IntegerField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.user_name

    def generate_unique_user_id(self):
        while True:
            new_id = random.randint(10000, 99999)
            if not UsersTable.objects.filter(user_id=new_id).exists():
                return new_id

@receiver(pre_save, sender=UsersTable)
def ensure_unique_user_id(sender, instance, **kwargs):
    if not instance.user_id:
        instance.user_id = instance.generate_unique_user_id()

class Inventory(models.Model):
    farmer = models.ForeignKey(UsersTable, on_delete=models.CASCADE, related_name='farmer_inventories')
    product_type = models.CharField(max_length=100)
    sent_quantity = models.DecimalField(max_digits=10, decimal_places=2)
    supplier = models.ForeignKey(UsersTable, on_delete=models.CASCADE, related_name='supplier_inventories')
    storekeeper = models.ForeignKey(UsersTable, on_delete=models.CASCADE, related_name='storekeeper_inventories', null=True, blank=True)
    storekeeper_name = models.CharField(max_length=100, null=True, blank=True)
    received_quantity = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    received_date_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.product_type} by {self.farmer.user_name}"
    

# grain_harverst_app/models.py

class ChatMessage(models.Model):
    sender = models.ForeignKey(UsersTable, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(UsersTable, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()

    def __str__(self):
        return self.name


   

