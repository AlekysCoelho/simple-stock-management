import re
from unicodedata import category
from venv import create

from django.db import models
from django.utils.translation import gettext_lazy as _


class ProductManager(models.Manager):
    def get_low_stock_products(self, threshold):
        """
        Returns products with stock below the limit.
        """
        return self.filter(stock__lt=threshold)

    def create_with_discount(self, name, description, category, price, stock, discount):
        """
        Create a new product with discount.
        """

        if price <= 0:
            raise ValueError("Price must be greater than zero.")
        if stock < 0:
            raise ValueError("Stock must be greater than or equal to zero.")
        if discount < 0:
            raise ValueError("Discount must be greater than or equal to zero.")
        price_with_discount = price - (price * discount / 100)
        return self.create(
            name=name,
            description=description,
            category=category,
            price=price,
            stock=stock,
            discount=discount,
            final_price=price_with_discount,
        )


class Product(models.Model):
    name = models.CharField(_("Product Name"), max_length=200)
    description = models.TextField(_("Product Description"))
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, related_name="products"
    )
    price = models.DecimalField(("Price Product"), max_digits=10, decimal_places=2)
    final_price = models.DecimalField(
        _("Final Price Product"), max_digits=10, decimal_places=2, blank=True, null=True
    )
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
