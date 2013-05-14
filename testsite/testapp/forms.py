from django.forms import ModelForm
from models import TestModel, OtherTestModel

class TestModelForm(ModelForm):

    class Meta:
        model = TestModel
        fields = ['name']


class OtherTestModelForm(ModelForm):

    class Meta:
        model = OtherTestModel
        fields = ['title']