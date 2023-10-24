import jsonschema
from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator


class JSONSchemaValidator(BaseValidator):
    def compare(self, value, schema):
        try:
            jsonschema.validate(
                value, schema, format_checker=jsonschema.draft202012_format_checker
            )
        except jsonschema.exceptions.ValidationError as e:
            raise ValidationError(str(e))
