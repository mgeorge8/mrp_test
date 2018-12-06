from django.db import models

class Manufacturer(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Type(models.Model):
    name = models.CharField(max_length=30)
    suffix = models.CharField(max_length=3)
    #field = models.ForeignKey(Field, on_delete=models.CASCADE,
     #                         related_name="type", null=True)

    def __str__(self):
        return self.name


class Field(models.Model):
    FIELD_CHOICES = (
        ('char1', 'Character 1'),
        ('char2', 'Character 2'),
        ('char3', 'Character 3'),
        ('char4', 'Character 4'),
        ('char5', 'Character 5'),
        ('char6', 'Character 6'),
        ('char7', 'Character 7'),
        ('char8', 'Character 8'),
        ('integer1', 'Integer 1'),
        ('integer2', 'Integer 2'),
    )
    name = models.CharField(max_length=20)
    fields = models.CharField(max_length=15, choices=FIELD_CHOICES)
    typePart = models.ForeignKey(Type, on_delete=models.CASCADE, related_name="field", null=True)

class Part(models.Model):
    partType = models.ForeignKey(Type, on_delete=models.CASCADE, related_name="part")
    partNumber = models.CharField(max_length=30, blank=True, editable=False)
    engimusingPartNumber = models.CharField(max_length=30, editable=False)
    description = models.CharField(max_length=300, blank=True)
    #location = models.ManyToManyField(Location, related_name="loc")
    location = models.ManyToManyField(Location, through='LocationRelationship')
    manufacturer = models.ManyToManyField(Manufacturer,
                                          through='ManufacturerRelationship')
    char1 = models.CharField(max_length=30, blank=True)
    char2 = models.CharField(max_length=30, blank=True)
    char3 = models.CharField(max_length=30, blank=True)
    char4 = models.CharField(max_length=30, blank=True)
    char5 = models.CharField(max_length=30, blank=True)
    char6 = models.CharField(max_length=30, blank=True)
    char7 = models.CharField(max_length=30, blank=True)
    char8 = models.CharField(max_length=30, blank=True)
    integer1 = models.IntegerField(blank=True, null=True)
    integer2 = models.IntegerField(blank=True, null=True)
    datasheet = models.FileField(upload_to='documents/', blank=True)
    #inStock = models.IntegerField()
    #package = models.CharField(max_length=30)

    def __str__(self):
        return self.partNumber

    def get_location(self):
        if self.location:
            #return self.location.all()
            #return '%s' % "-" % '%s' % " / ".join([location.name for location in self.location.all()])
            return '%s' % "\n".join([LocationRelationship.location.name + " - " + str(LocationRelationship.stock) for LocationRelationship
                                     in self.locationrelationship_set.all()])
                                     

    def get_manufacturers(self):
        if self.manufacturer:
            return '%s' % " / ".join([manufacturer.name for manufacturer in self.manufacturer.all()])

    def get_related(self):
        if self.manufacturer:
            return '%s' % " / ".join([str(ManufacturerRelationship.partNumber) for ManufacturerRelationship
                                      in self.manufacturerrelationship_set.all()]) #.objects.get(part=self)])

    def save(self, *args, **kwargs):
        if not self.id:
            partType = self.partType
            self.engimusingPartNumber = increment_engi_partnumber(partType)
            self.partNumber = int(self.engimusingPartNumber[3:9])
        super().save(*args, **kwargs)

def increment_engi_partnumber(partType):
    last_id = Part.objects.filter(partType=partType).order_by('partNumber').last()
    suffix = partType.suffix
    if not last_id:
        return suffix + '000001'
    partNumber = last_id.partNumber
    partNumber = int(partNumber)
    new_partNumber = partNumber + 1
    new_engi_partNumber = suffix + str(new_partNumber).zfill(6)
    return new_engi_partNumber

class ManufacturerRelationship(models.Model):
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    partNumber = models.CharField(max_length=20, blank=True)

class LocationRelationship(models.Model):
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    stock = models.IntegerField(blank=True, null=True)
