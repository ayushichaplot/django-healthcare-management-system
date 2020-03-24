from django.contrib import admin
from .import models
from .models import State
from .models import City, Facility


# Register your models here.
admin.site.register(State)
admin.site.register(City)
admin.site.register(Facility)