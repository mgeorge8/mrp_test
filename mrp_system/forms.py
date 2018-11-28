from django import forms
from mrp_system.models import Bin, Part, ManufacturerRelationship, Field, Type
from django.forms import ModelForm, BaseInlineFormSet
from django.forms.models import inlineformset_factory

FIELD_TYPES = {
    'char1': forms.CharField,
    'char2': forms.CharField,
    'integer1': forms.IntegerField,
    'integer2': forms.IntegerField
    }
FIELDS_F = {
    'char1': 'char1',
    'char2': 'char2',
    'integer1': 'integer1',
    'integer2': 'integer2'
    }

class PartForm(ModelForm):
##    class Meta:
##        model = Part
##        exclude = ('manufacturer',)  

        def __init__(self, type_id, *args, **kwargs):
            super(PartForm, self).__init__(*args, **kwargs)
            #type_id = kwargs.pop('type_id', 0)
            partType = Type.objects.get(id=type_id)
           # self.fields.pop('partType')
##            self.fields['partType'].initial = partType
##            self.fields['partType'].widget.attrs['readonly'] = True
##            self.fields['partType'].widget.attrs['disabled'] = True

            for field in partType.field.all():
                #self.fields[field.name] = FIELD_TYPES[field.fields](label = field.name)
                self.fields[FIELDS_F[field.fields]].label = field.name
            #parts = partType.field.all()
            extra_fields = ('char1', 'char2', 'integer1', 'integer2')
            for field in extra_fields:
                if field not in partType.field.values_list('fields', flat=True):
                    self.fields.pop(field)
            
        class Meta:
            model = Part
            exclude = ('manufacturer', 'partType')
            

class ManufacturerForm(ModelForm):
    class Meta:
        model = ManufacturerRelationship
        exclude = ('part',)
    
ManufacturerFormSet = inlineformset_factory(Part, ManufacturerRelationship,
                                            form=ManufacturerForm, extra=1)

class TypeForm(ModelForm):
    class Meta:
        model = Type
        exclude = ()
        labels = {
            "name": "Type Name"
        }

class FieldForm(ModelForm):
    class Meta:
        model = Field
        exclude = ()
        labels = {
            "name": "Field Name",
            "fields": "Field Type"
        }

class CustomInlineFormset(BaseInlineFormSet):
    def clean(self):
        if any(self.errors):
            return

        names = []
        fields = []
        duplicates = False
        
        for form in self.forms:
           if form.cleaned_data:
               name = form.cleaned_data['name']
               field = form.cleaned_data['fields']

               if name and field:
                   if name in names:
                       duplicates = True
                   names.append(name)

                   if field in fields:
                       duplicates = True
                   fields.append(field)

               if duplicates:
                   raise forms.ValidationError('Fields must have unique names and types.')
               if name and not field:
                   raise forms.ValidationError('All field names must have an associated type.')
               elif field and not name:
                   raise forms.ValidationError('All field names must have an associated type.')

                        

FieldFormSet = inlineformset_factory(Type, Field, form=FieldForm, extra=4, formset=CustomInlineFormset)

class TypeSelectForm(forms.Form):
    partType = forms.ModelChoiceField(label='', queryset=Type.objects.order_by('name'),
                                widget=forms.Select(attrs={"onChange":'this.form.submit()'}))

    def save(self):
        return (self.cleaned_data.get('partType'))
        
