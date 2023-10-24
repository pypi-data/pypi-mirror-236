from django.utils.translation import gettext_lazy as _

from django_generic_contact.models import GENERIC_CONTACT_DATA_SCHEMA
from django_generic_contact.validators import JSONSchemaValidator


def get_help_text():
    return _("Meta data according to Schema: {schema}").format(
        schema=GENERIC_CONTACT_DATA_SCHEMA
    )


def get_validators():
    return [JSONSchemaValidator(limit_value=GENERIC_CONTACT_DATA_SCHEMA)]
