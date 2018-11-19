from django.contrib import admin
from inventory.models import Location, ManufacturerRelationship, Manufacturer, Part, ResistorPart, GenericPart
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin, PolymorphicChildModelFilter

class ManufacturerRelationshipInline(admin.TabularInline):
    model = ManufacturerRelationship
    extra = 1

@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    inlines = (ManufacturerRelationshipInline,)

@admin.register(Location)

##class PartAdmin(admin.ModelAdmin):
##    inlines = (
##        ManufacturerRelationshipInline,
##        )
##    exclude = ('manufacturer',)
##
##admin.site.register(Manufacturer, ManufacturerAdmin)
##admin.site.register(Part, PartAdmin)

class PartChildAdmin(PolymorphicChildModelAdmin):
    base_model = Part
    
@admin.register(GenericPart)
class GenericPartAdmin(PartChildAdmin):
    base_model = GenericPart
    inlines = (ManufacturerRelationshipInline,)
    show_in_index = True
    search_fields = ['partNumber', 'binLocation', 'inventoryNumber', 'inStock',
                     'package']
    list_display = ['partNumber', 'binLocation', 'inventoryNumber', 'inStock',
                    'package', 'get_manufacturers', 'get_related']

@admin.register(ResistorPart)
class ResistorPartAdmin(PartChildAdmin):
    base_model = ResistorPart
    inlines = (ManufacturerRelationshipInline,)
    show_in_index = True
    list_display = ['partNumber', 'package', 'get_manufacturers', 'get_related']
    

@admin.register(Part)
class PartParentAdmin(PolymorphicParentModelAdmin):
    base_model = Part
    #child_models = (GenericPart, ResistorPart,)
    list_filter = (PolymorphicChildModelFilter,)
    inlines = (ManufacturerRelationshipInline,)
    exclude = ('manufacturer',)

    def get_child_models(self):
        return self.base_model.__subclasses__()
    
