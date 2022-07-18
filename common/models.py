import datetime

from django.db import models


# Create your models here
class Client(models.Model):
    name = models.CharField(max_length=200)
    phoneNumber = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    # qq
    qq = models.CharField(max_length=30, null=True, blank=True)


# medicine
class Medicine(models.Model):
    name = models.CharField(max_length=200)
    sn = models.CharField(max_length=200)
    des = models.CharField(max_length=200)


# order
class Order(models.Model):
    name = models.CharField(max_length=200)
    create_date = models.DateTimeField(default=datetime.datetime.now)
    # 客户为外键
    customer = models.ForeignKey(Client, on_delete=models.PROTECT)
    # 订单中的药品
    medicine = models.ManyToManyField(Medicine, through='OrderMedicine')


class OrderMedicine(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT)
    amount = models.PositiveIntegerField()


# country
class Country(models.Model):
    name = models.CharField(max_length=100)


# student
class Student(models.Model):
    name = models.CharField(max_length=100)
    grade = models.PositiveIntegerField()
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
