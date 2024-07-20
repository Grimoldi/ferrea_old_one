
from django import forms


class BookForm(forms.Form):
    '''BookForm This class handles the model of the Book Form

    This class handles the ORM representation of the form, setting up fields, data type, validation and so on.
    '''

    isbn = forms.CharField(
        label='isbn',
        max_length=40,
        required=False,
    )
    title = forms.CharField(
        label='title',
        max_length=40,
        required=False,
    )
    author = forms.CharField(
        label='author',
        max_length=40,
        required=False,
    )
    publishing = forms.CharField(
        label='publishing',
        max_length=40,
        required=False,
    )
    date_published = forms.IntegerField(
        label='date_published',
        required=False,
    )
    language = forms.CharField(
        label='language',
        max_length=3,
        required=False,
    )
    book_format = forms.CharField(
        label='format',
        max_length=40,
        required=False,
    )
    library = forms.CharField(
        label='library',
        max_length=40,
        required=True,
    )
    saga = forms.CharField(
        label='saga',
        max_length=40,
        required=False,
    )
    comments = forms.CharField(
        label='comments',
        required=False,
        widget=forms.HiddenInput()
    )
    cover = forms.CharField(
        label='cover',
        required=False,
        widget=forms.HiddenInput()
    )
