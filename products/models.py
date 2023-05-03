from django.db import models

class CategoryOptions(models.TextChoices):
    ELETRONICS = "Eletronics",
    CLOTHING = "Clothing",
    SHOES = "Shoes",
    TOYS = "Toys",
    SPORTS = "Sports",
    HEALTH = "Health",
    SCHOOL = "School",
    BOOKS = "Books",
    CRAFTS = "Crafts",
    HOME = "Home",
    BEAUTY = "Beauty",
    GARDEN = "Garden",
    GROCERY = "Grocery",
    OTHERS = "Others"

class Product(models.Model):
    class Meta:
        ordering = ['id']
    
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, default=None)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_stock = models.IntegerField()
    is_available_for_sale = models.BooleanField(default=False)
    brand = models.CharField(max_length=50, null=True)
    category = models.CharField(max_length=50, choices = CategoryOptions.choices, default= CategoryOptions.OTHERS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    seller = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="products")

    
