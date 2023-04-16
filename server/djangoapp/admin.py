from django.contrib import admin
from .models import CarMake, CarModel


class CarModelInline(admin.TabularInline):
    model = CarModel


class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]


class CarModelAdmin(admin.ModelAdmin):
    pass


admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
