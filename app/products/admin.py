from django.contrib import admin

from app.products.models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    list_per_page = 10


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "stock", "discount", "final_price")
    search_fields = ("name", "category__name")
    list_filter = ("category",)
    list_editable = ("price", "stock", "discount")
    list_per_page = 10
    actions = ["apply_discount"]

    def apply_discount(self, request, queryset):
        """Action to apply a discount to selected products."""
        queryset.update(discount=10)
        for product in queryset:
            product.save()
        self.message_user(request, "Discount applied successfully.")
