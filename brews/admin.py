from django.contrib import admin

from .models import Batch, Brand, FermentableType, Fermentable, FermentableBatch, Yeast, YeastPacket, AdditiveType, Additive, EquipmentType, Fermentation, FermentationFermentable, FermentationYeast, FermentationAdditive

admin.site.register(Batch)
admin.site.register(Brand)
admin.site.register(FermentableType)
admin.site.register(Fermentable)
admin.site.register(FermentableBatch)
admin.site.register(Yeast)
admin.site.register(YeastPacket)
admin.site.register(AdditiveType)
admin.site.register(Additive)
admin.site.register(EquipmentType)
admin.site.register(Fermentation)
admin.site.register(FermentationFermentable)
admin.site.register(FermentationYeast)
admin.site.register(FermentationAdditive)
