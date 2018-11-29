from django.contrib import admin
from mrp_system.models import (Part, Location,
Manufacturer, ManufacturerRelationship, Type)
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class PartResource(resources.ModelResource):
    class Meta:
        model = Part
        exclude = ('manufacturer',)

    def dehydrate_char2(self, part):
        if part.char2 == 'null':
            return ''

class PartAdmin(ImportExportModelAdmin):
    resource_class = PartResource

class ManufacturerResource(resources.ModelResource):
    class Meta:
        model = Manufacturer    

class ManufacturerAdmin(ImportExportModelAdmin):
    resource_class = ManufacturerResource

class ManufacturerRelationshipResource(resources.ModelResource):
    class Meta:
        model = ManufacturerRelationship    

class ManufacturerRelationshipAdmin(ImportExportModelAdmin):
    resource_class = ManufacturerRelationshipResource

class LocationResource(resources.ModelResource):
    class Meta:
        model = Location    

class LocationAdmin(ImportExportModelAdmin):
    resource_class = LocationResource

    
admin.site.register(Part, PartAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(ManufacturerRelationship, ManufacturerRelationshipAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Type)
