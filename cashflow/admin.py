from django.contrib import admin
from .models import Status, Transaction, TransactionType, Category, Subcategory




admin.site.register(Status)
admin.site.register(TransactionType)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Transaction)