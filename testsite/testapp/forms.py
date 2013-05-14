from django import forms
from django.forms.models import inlineformset_factory
from models import Author, Book

class AuthorForm(forms.ModelForm):

    class Meta:
        model = Author
        fields = ('name',)


class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ('author', 'title', 'published',)


BookFormSet = inlineformset_factory(Author, Book)