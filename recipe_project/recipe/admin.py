from django.contrib import admin
from .models import Recipe


# Customize admin site headers
admin.site.site_header = "Recipe App Administration"
admin.site.site_title = "Recipe App Admin"
admin.site.index_title = "Welcome to Recipe App Admin Panel"


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Admin interface for Recipe model."""
    list_display = ('name', 'cooking_time', 'user', 'get_difficulty')
    list_filter = ('user', 'cooking_time')
    search_fields = ('name', 'ingredients', 'description')
    
    def get_difficulty(self, obj):
        """Display difficulty in admin changelist."""
        return obj.difficulty()
    get_difficulty.short_description = 'Difficulty'

