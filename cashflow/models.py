from django.db import models
from datetime import date

class Status(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class TransactionType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    type = models.ForeignKey(TransactionType, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    date = models.DateField(default=date.today)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    transaction_type = models.ForeignKey(
        TransactionType,
        on_delete=models.PROTECT
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT
    )
    subcategory = models.ForeignKey(
        Subcategory,
        on_delete=models.PROTECT
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"{self.date} - {self.amount}"