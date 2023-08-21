from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class MaterialAttribute(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class RawMaterial(models.Model):
    name = models.CharField(max_length=255)
    attributes = models.ManyToManyField(MaterialAttribute, through='MaterialAttributeValue')

    def __str__(self):
        return self.name

class MaterialAttributeValue(models.Model):
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE)
    attribute = models.ForeignKey(MaterialAttribute, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=20, decimal_places=10)


class Recipe(models.Model):
    name = models.CharField(max_length=255)
    materials = models.ManyToManyField(RawMaterial, through='RecipeRawMaterial')

    def __str__(self):
        return self.name

class RecipeRawMaterial(models.Model):
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    max_percentage = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)], default=100, verbose_name="Max Percentage (%)")
    min_percentage = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)], default=0, verbose_name="Min Percentage (%)")
    min_weight_kg_per_ton = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(1000)], default=0, verbose_name="Min Weight (kg/ton)")
    max_weight_kg_per_ton = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(1000)], default=1000, verbose_name="Max Weight (kg/ton)")

class Receipt(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

class MaterialAttributeLimit(models.Model):
    attribute = models.ForeignKey(MaterialAttribute, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.attribute.name

class RecipeAttributeLimit(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    attribute = models.ForeignKey(MaterialAttribute, on_delete=models.CASCADE)
    min_value = models.DecimalField(max_digits=20, decimal_places=10, validators=[MinValueValidator(0)], verbose_name="Min Value", default=0.0)
    max_value = models.DecimalField(max_digits=20, decimal_places=10, validators=[MinValueValidator(0)], verbose_name="Max Value", default=999.9)

    class Meta:
        unique_together = ('recipe', 'attribute')
        verbose_name = "Recipe Attribute Limit"
        verbose_name_plural = "Recipe Attribute Limits"

    def __str__(self):
        return f"{self.recipe.name} - {self.attribute.name} (Min: {self.min_value}, Max: {self.max_value})"

