from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Subscription, User


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author')
    list_display_links = ('id', 'user')
    search_fields = ('user__email', 'user__first_name', 'user__last_name',
                     'author__email', 'author__first_name', 'author__last_name'
                     )
    autocomplete_fields = ('user', 'author')
    search_help_text = 'Поиск по имени, фамилии и email пользователся и автора'
    actions_selection_counter = True
    show_full_result_count = True


admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(User, UserAdmin)
