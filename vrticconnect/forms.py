from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User, Objava, Aktivnost, Fotografija

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "Zaposlen",
                   "Grupa", "first_name", "last_name")

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "Zaposlen")
        exclude = ["password"]

class ObjavaForm(forms.ModelForm):
    class Meta:
        model = Objava
        fields = ("Naslov", "Tekst")

class AktivnostForm(forms.ModelForm):
    class Meta:
        model = Aktivnost
        fields = ("Naziv", "Datum_aktivnosti")

class FotoForm(forms.ModelForm):
    class Meta:
        model = Fotografija
        fields = ('Naslov', 'Fotografija')