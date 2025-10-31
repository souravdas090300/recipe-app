from django.apps import AppConfig


class RecipeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    # Module path of the app
    name = 'apps.recipe'
    # Keep the historical app label as 'recipe' so existing migrations remain valid
    label = 'recipe'