from dataclasses import fields
import email
from xml.dom import ValidationErr
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Trip, Rating, UserPreference


class CreateUserForm(UserCreationForm): #inherits from Django's pre built usercreationform
    email = forms.EmailField(required=True)
    class Meta: #Define how we want our form to look like
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        def save(self, commit=True):
            user = super(UserCreationForm, self).save(commit=False)
            user.email = self.cleaned_data["email"]
            if commit:
                user.save()
            return user

class CreateTripForm(ModelForm):
    class Meta:
        model = Trip
        fields = ["location", "arrivalDate", "departureDate"]

class UserInterestsForm(ModelForm):
    class Meta:
        model = Rating
        fields = ["attraction", "rating"]

class UserPreferenceForm(ModelForm):
    class Meta:
        model = UserPreference
        fields = ["attraction_preference_1", "attraction_preference_2", "attraction_preference_3", "food_preference_1", "food_preference_2", "food_preference_3"]
