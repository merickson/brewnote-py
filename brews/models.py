from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

class Batch(models.Model):
    name = models.CharField(max_length=200, unique=True)
    num = models.IntegerField(validators=[MinValueValidator(0)], unique=True)
    created = models.DateTimeField('date created', auto_now_add=True)

    def __str__(self):
        return "Batch %s (%s)" % (self.num, self.name,)
    
class Brand(models.Model):
    name = models.CharField(max_length=200, unique=True)
    created = models.DateTimeField('date created')

    def __str__(self):
        return self.name

class MeasureType(models.TextChoices):
    DRY_WEIGHT_G = 'DW', _('Dry weight in grams')
    DRY_VOLUME_L = 'DV', _('Dry volume in liters')
    WET_VOLUME_L = 'WV', _('Wet volume in liters')

class FermentableType(models.Model):
    name = models.CharField(max_length=200, unique=True)
    measure = models.CharField(
        max_length=2,
        choices=MeasureType.choices,
        default=MeasureType.DRY_WEIGHT_G,
    )

    def __str__(self):
        return "%s (%s)" % (self.name, self.measure,)

class Fermentable(models.Model):
    name = models.CharField(max_length=200)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    fermentable_type = models.ForeignKey(FermentableType, on_delete=models.PROTECT)
    amount = models.FloatField()

    def __str__(self):
        return "%s %s" % (self.brand, self.name, )
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'brand', 'fermentable_type'],
                name='unique_fermentable_per_brand',
            ),
        ]

class FermentableBatch(models.Model):
    fermentable = models.ForeignKey(Fermentable, on_delete=models.PROTECT)
    purchased = models.DateTimeField('date purchased')

    def __str__(self):
        return "%s (id %s)" % (self.fermentable, self.pk,)

class YeastType(models.TextChoices):
    DRY = 'DRY', _('Dry yeast')
    WET = 'WET', _('Wet yeast')

class Yeast(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    name = models.CharField(max_length=200)
    measure = models.CharField(
        max_length=2,
        choices=MeasureType.choices,
        default=MeasureType.DRY_WEIGHT_G,
    )
    amount = models.IntegerField()
    yeastType = models.CharField(
        max_length=3,
        choices=YeastType.choices,
        default=YeastType.DRY,
    )

    def __str__(self):
        return "%s %s yeast" % (self.brand, self.name,)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'brand', 'yeastType'],
                name='unique_yeast_per_brand',
            ),
        ]

class YeastPacket(models.Model):
    yeast = models.ForeignKey(Yeast, on_delete=models.PROTECT)
    name = models.CharField(max_length=200)
    expiration = models.DateTimeField('expiration date')
    already_opened = models.BooleanField()

class AdditiveType(models.Model):
    name = models.CharField(max_length=200, unique=True)
    measure = models.CharField(
        max_length=2,
        choices=MeasureType.choices,
        default=MeasureType.DRY_WEIGHT_G
    )   

class Additive(models.Model):
    name = models.CharField(max_length=200)
    type = models.ForeignKey(AdditiveType, on_delete=models.PROTECT)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    name = models.CharField(max_length=200)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'brand', 'type'],
                name='unique_additive_per_brand',
            ),
        ]

class EquipmentType(models.Model):
    name = models.CharField(max_length=200, unique=True)
    measure = models.CharField(
        max_length=2,
        choices=MeasureType.choices,
        default=MeasureType.DRY_WEIGHT_G
    )
    size = models.FloatField()

class Fermentation(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.PROTECT)
    startdate = models.DateTimeField('fermentation start', auto_now_add=True)
    enddate = models.DateTimeField('fermentation end', blank=True, null=True)
    start_specific_gravity = models.FloatField()
    end_specific_gravity = models.FloatField()
    start_ph = models.FloatField()
    end_ph = models.FloatField()
    start_ta = models.FloatField()
    end_ta = models.FloatField()

class FermentationFermentable(models.Model):
    fermentation = models.ForeignKey(Fermentation, on_delete=models.PROTECT)
    fermentable = models.ForeignKey(Fermentable, on_delete=models.PROTECT)
    amount = models.FloatField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['fermentation', 'fermentable'],
                name='one_fermentable_per_fermentation',
            ),
        ]

class FermentationYeast(models.Model):
    fermentation = models.ForeignKey(Fermentation, on_delete=models.PROTECT)
    yeast = models.ForeignKey(YeastPacket, on_delete=models.PROTECT)
    amount = models.FloatField()

class FermentationAdditive(models.Model):
    fermentation = models.ForeignKey(Fermentation, on_delete=models.PROTECT)
    additive = models.ForeignKey(Additive, on_delete=models.PROTECT)
    added_time = models.DateTimeField()
    amount = models.FloatField()

