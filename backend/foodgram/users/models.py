from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    first_name = models.CharField(_("first name"), max_length=150, blank=False)
    last_name = models.CharField(_("last name"), max_length=150, blank=False)
    email = models.EmailField(_("email address"), unique=True, blank=False)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_(
            "Designates whether the user can log into this admin site."),
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password', 'first_name', 'last_name']

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ['email']

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.email})'


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Пользователь')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribers',
        verbose_name='Автор на которого подписан пользователь')

    class Meta:
        ordering = ('user',)
        verbose_name = 'подписчика'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                name='unique_subscription',
                fields=['user', 'author'],
            ),
            models.CheckConstraint(
                name='prevent_self_subscription',
                check=~models.Q(user=models.F('author')),
            ),
        ]

    def __str__(self):
        return f'{self.user} подписан на {self.author}'
