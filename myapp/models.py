# from django.db import models
from django.db import models



# Create your models here.
class TaiwanRegion(models.Model):
    country_city = models.CharField(max_length=50)
    district_town = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.country_city} - {self.district_town}"