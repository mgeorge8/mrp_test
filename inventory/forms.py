from django import forms
from inventory.models import GenericPart, ManufacturerRelationship
from django.forms import ModelForm
from django.forms.models import inlineformset_factory

class PartListSearchForm(forms.Form):
    query_part = forms.CharField(label=('Part'), required=False)

    def __init__(self, query_part):
        super(PartListSearchForm, self).__init__()
        self.fields['query_part'].initial = query_part

class GenericPartForm(ModelForm):
    class Meta:
        model = GenericPart
        exclude = ('manufacturer',)

class ManufacturerForm(ModelForm):
    class Meta:
        model = ManufacturerRelationship
        exclude = ('part',)
    
ManufacturerFormSet = inlineformset_factory(GenericPart, ManufacturerRelationship,
                                            form=ManufacturerForm, extra=1)

