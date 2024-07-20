
from django import forms


class UserForm(forms.Form):
    '''BookForm This class handles the model of the User Form

    This class handles the ORM representation of the form, setting up fields, data type, validation and so on.
    '''

    email = forms.EmailField(
        label='email',
        max_length=40,
        required=False,
    )
    username = forms.CharField(
        label='user',
        max_length=20,
        required=False,
        widget=forms.TextInput(
            attrs={'readonly': 'readonly'}
        ),
    )
    name = forms.CharField(
        label='name',
        max_length=20,
        required=False,
    )
    surname = forms.CharField(
        label='surname',
        max_length=20,
        required=False,
    )
    city = forms.CharField(
        label='city',
        max_length=20,
        required=False,
    )
    address = forms.CharField(
        label='address',
        required=False,
    )
    phone = forms.IntegerField(
        label='phone',
        max_value=9999999999,
        min_value=0000000000,
        required=False,
    )
    card_number = forms.CharField(
        label='card_number',
        max_length=20,
        required=True,
        widget=forms.TextInput(
            attrs={'readonly': 'readonly'}
        ),
    )
