from pulp import LpVariable, LpProblem, LpMinimize, LpStatus
from .models import RawMaterial, MaterialAttributeValue, Recipe, RecipeAttributeLimit, RecipeRawMaterial

def get_cost_per_tonne(material_name):
    try:
        cost_per_tonne_value = float(
            MaterialAttributeValue.objects.get(raw_material__name=material_name, attribute__name="Cost per tonne").value)
        return cost_per_tonne_value
    except MaterialAttributeValue.DoesNotExist:
        return 0  # If this property is not found, it defaults to 0

def calculate_optimal_mix():
    prob = LpProblem("OptimalFeedMix", LpMinimize)

    materials = RawMaterial.objects.all()
    var_dict = {}
    for material in materials:
        var_name = f"percentage_{material.name}"
        var_dict[material] = LpVariable(var_name, 0, 100)  # The percentage ranges from 0 to 100

    total_cost = 0
    for material in materials:
        cost_per_tonne_value = get_cost_per_tonne(material.name)
        total_cost += var_dict[material] * cost_per_tonne_value

    prob += total_cost

    selected_recipe = Recipe.objects.first()

    # Minimum and maximum percentage constraints for adding raw materials
    for material in materials:
        recipe_material = RecipeRawMaterial.objects.filter(recipe=selected_recipe, raw_material=material).first()
        if recipe_material:
            prob += var_dict[material] >= float(recipe_material.min_percentage)
            prob += var_dict[material] <= float(recipe_material.max_percentage)
            prob += var_dict[material] * 10 >= float(recipe_material.min_weight_kg_per_ton)
            prob += var_dict[material] * 10 <= float(recipe_material.max_weight_kg_per_ton)

    recipe_attribute_limits = RecipeAttributeLimit.objects.filter(recipe=selected_recipe)
    for ral in recipe_attribute_limits:
        attribute_name = ral.attribute.name
        min_value = float(ral.min_value)
        max_value = float(ral.max_value)

        total_attribute_value = 0
        for material in materials:
            try:
                attribute_value_obj = MaterialAttributeValue.objects.filter(raw_material=material,
                                                                            attribute__name=attribute_name).latest(
                    'id')
                attribute_value = float(attribute_value_obj.value)
            except MaterialAttributeValue.DoesNotExist:
                attribute_value = 0  # 默认值

            total_attribute_value += var_dict[material] * attribute_value

        prob += total_attribute_value >= min_value
        prob += total_attribute_value <= max_value

    prob += sum(var_dict.values()) == 100  # 总百分比应为100%

    prob.solve()

    if LpStatus[prob.status] == "Optimal":
        return {material.name: var_dict[material].varValue for material in materials}
    else:
        return "No optimal solution found!"
