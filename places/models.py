from django.db import models
import uuid
from .managers import CustomUserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError



class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Country(models.Model):
    id = models.UUIDField(primary_key = True, 
         default = uuid.uuid4, 
         editable = False) 
    name = models.CharField(max_length=50)
    country_code = models.CharField(max_length=2, unique=True)
    phone_code = models.CharField(max_length=10,unique=True, default='+91')
    my_user = models.ForeignKey(CustomUser, related_name="Country_CustomUser", null=True, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.id)



class State(models.Model):
    country = models.ForeignKey(Country, on_delete = models.CASCADE)
    id = models.UUIDField(primary_key = True, 
         default = uuid.uuid4, 
         editable = False) 
    name = models.CharField(max_length=50)
    state_code = models.CharField(max_length=2)
    phone_code = models.CharField(max_length=10,unique=True, default='+91')
    gst_code = models.IntegerField(unique=True)
    
    class Meta:
        unique_together = ['name', 'country']

    def __str__(self) -> str:
        return str(self.id)
        


class City(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key = True, 
         default = uuid.uuid4, 
         editable = False) 
    name = models.CharField(max_length=50)
    city_code = models.CharField(max_length=2)
    population = models.PositiveIntegerField()
    avg_age = models.PositiveIntegerField()
    num_of_adult_males = models.PositiveIntegerField()
    num_of_adult_females = models.PositiveIntegerField()

    def validate_population(self):
        if self.population < self.num_of_adult_females + self.num_of_adult_males:
            raise ValidationError("City's population must be greater than the summation of num_of_adult males and females")

    class Meta:
        unique_together = ['name', 'city_code','state']

    def save(self, *args, **kwargs):
        self.validate_population()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.id)
