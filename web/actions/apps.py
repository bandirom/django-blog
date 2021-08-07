from django.apps import AppConfig


class ActionsConfig(AppConfig):
    name = 'actions'

    def ready(self):
        import actions.signals
