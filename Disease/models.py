from djongo import models
from disease.data import data_country



class DataModel(models.Model):
    fname = models.CharField(max_length=25)
    lname = models.CharField( max_length=25)
    email = models.EmailField()
    address = models.CharField( max_length=1000 )
    country = models.CharField( max_length=50,choices=data_country())#(('United States', 'United States'), ('India', 'India')) )
    zipcode = models.IntegerField()
    data = models.CharField( max_length=2000 )

