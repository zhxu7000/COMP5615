from django.contrib import admin
from .models import (
    MaterialAttribute,
    RawMaterial,
    MaterialAttributeValue,
    Recipe,
    RecipeRawMaterial,
    Receipt,
    RecipeAttributeLimit,
)

# MaterialAttribute的Admin界面
@admin.register(MaterialAttribute)
class MaterialAttributeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']

# RawMaterial的Admin界面
@admin.register(RawMaterial)
class RawMaterialAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

# MaterialAttributeValue的Admin界面
@admin.register(MaterialAttributeValue)
class MaterialAttributeValueAdmin(admin.ModelAdmin):
    list_display = ['raw_material', 'attribute', 'value']
    list_filter = ['raw_material', 'attribute']
    raw_id_fields = ['raw_material', 'attribute']  # 使用raw_id_fields显示外键字段

# Recipe的Admin界面
@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['name']

# RecipeRawMaterial的Admin界面
@admin.register(RecipeRawMaterial)
class RecipeRawMaterialAdmin(admin.ModelAdmin):
    list_display = ['raw_material', 'recipe', 'max_percentage', 'min_percentage', 'min_weight_kg_per_ton',
                    'max_weight_kg_per_ton']
    list_filter = ['raw_material', 'recipe']
    raw_id_fields = ['raw_material', 'recipe']  # 使用raw_id_fields显示外键字段

# RecipeMaterialAttributeLimit的Admin界面
@admin.register(RecipeAttributeLimit)
class RecipeMaterialAttributeLimitAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'attribute', 'min_value', 'max_value']
    list_filter = ['recipe', 'attribute']
    raw_id_fields = ['recipe', 'attribute']

# Receipt的Admin界面
@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'total_price', 'date']
