import re
from unicodedata import category
from venv import create

from django.db import models
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    name = models.CharField(_("Product Name"), max_length=200)
    description = models.TextField(_("Product Description"))
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, related_name="products"
    )
    price = models.DecimalField(("Price Product"), max_digits=10, decimal_places=2)
    stock = models.IntegerField(_("Quantity of Product in Stock"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.name} - {self.category.name}"


class Category(models.Model):
    name = models.CharField(_("Category Name"), max_length=255)
    description = models.TextField(_("Category Description"))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.name}"
