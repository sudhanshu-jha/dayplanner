from django.contrib import admin

# Register your models here.
from .models import Goal


class GoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'user')
    search_fields = ['title']

    fieldsets = [
        ('user', {'fields': ['user']}),
        ('title', {'fields': ['title']}),
        ('description', {'fields': ['description']}),
    ]
    list_filter = ['user']


admin.site.register(Goal, GoalAdmin)
