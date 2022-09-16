from rest_framework import serializers

from recipes.models import Ingredient, IngredientRecipe, Recipe, Tag
from api_users.serializers import UserSerializer


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )

    def serialize_ingredient_recipe(self, ingridient):
        if 'recipe' in self.context:
            ingredient_recipe = ingridient.ingredientrecipe_set.filter(
                recipe=self.context['recipe']
            ).first()
            if ingredient_recipe:
                return IngredientRecipeSerializer(ingredient_recipe).data
        return {}

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        return {**rep, **self.serialize_ingredient_recipe(instance)}


class IngredientRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = IngredientRecipe
        fields = ('amount',)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )


class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    # ingredients = IngredientSerializer(many=True, read_only=True)
    ingredients = serializers.SerializerMethodField()
    # tags = TagSerializer(many=True, read_only=True)

    class Meta:
        depth = 1
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            # 'is_favorited',
            # 'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_ingredients(self, recipe):
        return IngredientSerializer(
            recipe.ingredients.all(),
            many=True,
            context={'recipe': recipe}
        ).data
