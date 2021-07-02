from django.apps import AppConfig


class ContactUsConfig(AppConfig):
    name = 'contact_us'

    def ready(self):
        import contact_us.signals
