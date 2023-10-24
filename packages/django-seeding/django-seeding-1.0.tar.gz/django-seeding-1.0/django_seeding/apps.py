from django.apps import AppConfig


class SeedingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'seeding'

    def ready(self):
        from .seeder_registry import SeederRegistry
        SeederRegistry.on_run()
        return super().ready()
