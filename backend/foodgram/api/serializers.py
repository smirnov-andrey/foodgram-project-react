import base64

from django.core.files.base import ContentFile
from django.db import transaction

from rest_framework import serializers

from recipes.models import Ingredient, IngredientInRecipe, Recipe, Tag, User
from users.serializers import UserSerializer


class Base64ImageField(serializers.ImageField):
    """Декодирует base64 в картинку и сохраняет в media."""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения всех."""
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения ингредиентов в рецепте."""
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredient.objects.all()

    )
    name = serializers.ReadOnlyField(
        source='ingredient.name',
    )
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit',
    )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class IngredientAddSerializer(serializers.Serializer):
    """Сериализатор для добавления ингредиентов в рецепт."""
    id = serializers.IntegerField(required=True)
    amount = serializers.IntegerField(required=True)


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов."""
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для рецептов."""
    is_favorited = serializers.BooleanField()
    is_in_shopping_cart = serializers.BooleanField()
    ingredients = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)
    author = UserSerializer()

    class Meta:
        model = Recipe
        fields = ('id',
                  'tags',
                  'author',
                  'ingredients',
                  'is_favorited',
                  'is_in_shopping_cart',
                  'name',
                  'image',
                  'text',
                  'cooking_time'
                  )

    def get_ingredients(self, obj):
        return IngredientInRecipeSerializer(
            IngredientInRecipe.objects.filter(recipe=obj).all(),
            many=True
        ).data


class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления и изменения рецептов."""
    image = Base64ImageField()
    ingredients = IngredientAddSerializer(many=True, write_only=True)
    tags = serializers.ListField(write_only=True)

    class Meta:
        model = Recipe
        fields = ('ingredients',
                  'tags',
                  'image',
                  'name',
                  'text',
                  'cooking_time',
                  )

    def validate(self, data):
        if not data.get('tags'):
            raise serializers.ValidationError(
                'Выберите один или несколько тегов')
        ingredients = data.get('ingredients')
        ingredients_in_recipe = []
        for ingredient in ingredients:
            if ingredient.get('amount') <= 0:
                raise serializers.ValidationError(
                    'Количество ингредиента должно быть больше 0')
            ingredients_in_recipe.append(ingredient.get('id'))
        if len(ingredients_in_recipe) == 0:
            raise serializers.ValidationError(
                'Добавьте хотя бы один ингредиент')
        if len(ingredients_in_recipe) != len(set(ingredients_in_recipe)):
            raise serializers.ValidationError(
                'Ингредиенты не должны повторяться')
        return data

    @transaction.atomic
    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(
            author=self.context.get("request").user,
            **validated_data
        )
        recipe.tags.add(*tags)
        ingredients_to_recipe = [
            IngredientInRecipe(
                recipe=recipe,
                ingredient_id=ingredient.get('id'),
                amount=ingredient.get('amount')
            ) for ingredient in ingredients
        ]
        IngredientInRecipe.objects.bulk_create(ingredients_to_recipe)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance.tags.clear()
        instance.tags.add(*tags)
        IngredientInRecipe.objects.filter(recipe_id=instance.pk).delete()
        ingredients_to_recipe = [
            IngredientInRecipe(
                recipe=instance,
                ingredient_id=ingredient.get('id'),
                amount=ingredient.get('amount')
            ) for ingredient in ingredients
        ]
        IngredientInRecipe.objects.bulk_create(ingredients_to_recipe)
        super().update(instance, validated_data)
        return instance

    def to_representation(self, instance):
        serializer = RecipeSerializer(instance)
        return serializer.data


class RecipeShortSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения рецептов в подписке."""
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscriptionListSerializer(UserSerializer):
    """Сериализатор для отображения подписок пользователя."""
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

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
            'recipes_count'
        )

    def get_recipes(self, obj):
        request = self.context.get('request')
        queryset = obj.user_recipes.all()
        if request:
            recipes_limit = request.query_params.get('recipes_limit', None)
            if recipes_limit:
                queryset = queryset[:int(recipes_limit)]
        return RecipeShortSerializer(queryset, many=True).data

    @staticmethod
    def get_recipes_count(obj):
        return obj.user_recipes.all().count()
