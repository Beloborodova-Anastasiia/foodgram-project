from api_users.serializers import CustomUserSerializer
from django.shortcuts import get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError
from recipes.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                            Shopping, Tag, TagRecipe)
from rest_framework import serializers
from users.models import Subscribe, User

from api_foodgram.constants import RECIPES_LIMIT_DEFAULT

from .fields import Base64ImageField


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
        representation = super().to_representation(instance)
        return {**representation, **self.serialize_ingredient_recipe(instance)}


class IngredientRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = IngredientRecipe
        fields = ('amount',)


class IngredientRecipeCreateSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    amount = serializers.FloatField()

    def validate_amount(self, value):
        if value < 1:
            raise serializers.ValidationError(
                'Количество должно быть больше нуля'
            )
        return value


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
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientRecipeCreateSerializer(many=True, write_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )
    is_favorite = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorite',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(
            **validated_data,
            author=self.context['request'].user
        )
        for ingr in ingredients:
            current_ingredient = get_object_or_404(
                Ingredient,
                id=ingr['id']
            )
            IngredientRecipe.objects.create(
                ingredient=current_ingredient,
                recipe=recipe,
                amount=ingr['amount']
            )
        for tag in tags:
            current_tag = get_object_or_404(Tag, id=tag.id)
            TagRecipe.objects.create(
                tag=current_tag, recipe=recipe)
        Favorite.objects.create(
            user=self.context['request'].user,
            recipe=recipe
        )
        Shopping.objects.create(
            user=self.context['request'].user,
            recipe=recipe
        )
        return recipe

    def update(self, instance, validated_data):
        if 'ingredients' in validated_data:
            ingredients = validated_data.pop('ingredients')
            ingredient_recipe = IngredientRecipe.objects.filter(
                recipe=instance
            )
            ingredient_recipe.delete()
            for ingr in ingredients:
                current_ingredient = get_object_or_404(
                    Ingredient,
                    id=ingr['id']
                )
                IngredientRecipe.objects.create(
                    ingredient=current_ingredient,
                    recipe=instance,
                    amount=ingr['amount']
                )
        if 'tags' in validated_data:
            tags = validated_data.pop('tags')
            tag_recipe = TagRecipe.objects.filter(
                recipe=instance
            )
            tag_recipe.delete()
            for tag in tags:
                current_tag = get_object_or_404(Tag, id=tag.id)
                TagRecipe.objects.create(
                    tag=current_tag, recipe=instance)
        Recipe.objects.filter(id=instance.id).update(
            **validated_data,
        )
        return super().update(instance, validated_data)

    def get_is_favorite(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Favorite.objects.filter(user=user, recipe=obj).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Shopping.objects.filter(user=user, recipe=obj).exists()
        return False

    def to_representation(self, instance):
        tags_serialized = TagSerializer(
            instance.tags.all(),
            many=True,
        ).data
        ingredients_serialized = IngredientSerializer(
            instance.ingredients.all(),
            many=True,
            context={'recipe': instance}
        ).data
        representation = super().to_representation(instance)
        representation['tags'] = tags_serialized
        representation['ingredients'] = ingredients_serialized
        return {**representation}


class ShortcutRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        reasd_only_fields = ('id', 'name', 'image', 'cooking_time')


class SubscribtionSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )
        read_only = True

    def get_recipes(self, obj):
        try:
            recipes_limit = int(self.context['request'].GET['recipes_limit'])
        except MultiValueDictKeyError:
            recipes_limit = RECIPES_LIMIT_DEFAULT
        recipes = obj.recipes.all().order_by('-pub_date')[:recipes_limit]
        serializer = ShortcutRecipeSerializer(recipes, many=True)
        return serializer.data

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Subscribe.objects.filter(author=obj, user=user).exists()

    def get_recipes_count(self, obj):
        return obj.recipes.all().count()
