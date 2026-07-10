from django.contrib import admin
from .models import Category, Status, Subcategory, Transaction, TransactionType


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


@admin.register(TransactionType)
class TransactionTypeAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "transaction_type"]
    list_filter = ["transaction_type"]
    search_fields = ["name"]


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "category"]
    list_filter = ["category"]
    search_fields = ["name"]


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        "date",
        "status",
        "transaction_type",
        "category",
        "subcategory",
        "amount",
        "comment",
    ]

    list_filter = [
        "date",
        "status",
        "transaction_type",
        "category",
        "subcategory",
    ]

    search_fields = [
        "comment",
        "category__name",
        "subcategory__name",
    ]

    ordering = ["-date"]