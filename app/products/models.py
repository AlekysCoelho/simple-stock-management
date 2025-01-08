from decimal import Decimal
from math import e

from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _


class ProductManager(models.Manager):
    def get_low_stock_products(self, threshold: int = 10) -> QuerySet:
        """
        Returns products with stock below the limit.
        """

        cache_key = f"low_stock_products_{threshold}"
        products = cache.get(cache_key)
        if products is None:
            products = self.filter(stock__lt=threshold)
            cache.set(cache_key, products, timeout=60 * 5)
        return products

    def create_with_discount(
        self,
        name: str,
        description: str,
        category: "Category",
        price: Decimal,
        stock: int,
        discount: Decimal,
    ):
        """
        Create a new product with discount.
        """

        if price <= 0:
            raise ValidationError("Price must be greater than zero.")
        if stock < 0:
            raise ValidationError("Stock must be greater than or equal to zero.")
        if discount < 0:
            raise ValidationError("Discount must be greater than or equal to zero.")
        if discount > 100:
            raise ValidationError("Discount must be less than or equal to 100.")

        final_price = price - (price * discount / 100)

        products = self.create(
            name=name,
            description=description,
            category=category,
            price=price,
            stock=stock,
            discount=discount,
            final_price=final_price,
        )

        cache_keys = [f"category_products_{category.id}", "low_stock_products"]
        cache.delete_many(cache_keys)

        return products


class Product(models.Model):
    name = models.CharField(_("Product Name"), max_length=200, db_index=True)
    description = models.TextField(_("Product Description"))
    category = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        related_name="products",
        db_index=True,
    )
    price = models.DecimalField(
        ("Price Product"),
        validators=[
            MinValueValidator(
                Decimal("0.01"), message="Price must be greater than zero."
            )
        ],
        max_digits=10,
        decimal_places=2,
    )
    final_price = models.DecimalField(
        _("Final Price Product"), max_digits=10, decimal_places=2, blank=True, null=True
    )
    stock = models.IntegerField(
        _("Quantity of Product in Stock"),
        validators=[
            MinValueValidator(0, message="Stock must be greater than or equal to zero.")
        ],
    )
    discount = models.DecimalField(
        _("Discount Product"),
        validators=[
            MinValueValidator(
                0, message="Discount must be greater than or equal to zero."
            )
        ],
        max_digits=5,
        decimal_places=2,
        default=0.00,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ProductManager()

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["name", "category"]),
        ]

    def clean(self):
        """Validates product data before saving."""

        if self.price <= 0:
            raise ValidationError({"Price": "Price must be greater than zero."})
        if self.stock < 0:
            raise ValidationError(
                {"Stock": "Stock must be greater than or equal to zero."}
            )
        if self.discount < 0:
            raise ValidationError(
                {"Discount": "Discount must be greater than or equal to zero."}
            )
        if self.discount > 100:
            raise ValidationError(
                {"Discount": "Discount must be less than or equal to 100."}
            )

        self._calculate_final_price()

    def _calculate_final_price(self) -> None:
        """Calculate the final price based on discount."""
        if self.discount > 0:
            self.final_price = self.price * (
                Decimal("1") - (self.discount / Decimal("100"))
            )
        else:
            self.final_price = self.price

    def __str__(self) -> str:
        return f"{self.name} - {self.category.name}"

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def is_in_stock(self, quantity: int = 1) -> bool:
        """Check is there is enough stock for the given quantity."""
        return self.stock >= quantity

    def adjust_price(self, percentage: Decimal) -> None:
        """Adjust the product price by a percentage."""
        if percentage == 0:
            return
        price_adjustment = self.price * (percentage / Decimal("100"))
        self.final_price += price_adjustment
        self._calculate_final_price()
        self.save()


class Category(models.Model):
    name = models.CharField(_("Category Name"), max_length=255)
    description = models.TextField(_("Category Description"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name}"

    def get_products_count(self) -> int:
        """Return the number of products in the category."""
        return self.products.count()
