from django import forms
from django.contrib import admin

from django_generic_contact.models import Contact
from django_generic_contact.utils import get_help_text, get_validators


class ContactAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ContactAdminForm, self).__init__(*args, **kwargs)
        self.fields["data"].help_text = get_help_text()
        self.fields["data"].validators = get_validators()

    class Meta:
        model = Contact
        exclude = ()


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = [
        "creation_date",
        "name",
    ]
    form = ContactAdminForm
