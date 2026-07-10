from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from smart_selects.db_fields import ChainedForeignKey


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
    date = models.DateField(default=timezone.localdate)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    transaction_type = models.ForeignKey(
        TransactionType,
        on_delete=models.PROTECT
    )
    category = ChainedForeignKey(
        Category,
        on_delete=models.PROTECT,
        chained_field="transaction_type",
        chained_model_field="type",
        show_all=False,
        auto_choose=True,
        sort=True,
    )
    subcategory = ChainedForeignKey(
        Subcategory,
        on_delete=models.PROTECT,
        chained_field="category",
        chained_model_field="category",
        show_all=False,
        auto_choose=True,
        sort=True,
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"{self.date} - {self.amount}"

    def clean(self):
        errors = {}

        if (
            self.category_id
            and self.transaction_type_id
            and self.category.type_id != self.transaction_type_id
        ):
            errors["category"] = (
                f'Категория "{self.category}" не относится к типу "{self.transaction_type}".'
            )

        if (
            self.subcategory_id
            and self.category_id
            and self.subcategory.category_id != self.category_id
        ):
            errors["subcategory"] = (
                f'Подкатегория "{self.subcategory}" не относится к категории "{self.category}".'
            )

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)