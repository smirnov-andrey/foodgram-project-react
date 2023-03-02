from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Наименование',
        unique=True,
        blank=False,
        max_length=200)
    color = models.CharField(
        verbose_name='Цвет в HEX',
        blank=False,
        max_length=7)
    slug = models.SlugField(
        verbose_name='Уникальный слаг',
        unique=True,
        blank=False,
        max_length=200)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return f'{self.name} ({self.slug})'


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Наименование',
        unique=True,
        blank=False,
        max_length=200)
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения',
        blank=False,
        max_length=200)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return f'{self.name} ({self.measurement_unit})'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_recipes',
        verbose_name='Автор рецепта')
    name = models.CharField(
        blank=False,
        max_length=200,
        verbose_name='Название')
    image = models.ImageField(
        upload_to='recipe_images/',
        blank=False,
        verbose_name='Ссылка на картинку на сайте')
    text = models.TextField(
        blank=False,
        verbose_name='Описание')
    cooking_time = models.PositiveSmallIntegerField(
        blank=False,
        verbose_name='Время приготовления (в минутах)')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientInRecipe',
        related_name='ingredient_recipes',
        verbose_name='Список ингредиентов')
    tag = models.ManyToManyField(
        Tag,
        related_name='tag_recipes',
        verbose_name='Список тегов')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.PROTECT,
        null=False,
        verbose_name='Ингридиент')
    amount = models.PositiveSmallIntegerField(
        blank=False,
        verbose_name='Количество')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        null=False,
        verbose_name='Рецепт')

    def __str__(self):
        return f'{self.ingredient} в количестве {self.amount}'


class FavoriteRecipes(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        related_name='user_favorites',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        null=False,
        related_name='recipe_favorites',
        verbose_name='Рецепт'
    )

    class Meta:
        ordering = ('recipe',)
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

    def __str__(self):
        return (f' Рецепт {self.recipe} в избранном у '
                f'{self.user}')


class ShoppingCarts(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        related_name='user_cart',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        null=False,
        related_name='recipe_carts',
        verbose_name='Рецепт'
    )

    class Meta:
        ordering = ('recipe',)
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        return (f' Рецепт {self.recipe} в списке покупок у '
                f'{self.user}')
