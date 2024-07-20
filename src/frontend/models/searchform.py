from django import forms


class SearchForm(forms.Form):
    '''BookForm This class handles the model of the Search Form

    This class handles the ORM representation of the form, setting up fields, data type, validation and so on.
    '''

    BOOK_STATUS = (
        ("", ""),
        ("Available", "Available"),
    )

    author = forms.CharField(label='author', max_length=20, required=False)
    title = forms.CharField(label='title', max_length=20, required=False)
    saga = forms.CharField(label='saga', max_length=20, required=False)
    status = forms.ChoiceField(choices=BOOK_STATUS, required=False)
