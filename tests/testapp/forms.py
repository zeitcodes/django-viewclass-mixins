from .models import Author, Book
from django import forms
from django.forms.models import inlineformset_factory


class AuthorForm(forms.ModelForm):

    class Meta:
        model = Author
        fields = ('name',)


class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ('author', 'title',)


BookFormSet = inlineformset_factory(Author, Book, extra=1, can_delete=False)
