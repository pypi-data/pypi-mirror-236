from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

GENERIC_CONTACT_DATA_SCHEMA = getattr(settings, "GENERIC_CONTACT_DATA_SCHEMA", {})


class GenericContact(models.Model):
    creation_date = models.DateTimeField(
        verbose_name=_("Creation date"),
        blank=False,
        null=False,
        auto_now_add=True,
    )

    data = models.JSONField(
        _("meta data"),
        default=dict,
    )

    class Meta:
        abstract = True


class Contact(GenericContact):
    name = models.CharField(_("name"), max_length=255)

    message = models.TextField(_("message"), blank=True)
