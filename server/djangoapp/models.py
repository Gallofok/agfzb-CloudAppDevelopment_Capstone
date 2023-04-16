from django.db import models

class CarMake(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    # Add any other fields you would like to include in a car make

    def __str__(self):
        return self.name


class CarModel(models.Model):
    CAR_TYPES = (
        ('S', 'Sedan'),
        ('SUV', 'Sport Utility Vehicle'),
        ('W', 'Wagon'),
    )
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer_id = models.IntegerField()
    name = models.CharField(max_length=50)
    car_type = models.CharField(max_length=3, choices=CAR_TYPES)
    year = models.DateField()
    # Add any other fields you would like to include in a car model

    def __str__(self):
        return self.name
