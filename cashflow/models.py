from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from smart_selects.db_fields import ChainedForeignKey


class Status(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"
        ordering = ["name"]


class TransactionType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип операции"
        verbose_name_plural = "Типы операций"
        ordering = ["name"]


class Category(models.Model):
    name = models.CharField(max_length=100)
    transaction_type = models.ForeignKey(
        TransactionType,
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]


class Subcategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"
        ordering = ["name"]


class Transaction(models.Model):
    date = models.DateField(default=timezone.localdate)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    transaction_type = models.ForeignKey(TransactionType, on_delete=models.PROTECT)
    category = ChainedForeignKey(
        Category,
        on_delete=models.PROTECT,
        chained_field="transaction_type",
        chained_model_field="transaction_type",
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
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"{self.date} - {self.amount}"

    class Meta:
        verbose_name = "Операция"
        verbose_name_plural = "Операции"
        ordering = ["-date"]

    def clean(self):
        errors = {}

        if (
            self.category_id
            and self.transaction_type_id
            and self.category.transaction_type_id != self.transaction_type_id
        ):
            errors["category"] = (
                f'Категория "{self.category}" '
                f'не относится к типу "{self.transaction_type}".'
            )

        if (
            self.subcategory_id
            and self.category_id
            and self.subcategory.category_id != self.category_id
        ):
            errors["subcategory"] = (
                f'Подкатегория "{self.subcategory}" '
                f'не относится к категории "{self.category}".'
            )

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
