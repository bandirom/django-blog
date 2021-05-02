from django.db.models import IntegerChoices
from django.utils.translation import gettext_lazy as _


class GenderChoice(IntegerChoices):
    MALE = 0, _('Male')
    Female = 1, _('Female')
