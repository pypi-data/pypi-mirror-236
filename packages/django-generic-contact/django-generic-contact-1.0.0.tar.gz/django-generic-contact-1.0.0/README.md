## Django Generic Contact

[![PyPI version](https://img.shields.io/pypi/v/django-generic-contact.svg)](https://pypi.org/project/django-generic-contact/)
[![Run linter and tests](https://github.com/anexia/django-generic-contact/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/anexia/django-generic-contact/actions/workflows/test.yml)
[![Codecov](https://img.shields.io/codecov/c/gh/anexia/django-generic-contact)](https://codecov.io/gh/anexia/django-generic-contact)

Django module to store contact request in a structured yet generic manner within the database.

### Installation

1. Install using pip:

```shell
pip install django-generic-contact
```

2. Integrate `django_generic_contact` into your `settings.py`

```python
INSTALLED_APPS = [
    # ...
    'django_generic_contact',
    # ...
]
```

### Usage

The package provides you with a `Contact` model which expects `data` (dict) and the `name` of the requester, 
an optional `message` can be added:

```
from django_generic_contact.models import Contact

contact = Contact.objects.create(
    name="Mr. Tester",
    message="Please contact me via email or phone.",
    data={
        "email": "mr@tester.com",
        "phone": "123456",
    }
)
```

#### JSON Schema validation

The contents of `data` will be validated against a [json schema](https://json-schema.org/) defined in your project's 
`settings.py` (if provided). If needed you can define `GENERIC_CONTACT_DATA_SCHEMA` to check all relevant input
according to the expected structure, e.g.:

```
GENERIC_CONTACT_DATA_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "properties": {
        "email": {"type": "string", "format": "email"},
        "phone": {"type": "integer"},
    },
}
```

See more examples of `GENERIC_CONTACT_DATA_SCHEMA` in `tests/testapp/tests/test_model.py`.

#### Customizing the Contact model
The base model `GenericContact` only requires the `data`. Thus you can let your own models inherit from this and extend
it according to your project's needs, e.g.:

```
from django_generic_contact.models import GenericContact

class CustomContact(GenericContact):
    birth_date = models.Datetime(_("birth date"))
    zip = models.CharField(_("zip"))
```

## Unit Tests

See folder [tests/](tests/). The provided tests cover these criteria:
* success:
  * Contact model instance creation 
  * project's jsonschema validation
* failure:
  * project's jsonschema validation
  * exemplary custom jsonschema validation

Follow below instructions to run the tests.
You may exchange the installed Django and DRF versions according to your requirements. 
:warning: Depending on your local environment settings you might need to explicitly call `python3` instead of `python`.
```bash
# install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# setup environment
pip install -e .

# run tests
cd tests && python manage.py test
```

### Contributing

Contributions are welcomed! Read the [Contributing Guide](CONTRIBUTING.md) for more information.

### Licensing

See [LICENSE](LICENSE) for more information.
