from django.db import models

# Create your models here.
from django.db import models

class Login(models.Model):
    login_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    usertype = models.CharField(max_length=255)
    # usertype: 'admin', 'user', 'hks', 'it_officer'

class Ward(models.Model):
    ward_id     = models.AutoField(primary_key=True)
    ward_number = models.CharField(max_length=255)

class User(models.Model):
    user_id             = models.AutoField(primary_key=True)
    login_id            = models.ForeignKey(Login, on_delete=models.CASCADE)
    ward_id             = models.ForeignKey(Ward, on_delete=models.CASCADE, null=True, blank=True)
    building_owner_name = models.CharField(max_length=255)
    building_number     = models.CharField(max_length=255)
    housename           = models.CharField(max_length=255)
    place               = models.CharField(max_length=255)
    phone               = models.CharField(max_length=255)
    email               = models.CharField(max_length=255)

class HKS(models.Model):
    TYPE_CHOICES = [
        ('normal', 'Normal'),
        ('custom', 'Custom'),
        ('delivery', 'Delivery')
    ]
    hks_id   = models.AutoField(primary_key=True)
    login_id = models.ForeignKey(Login, on_delete=models.CASCADE)
    name     = models.CharField(max_length=255)
    place    = models.CharField(max_length=255)
    phone    = models.CharField(max_length=255)
    email    = models.CharField(max_length=255)
    type     = models.CharField(max_length=50, choices=TYPE_CHOICES)
    # type: 'normal'(A), 'custom'(B), 'delivery'(C)

class IT_Officer(models.Model):
    officer_id = models.AutoField(primary_key=True)
    login_id   = models.ForeignKey(Login, on_delete=models.CASCADE)
    name       = models.CharField(max_length=255)
    phone      = models.CharField(max_length=255)
    email      = models.CharField(max_length=255)

class Assign_Ward(models.Model):
    assign_id = models.AutoField(primary_key=True)
    hks_id    = models.ForeignKey(HKS, on_delete=models.CASCADE)
    ward_id   = models.ForeignKey(Ward, on_delete=models.CASCADE)

class Complaints(models.Model):
    complaints_id = models.AutoField(primary_key=True)
    sender_id     = models.ForeignKey(Login, on_delete=models.CASCADE, related_name='sent_complaints')
    receiver_id   = models.ForeignKey(Login, on_delete=models.CASCADE, related_name='received_complaints')
    description   = models.TextField()
    reply         = models.TextField(null=True, blank=True)
    date          = models.CharField(max_length=255)

class My_Waste(models.Model):
    my_waste_id = models.AutoField(primary_key=True)
    user_id     = models.ForeignKey(User, on_delete=models.CASCADE)
    date        = models.CharField(max_length=255)
    status      = models.CharField(max_length=255, default='pending')
    # status: 'pending', 'verified', 'collected'

class Products(models.Model):
    products_id  = models.AutoField(primary_key=True)
    product_type = models.CharField(max_length=255)
    product_name = models.CharField(max_length=255)
    description  = models.TextField()
    image        = models.FileField(upload_to='products/')
    stock        = models.CharField(max_length=255)
    amount       = models.CharField(max_length=255)
    # product_type: 'bio', 'plastic'

class Order_Master(models.Model):
    om_id        = models.AutoField(primary_key=True)
    user_id      = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.CharField(max_length=255)
    date         = models.CharField(max_length=255)
    status       = models.CharField(max_length=255, default='pending')
    # status: 'pending', 'delivered', 'cancelled'

class Order_Child(models.Model):
    oc_id      = models.AutoField(primary_key=True)
    om_id      = models.ForeignKey(Order_Master, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity   = models.CharField(max_length=255)
    amount     = models.CharField(max_length=255)

class OD_Payment(models.Model):
    od_payment_id = models.AutoField(primary_key=True)
    om_id         = models.ForeignKey(Order_Master, on_delete=models.CASCADE)
    amount        = models.CharField(max_length=255)
    date          = models.CharField(max_length=255)
    status        = models.CharField(max_length=255, default='pending')
    # status: 'pending', 'paid'

class IT_Notification(models.Model):
    it_notification_id = models.AutoField(primary_key=True)
    title              = models.CharField(max_length=255)
    description        = models.TextField()
    date               = models.CharField(max_length=255)

class HKS_Notification(models.Model):
    hks_notification_id = models.AutoField(primary_key=True)
    hks_id              = models.ForeignKey(HKS, on_delete=models.CASCADE)
    title               = models.CharField(max_length=255)
    description         = models.TextField()
    date                = models.CharField(max_length=255)

class Custom_Waste_Request(models.Model):
    custom_waste_request_id = models.AutoField(primary_key=True)
    user_id                 = models.ForeignKey(User, on_delete=models.CASCADE)
    date                    = models.CharField(max_length=255)
    total_amount            = models.CharField(max_length=255)
    status                  = models.CharField(max_length=255, default='pending')
    # status: 'pending', 'approved', 'completed'

class Custom_Waste_Status(models.Model):
    custom_waste_status_id  = models.AutoField(primary_key=True)
    custom_waste_request_id = models.ForeignKey(Custom_Waste_Request, on_delete=models.CASCADE)
    plastic_quantity        = models.CharField(max_length=255)
    plastic_amount          = models.CharField(max_length=255)
    bio_quantity            = models.CharField(max_length=255)
    bio_amount              = models.CharField(max_length=255)

class Cust_Payment(models.Model):
    cust_payment_id         = models.AutoField(primary_key=True)
    custom_waste_request_id = models.ForeignKey(Custom_Waste_Request, on_delete=models.CASCADE)
    amount                  = models.CharField(max_length=255)
    date                    = models.CharField(max_length=255)
    status                  = models.CharField(max_length=255, default='pending')
    # status: 'pending', 'paid'

class Public_Waste(models.Model):
    public_waste_id = models.AutoField(primary_key=True)
    user_id         = models.ForeignKey(User, on_delete=models.CASCADE)
    title           = models.CharField(max_length=255)

    image           = models.FileField(upload_to='public_waste/')
    status          = models.CharField(max_length=255, default='pending')
    # status: 'pending', 'verified', 'cleaned'

class Rewards(models.Model):
    rewards_id      = models.AutoField(primary_key=True)
    public_waste_id = models.ForeignKey(Public_Waste, on_delete=models.CASCADE)
    rewards         = models.CharField(max_length=255)
    date            = models.CharField(max_length=255)