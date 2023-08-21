from django.shortcuts import render
from pulp import LpVariable, LpProblem, LpMinimize, LpStatus
from .models import RawMaterial, MaterialAttributeValue, Recipe, RecipeAttributeLimit, RecipeRawMaterial
from django.http import FileResponse
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from io import BytesIO
from .utils import get_cost_per_tonne, calculate_optimal_mix  # 假设你在utils.py中定义了这两个函数


def download_pdf_view(request):
    optimal_mix = calculate_optimal_mix()
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=landscape(letter))

    x_offset = 50
    y_offset = 600
    height = 20
    page_limit = 150

    p.drawString(x_offset, y_offset, "Materials Report")
    y_offset -= (2 * height)

    for material_name, percentage in optimal_mix.items():
        if y_offset <= page_limit:
            p.showPage()
            y_offset = 750

        p.drawString(x_offset, y_offset, f"Material Name: {material_name}")
        y_offset -= height

        cost_per_tonne_value = get_cost_per_tonne(material_name)
        p.drawString(x_offset, y_offset, f"Percentage: {percentage}")
        y_offset -= height
        p.drawString(x_offset, y_offset, f"Cost per Tonne: {cost_per_tonne_value}")
        y_offset -= (2 * height)

    p.save()
    buffer.seek(0)
    response = FileResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="materials_report.pdf"'

    return response


def optimal_mix_view(request):
    if request.method == "POST":
        result = calculate_optimal_mix()
        return render(request, 'home.html', {'result': result})
    else:
        return render(request, 'home.html')


def home_view(request):
    materials = RawMaterial.objects.all()
    materials_data = [{
        'name': material.name,
        'cost_per_tonne': get_cost_per_tonne(material.name)
    } for material in materials]

    selected_recipe = Recipe.objects.first()
    recipe_data = {
        'name': selected_recipe.name if selected_recipe else "No Recipe Selected",
        'raw_materials': []
    }

    if selected_recipe:
        materials_attributes_data = [
            {
                'name': material.name,
                'attributes': {
                    attr.attribute.name: attr.value for attr in MaterialAttributeValue.objects.filter(raw_material=material)
                }
            } for material in materials
        ]

        result = None
        if request.method == "POST":
            result = calculate_optimal_mix()

        context = {
            'materials': materials_data,
            'selected_recipe': recipe_data,
            'result': result,
            'materials_attributes': materials_attributes_data
        }
        return render(request, 'home.html', context)
    else:
        return render(request, 'home.html')
