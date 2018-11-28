from django.db import models

class Manufacturer(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class Bin(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Type(models.Model):
    name = models.CharField(max_length=30)
    #field = models.ForeignKey(Field, on_delete=models.CASCADE,
     #                         related_name="type", null=True)

    def __str__(self):
        return self.name


class Field(models.Model):
    FIELD_CHOICES = (
        ('char1', 'Character 1'),
        ('char2', 'Character 2'),
        ('integer1', 'Integer 1'),
        ('integer2', 'Integer 2'),
    )
    name = models.CharField(max_length=20)
    fields = models.CharField(max_length=15, choices=FIELD_CHOICES)
    typePart = models.ForeignKey(Type, on_delete=models.CASCADE, related_name="field", null=True)

class Part(models.Model):
    partType = models.ForeignKey(Type, on_delete=models.CASCADE, related_name="part")
    partNumber = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    location = models.ManyToManyField(Bin)
    manufacturer = models.ManyToManyField(Manufacturer,
                                          through='ManufacturerRelationship')
    char1 = models.CharField(max_length=100, blank=True)
    char2 = models.CharField(max_length=100, blank=True)
    integer1 = models.IntegerField(blank=True, null=True)
    integer2 = models.IntegerField(blank=True, null=True)
    #inStock = models.IntegerField()
    #package = models.CharField(max_length=30)

    def __str__(self):
        return self.partNumber

    def get_location(self):
        if self.location:
            return '%s' % " / ".join([location.name for location in self.location.all()])

    def get_manufacturers(self):
        if self.manufacturer:
            return '%s' % " / ".join([manufacturer.name for manufacturer in self.manufacturer.all()])

    def get_related(self):
        if self.manufacturer:
            return '%s' % " / ".join([str(ManufacturerRelationship.partNumber) for ManufacturerRelationship
                                      in self.manufacturerrelationship_set.all()]) #.objects.get(part=self)])
                                    

class ManufacturerRelationship(models.Model):
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    partNumber = models.IntegerField()
