from django.apps import AppConfig


class ShinobiVerseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shinobi_verse'


    def ready(self):
        import shinobi_verse.signals