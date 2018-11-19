from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, TemplateView
from mrp_system.models import Part, Type, Field, Manufacturer, Location
from mrp_system.forms import (PartForm, ManufacturerForm,
ManufacturerFormSet, FieldFormSet, TypeForm, TypeSelectForm)
from django.views.generic.edit import CreateView
from django.forms.models import inlineformset_factory
from django.urls import reverse, reverse_lazy
from django.forms import ModelForm
from django import forms

class TypeListView(ListView):
    model = Type
    template_name = 'type_list.html'
    

def PartCreate(request, type_id):
##    model = GenericPart
##    fields = '__all__'
##    form_class = PartForm
##    template_name = 'part_form.html'
##    success_url = reverse_lazy('index')
    partType = Type.objects.get(id=type_id)

    if request.method == 'POST':
        #self.object = None
        form = PartForm(type_id, request.POST)
        part_formset = ManufacturerFormSet(request.POST)
        if (form.is_valid() and part_formset.is_valid()):
            self_object = form.save(commit=False)
            self_object.partType_id = type_id
            self_object.save()
            form.save_m2m()
            part_formset.instance = self_object
           # part_formset = ManufacturerFromSet(request.POST, instance = self_object)
            part_formset.save()
            url = reverse('list_parts', args=[partType.pk])
            return HttpResponseRedirect(url)
    else:
        #self.object = None
        form = PartForm(type_id=type_id)
        part_formset = ManufacturerFormSet()
    return render(request,'part_form.html',{'form': form,
                                            'part_formset': part_formset,
                                            'partType': partType})

        

##class PartCreate(CreateView):
####    model = GenericPart
####    fields = '__all__'
##    form_class = PartForm
##    template_name = 'part_form.html'
##    success_url = reverse_lazy('index')
##
##    def get(self, request, *args, **kwargs):
##        self.object = None
##        form_class = self.get_form_class()
##        form = self.get_form(form_class)
##        part_formset = ManufacturerFormSet()
##        return self.render_to_response(
##            self.get_context_data(form=form, part_formset=part_formset))
##
##    def post(self, request, *args, **kwargs):
##        self.object = None
##        form_class = self.get_form_class()
##        form = self.get_form(form_class)
##        part_formset = ManufacturerFormSet(request.POST)
##        if (form.is_valid() and part_formset.is_valid()):
##            return self.form_valid(form, part_formset)
##        else:
##            return self.form_invalid(form, part_formset)
##
##    def form_valid(self, form, part_formset):
##        self.object = form.save()
##        part_formset.instance = self.object
##        part_formset.save()
##        return super(PartCreate, self).form_valid(form)
##
##    def form_invalid(self, form, part_formset):
##        return self.render_to_response(
##            self.get_context_data(form=form,part_formset=part_formset))



class TypeCreate(CreateView):
    form_class = TypeForm
    template_name = 'type_form.html'
    success_url = reverse_lazy('list_types')

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        field_formset = FieldFormSet()
        return self.render_to_response(
            self.get_context_data(form=form, field_formset=field_formset))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        field_formset = FieldFormSet(request.POST)
        if (form.is_valid() and field_formset.is_valid()):
            return self.form_valid(form, field_formset)
        else:
            return self.form_invalid(form, field_formset)

    def form_valid(self, form, field_formset):
        self.object = form.save()
        field_formset.instance = self.object
        field_formset.save()
        return super(TypeCreate, self).form_valid(form)

    def form_invalid(self, form, part_formset):
        return self.render_to_response(
            self.get_context_data(form=form, field_formset=field_formset))


class PartListView(ListView):
    model = Part
    paginate_by = 20
    template_name = 'list.html'
    context_object_name = 'parts'
    queryset = Part.objects.prefetch_related('manufacturer')
    query_part = ''

##    def get_context_data(self, **kwargs):
##        context = super(PartListView, self).get_context_data(**kwargs)
##        context['form'] = PartListSearchForm(self.query_part)
##        context['search_request'] = ('query_part=' + str(self.query_part))
##        return context
##
##    def get(self, request, *args, **kwargs):
##        self.query_part = request.GET.get('query_part', '')
##        return super(PartListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        if not self.query_part:
            part_list = Part.objects.all()
        else:
            part_list = Part.objects.filter(name__icontains=self.query_part)

        return part_list

class ListParts(TemplateView):
    template_name = 'part_list.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        if context['form'].is_valid():
            print ('yes done')
            partType = context['form'].save()
            
            url = reverse('list_parts', args=[partType.pk])
            #url = request.GET.get('next', reverse('dashboard'))
            return HttpResponseRedirect(url)
            #return redirect('week_timesheet', user_id=entry.pk)
        return super(ListParts, self).render_to_response(context)
    
    def get_context_data(self, *args, **kwargs):
        context = super(ListParts, self).get_context_data(**kwargs)

        form = TypeSelectForm(self.request.POST or None)
        
        type_id = self.kwargs['type_id']
        partType = Type.objects.get(id=type_id)
        parts = Part.objects.filter(partType=partType)
        fields = Field.objects.filter(typePart_id=type_id)

        context.update({
            'type': partType,
            'parts': parts,
            'fields': fields,
            'form': form,
            })
        return context

class CreateManufacturer(CreateView):
    model = Manufacturer
    fields = ['name']
    template_name = 'manufacturer_form.html'
    success_url = reverse_lazy('list_types')

class CreateLocation(CreateView):
    model = Location
    fields = ['name']
    template_name = 'location_form.html'
    success_url = reverse_lazy('list_types')
