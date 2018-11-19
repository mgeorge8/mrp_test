from django.db import models

from polymorphic.models import PolymorphicModel

class Manufacturer(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Part(PolymorphicModel):
    partNumber = models.CharField(max_length=30)
    #location = models.CharField(max_length=30)
    #inventoryNumber = models.IntegerField(blank=True, null=True)
    #inStock = models.IntegerField()
    #package = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    location = models.ManyToManyField(Location)
    manufacturer = models.ManyToManyField(Manufacturer, through='ManufacturerRelationship')

    def __str__(self):
        return self.partNumber

    def get_manufacturers(self):
        if self.manufacturer:
            return '%s' % " / ".join([manufacturer.name for manufacturer in self.manufacturer.all()])

    def get_related(self):
##        qs = ManufacturerRelationship.objects.select_related('manufacturer')
##        return qs.filter(part=self)
        if self.manufacturer:
            return '%s' % " / ".join([str(ManufacturerRelationship.partNumber) for ManufacturerRelationship
                                      in self.manufacturerrelationship_set.all()]) #.objects.get(part=self)])
                                    

class ManufacturerRelationship(models.Model):
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    partNumber = models.IntegerField()


class GenericPart(Part):
    binLocation = models.CharField(max_length=30)
    inventoryNumber = models.IntegerField()
    inStock = models.IntegerField()
    package = models.CharField(max_length=30)


class ResistorPart(Part):
    package = models.CharField(max_length=15)

##class Product(models.Model):
##    name = models.CharField(max_length=30)
##    parts = models.ManyToManyField(Part)
