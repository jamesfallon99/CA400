from django.contrib import admin
# from .models import User
from .models import Review, Attraction, Rating, Trip, Location, UserPreference
# # Register your models here.
# admin.site.register(User)
admin.site.register(Review)
admin.site.register(UserPreference)
admin.site.register(Attraction)
admin.site.register(Rating)
admin.site.register(Trip)
admin.site.register(Location)
