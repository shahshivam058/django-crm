from django.db import models

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=70,null=True)
    phone = models.CharField(max_length=10,null=True)
    email = models.CharField(max_length=100,null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class Tag(models.Model):
    name = models.CharField(max_length=70)

    def __str__(self):
        return self.name

class Product(models.Model):
    CATEGORY = (
        ('Indoor','Indoor'),
        ('Outdoor','Outdoor'),
    )
    name = models.CharField(max_length=70,null=True)
    price = models.IntegerField()
    category = models.CharField(max_length=100,choices=CATEGORY)
    description = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS = (
        ('Pending','Pending'),
        ('Out of Delivery','Out of Delivery'),
        ('Deliverd','Deliverd'),
    )

    customer = models.ForeignKey(Customer,null=True,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,null=True,on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20,choices=STATUS)
    note = models.CharField(max_length=1000,null=True)

    def __str__(self):
        return self.status
    
"""
queryset = Customer.objects.all()

queryset = veriable that stores the data
customer = model name
objects = model object attribute
all() = method to retrive data


another methods 
get()
filter()
exclude()

"""
