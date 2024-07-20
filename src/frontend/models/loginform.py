
from django import forms
from django.utils.safestring import mark_safe


class LoginForm(forms.Form):
    '''LoginForm This class handles the model of the Login Form

    This class handles the ORM representation of the form, setting up fields, data type, validation and so on.
    '''
    username = forms.CharField(
        label=mark_safe('Username<br />'),
        max_length=20,
        required=False,
    )
    password = forms.CharField(
        label=mark_safe('<br />Password<br />'),
        max_length=20,
        required=False,
        widget=forms.PasswordInput,
    )
