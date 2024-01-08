from django import forms


class SearchMangaForm(forms.Form):
    search = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'search-input',
                'placeholder': 'Search a manga',
                'name': 'search',

            }
        ),
        label='',
        required=False,
        max_length=40
    )
