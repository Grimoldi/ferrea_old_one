
from django import forms


class IsbnForm(forms.Form):
    '''BookForm This class handles the model of the ISBN Form

    This class handles the ORM representation of the form, setting up fields, data type, validation and so on.
    '''

    isbn = forms.CharField(
        label='isbn',
        max_length=13,
        required=False,
    )
