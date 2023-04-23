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
class CarDealer:
    
    def __init__(self, id, city, state, st, address, zip, lat, long, short_name, full_name):
        self.id = id
        self.city = city
        self.state = state
        self.st = st
        self.address = address
        self.zip = zip
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.full_name = full_name


    def __str__(self):
        return "Dealer name: " + self.full_name + "\n" \
                + "Address: " + self.address + "\n" \
                + "City: " + self.city + "\n" \
                + "State: " + self.state + "\n" \
                + "Zip Code: " + self.zip + "\n" \
                + "Latitude: " + str(self.lat) + "\n" \
                + "Longitude: " + str(self.long) + "\n" \
                + "Short Name: " + self.short_name + "\n" \
                + "Dealer ID: " + str(self.id)


class Review(models.Model):
    dealership = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    purchase = models.BooleanField()
    review = models.TextField()
    purchase_date = models.DateField()
    car_make = models.CharField(max_length=50)
    car_model = models.CharField(max_length=50)
    car_year = models.IntegerField()
    sentiment = models.CharField(max_length=50)

    def __str__(self):
        return  self.review 
