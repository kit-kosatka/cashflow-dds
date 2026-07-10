from django.db import transaction
from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import (Status, TransactionType, Category, Subcategory, Transaction)

class TransactionModelTest(TestCase):
    def setUp(self):
        self.status = Status.objects.create(
            name="Бизнес"
        )
        self.expense_type = TransactionType.objects.create(
            name="Списание"
        )
        self.income_type = TransactionType.objects.create(
            name="Пополнение"
        )
        self.category = Category.objects.create(
            name="Маркетинг",
            transaction_type=self.expense_type
        )
        self.subcategory = Subcategory.objects.create(
            name="Avito",
            category=self.category
        )

    def test_create_valid_transaction(self):
        transaction = Transaction(
            status=self.status,
            transaction_type=self.expense_type,
            category=self.category,
            subcategory=self.subcategory,
            amount=1000,
            comment="Реклама",
        )

        transaction.full_clean()
        transaction.save()

        self.assertEqual(Transaction.objects.count(), 1)

    def test_invalid_category_for_transaction_type(self):
        transaction = Transaction(
            status=self.status,
            transaction_type=self.income_type,
            category=self.category,
            subcategory=self.subcategory,
            amount=1000,
            comment="Некорректная запись",
        )

        with self.assertRaises(ValidationError):
            transaction.full_clean()

    def test_invalid_subcategory_for_category(self):
        second_category = Category.objects.create(
            name="Инфраструктура",
            transaction_type=self.expense_type,
        )

        second_subcategory = Subcategory.objects.create(
            name="VPS",
            category=second_category,
        )

        transaction = Transaction(
            status=self.status,
            transaction_type=self.expense_type,
            category=self.category,
            subcategory=second_subcategory,
            amount=1000,
            comment="Некорректная запись",
        )

        with self.assertRaises(ValidationError):
            transaction.full_clean()