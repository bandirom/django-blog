from django.db.models import IntegerChoices
from django.utils.translation import gettext_lazy as _


class ArticleStatus(IntegerChoices):
    INACTIVE = (0, _('Inactive'))
    ACTIVE = (1, _('Active'))
