from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView
from inventory.models import Part, GenericPart
from inventory.forms import (PartListSearchForm, GenericPartForm, ManufacturerForm,
ManufacturerFormSet)
from django.views.generic.edit import CreateView
from django.forms.models import inlineformset_factory
from django.urls import reverse_lazy

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

class PartListView(ListView):
    model = Part
    paginate_by = 20
    template_name = 'list.html'
    context_object_name = 'parts'
    queryset = Part.objects.prefetch_related('manufacturer')
    query_part = ''

    def get_context_data(self, **kwargs):
        context = super(PartListView, self).get_context_data(**kwargs)
        context['form'] = PartListSearchForm(self.query_part)
        context['search_request'] = ('query_part=' + str(self.query_part))
        return context

    def get(self, request, *args, **kwargs):
        self.query_part = request.GET.get('query_part', '')
        return super(PartListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        if not self.query_part:
            part_list = Part.objects.all()
        else:
            part_list = Part.objects.filter(name__icontains=self.query_part)

        return part_list


class PartCreate(CreateView):
##    model = GenericPart
##    fields = '__all__'
    form_class = GenericPartForm
    template_name = 'genericpart_form.html'
    success_url = reverse_lazy('inventory')

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        part_formset = ManufacturerFormSet()
        return self.render_to_response(
            self.get_context_data(form=form, part_formset=part_formset))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        part_formset = ManufacturerFormSet(request.POST)
        if (form.is_valid() and part_formset.is_valid()):
            return self.form_valid(form, part_formset)
        else:
            return self.form_invalid(form, part_formset)

    def form_valid(self, form, part_formset):
        self.object = form.save()
        part_formset.instance = self.object
        part_formset.save()
        return super(PartCreate, self).form_valid(form)

    def form_invalid(self, form, part_formset):
        return self.render_to_response(
            self.get_context_data(form=form,part_formset=part_formset))

##def create_generic_part(request, id):
##    part = Part.objects.get(id=id)
##    form = GenericPartForm(instance = part)
##    ManufacturerFormset = inlineformset_factory(GenericPart, ManufacturerRelationship)
##    formset = ManufacturerFormset(instance = part)
##
##    dict = {
##        "form": form,
##        "formset": formset,
##        "instance": part}
##
##    if request.method == "POST":
##        form = GenericPartForm(request.POST, instance = part)
##        formset = ManufacturerFormset(request.POST, instance = client)
##
##        if form.is_valid() and formset.is_valid():
##            part_mod = form.save()
##            formset.save()
##
##            id = part_mod.id
##            return HttpResponseRedirect("/inventory/")
##        else:
##            return HttpResponseRedirect("/inventory/")
##
##    return render_to_response(
##        "genericpart_form.html",
##        dict,
##        context_instance=RequestContext(request))
    
